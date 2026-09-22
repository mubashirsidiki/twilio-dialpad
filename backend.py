from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant
from twilio.twiml.voice_response import VoiceResponse
from dotenv import dotenv_values

env = dotenv_values(".env")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Twilio configuration - loaded via dotenv
TWILIO_NUMBER_FOR_MAKING_CALLS = env.get("TWILIO_NUMBER_FOR_MAKING_CALLS") or ""
NUMBER_FOR_RECEIVING_CALLS = env.get("NUMBER_FOR_RECEIVING_CALLS") or ""
TWILIO_API_SID = env.get("TWILIO_API_SID") or ""
TWILIO_API_CLIENT_SECRET = env.get("TWILIO_API_CLIENT_SECRET") or ""
TWILIO_ACCOUNT_SID = env.get("TWILIO_ACCOUNT_SID") or ""
TWIML_APP_SID = env.get("TWIML_APP_SID") or ""


@app.get("/")
async def root():
    with open("index.html", "r") as f:
        content = f.read()
        # Inject receiving/default number if set
        if NUMBER_FOR_RECEIVING_CALLS:
            content = content.replace(
                'placeholder="Phone Number"', f'placeholder="Phone Number" value="{NUMBER_FOR_RECEIVING_CALLS}"'
            )
        return HTMLResponse(content)


@app.get("/config")
async def config():
    """Return default/receiving number for frontend"""
    return JSONResponse({"defaultNumber": NUMBER_FOR_RECEIVING_CALLS})



@app.post("/voice")
async def voice(request: Request):
    """TwiML endpoint for handling voice calls"""
    form_data = await request.form()
    to_number = form_data.get("To", "")
    print(f"Voice endpoint called - To: {to_number}, All data: {dict(form_data)}")

    # Route to NUMBER_FOR_RECEIVING_CALLS if incoming or not specified
    if (not to_number or to_number == TWILIO_NUMBER_FOR_MAKING_CALLS) and NUMBER_FOR_RECEIVING_CALLS:
        to_number = NUMBER_FOR_RECEIVING_CALLS

    response = VoiceResponse()
    response.dial(number=to_number, caller_id=TWILIO_NUMBER_FOR_MAKING_CALLS)

    twiml = str(response)
    print(f"Returning TwiML: {twiml}")
    return Response(content=twiml, media_type="application/xml")


@app.get("/token-debug")
async def debug_token():
    """Debug endpoint to see token details without decoding"""
    token = AccessToken(
        TWILIO_ACCOUNT_SID, TWILIO_API_SID, TWILIO_API_CLIENT_SECRET, identity="web-dialer-user"
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
        "api_key": TWILIO_API_SID,
        "twiml_app_sid": TWIML_APP_SID,
    })


@app.get("/token")
async def get_token():
    """Generate a Twilio JWT token for the client"""
    print(f"Creating token with: AccountSID={TWILIO_ACCOUNT_SID}, APIKey={TWILIO_API_SID}, TwiMLApp={TWIML_APP_SID}")

    token = AccessToken(
        TWILIO_ACCOUNT_SID, TWILIO_API_SID, TWILIO_API_CLIENT_SECRET, identity="web-dialer-user"
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
