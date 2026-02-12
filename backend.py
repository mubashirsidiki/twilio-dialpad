from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant
from twilio.twiml.voice_response import VoiceResponse
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Twilio credentials - load from environment
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER", "")

# Twilio API Key - you need to create one in Twilio Console
# Go to https://console.twilio.com/us1/develop/api-keys/create
# Create a "Standard" API key with "Voice" permissions
TWILIO_API_KEY = os.getenv("TWILIO_API_KEY", "YOUR_API_KEY_SID")
TWILIO_API_SECRET = os.getenv("TWILIO_API_SECRET", "YOUR_API_KEY_SECRET")

# Your Twilio TwiML Application SID
# Create at https://console.twilio.com/us1/develop/sip/trunking
# Or use Programmable Voice -> TwiML Apps
TWIML_APP_SID = os.getenv("TWIML_APP_SID", "YOUR_TWIML_APP_SID")
DEFAULT_NUMBER = os.getenv("DEFAULT_NUMBER", "")


@app.get("/")
async def root():
    with open("index.html", "r") as f:
        content = f.read()
        # Inject default number if set
        if DEFAULT_NUMBER:
            content = content.replace(
                'placeholder="Phone Number"', f'placeholder="Phone Number" value="{DEFAULT_NUMBER}"'
            )
        return HTMLResponse(content)


@app.get("/config")
async def config():
    """Return default number for frontend"""
    return JSONResponse({"defaultNumber": DEFAULT_NUMBER})


@app.get("/static/twilio.js")
async def serve_twilio_sdk():
    """Serve the Twilio Voice SDK"""
    with open("twilio.min.js", "r") as f:
        return Response(content=f.read(), media_type="application/javascript")


@app.post("/voice")
async def voice(request: Request):
    """TwiML endpoint for handling voice calls"""
    form_data = await request.form()
    to_number = form_data.get("To", "")
    print(f"Voice endpoint called - To: {to_number}, All data: {dict(form_data)}")

    response = VoiceResponse()
    response.dial(number=to_number, caller_id=TWILIO_NUMBER)

    twiml = str(response)
    print(f"Returning TwiML: {twiml}")
    return Response(content=twiml, media_type="application/xml")


@app.get("/token-debug")
async def debug_token():
    """Debug endpoint to see token details without decoding"""
    token = AccessToken(
        TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, identity="web-dialer-user"
    )
    voice_grant = VoiceGrant(
        outgoing_application_sid=TWIML_APP_SID,
        incoming_allow=True,
    )
    token.add_grant(voice_grant)
    jwt_token = token.to_jwt()
    return JSONResponse({
        "token": jwt_token,
        "account_sid": TWILIO_ACCOUNT_SID,
        "api_key": TWILIO_API_KEY,
        "twiml_app_sid": TWIML_APP_SID,
    })


@app.get("/token")
async def get_token():
    """Generate a Twilio JWT token for the client"""
    print(f"Creating token with: AccountSID={TWILIO_ACCOUNT_SID}, APIKey={TWILIO_API_KEY}, TwiMLApp={TWIML_APP_SID}")

    token = AccessToken(
        TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, identity="web-dialer-user"
    )

    voice_grant = VoiceGrant(
        outgoing_application_sid=TWIML_APP_SID,
        incoming_allow=True,
    )
    token.add_grant(voice_grant)

    jwt_token = token.to_jwt()
    print(f"Token generated, length: {len(jwt_token)}")

    return JSONResponse({"token": jwt_token})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
