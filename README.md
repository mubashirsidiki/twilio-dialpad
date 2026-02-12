# Twilio Web Dialer

Minimal browser-based dialpad for making calls through Twilio.

## Quick Start

```bash
git clone https://github.com/mubashirsidiki/twilio-dialpad.git
cd twilio-dialpad
uv sync
curl -L -o twilio.min.js https://unpkg.com/@twilio/voice-sdk@2.1.2/dist/twilio.min.js
cp .env.example .env
# Edit .env with credentials from: https://docs.google.com/spreadsheets/d/1qYvlaUrC4542Bj6IKFS-lvnid0N4ZkKeEzhACcDX0dY/edit?gid=0#gid=0
uv run python backend.py
```

In another terminal:
```bash
ngrok http 8000
# Copy the https URL to your TwiML App's Voice URL in Twilio Console
```

## Twilio Console Setup

1. **API Key**: https://console.twilio.com/us1/develop/api-keys/create → Standard + Voice
2. **TwiML App**: https://console.twilio.com/us1/develop/voice/twiml-apps → Set Voice URL to your ngrok URL
3. **Verify Numbers** (trial): https://console.twilio.com/us1/develop/phone-numbers/manage/verified

## Usage

- Open ngrok URL in browser
- Click dialpad buttons or type numbers
- Press blue button to call, press again to hangup

**Keyboard**: `0-9 * #` input, `Backspace` delete, `Enter` call

## Trial Account

Can only call verified numbers. Upgrade to paid for unrestricted calling.

## Files

- `backend.py` — FastAPI server
- `index.html` — Dialpad UI
- `twilio.min.js` — Twilio SDK (download separately)
- `.env.example` — Environment template

MIT License
