# Twilio Web Dialer

Minimal browser-based dialpad for making calls through Twilio.

## Features

- Click-to-dial keypad interface
- Keyboard input support
- Browser-based VoIP calling
- Default number pre-configuration

## Prerequisites

- Twilio account with Voice enabled
- Python 3.10+
- ngrok (for local development)

## Setup

### 1. Install Dependencies

```bash
uv pip install -r requirements.txt
```

Or with pip:
```bash
pip install fastapi uvicorn[standard] twilio python-dotenv python-multipart
```

### 2. Configure Environment

Create a `.env` file:

```env
TWILIO_ACCOUNT_SID=ACxxxxx
TWILIO_AUTH_TOKEN=xxxxx
TWILIO_NUMBER=+1xxxxx
TWILIO_API_KEY=SKxxxxx
TWILIO_API_SECRET=xxxxx
TWIML_APP_SID=APxxxxx
DEFAULT_NUMBER=+1xxxxx
```

### 3. Twilio Console Setup

**Create API Key:**
1. Go to https://console.twilio.com/us1/develop/api-keys/create
2. Type: **Standard**
3. Permissions: **Voice**
4. Save SID and Secret to `.env`

**Create TwiML App:**
1. Go to https://console.twilio.com/us1/develop/voice/twiml-apps
2. Create new TwiML App
3. Set Voice URL to your ngrok URL: `https://xxx.ngrok-free.app/voice`
4. Save App SID to `.env`

**Verify Phone Numbers** (Trial accounts only):
1. Go to https://console.twilio.com/us1/develop/phone-numbers/manage/verified
2. Add numbers you want to call

### 4. Run Server

```bash
uv run python backend.py
```

### 5. Expose with ngrok

```bash
ngrok http 8000
```

Update your TwiML App Voice URL to the ngrok URL.

## Usage

1. Open the ngrok URL in your browser
2. Click the dialpad buttons or type numbers
3. Press the blue call button to dial
4. Press again to hangup

**Keyboard Shortcuts:**
- `0-9 * #` — Input digits
- `Backspace` — Delete digit
- `Enter` — Toggle call

## Trial Account Limitations

- Can only call verified phone numbers
- Upgrade to paid account for unrestricted calling

## Files

- `backend.py` — FastAPI server for token generation
- `index.html` — Dialpad UI
- `twilio.min.js` — Twilio Voice SDK (downloaded locally)
