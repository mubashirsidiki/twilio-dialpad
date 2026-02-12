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
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- [ngrok](https://ngrok.com/download) (for local development)

## Setup

### 1. Clone and Install Dependencies

```bash
git clone https://github.com/mubashirsidiki/twilio-dialpad.git
cd twilio-dialpad
uv sync
```

Or with pip:
```bash
pip install fastapi uvicorn[standard] twilio python-dotenv python-multipart
```

**Download Twilio Voice SDK:**

Twilio Voice SDK v2+ is not available via CDN. Download it locally:

```bash
curl -L -o twilio.min.js https://unpkg.com/@twilio/voice-sdk@2.1.2/dist/twilio.min.js
```

Or download manually from: https://www.npmjs.com/package/@twilio/voice-sdk

### 2. Configure Environment

Copy the example environment file and add your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your Twilio credentials:

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
3. Set Voice URL to: `https://your-ngrok-url.ngrok-free.app/voice`
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

Copy the ngrok URL and update your TwiML App's Voice URL in Twilio Console.

### 6. Open in Browser

Navigate to your ngrok URL (e.g., `https://xxx.ngrok-free.app`)

## Usage

1. Open the ngrok URL in your browser
2. Click the dialpad buttons or type numbers directly
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
- `.env.example` — Environment template
- `pyproject.toml` — Python dependencies

## License

MIT
