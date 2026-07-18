# 🎙️ NovaVoice AI — Production-Grade Gemini Live API Voice Agent Platform

> Ultra-low latency, real-time conversational AI voice platform powered by Gemini Live API, FastAPI, WebSockets, and modular voice infrastructure.

---

## ✨ Features

| Tool | Description |
|------|-------------|
| 📅 **Calendar** | Check availability and book 30-min meetings on Google Calendar |
| 🌤️ **Weather** | Real-time weather for any city worldwide (Open-Meteo, no API key) |
| ✉️ **Email** | Send reminder emails via Gmail SMTP |
| 📝 **Transcript** | Download full conversation history as Markdown |
| 🎨 **Premium UI** | Glassmorphic design, aurora animations, responsive layout |

---

# 🚀 Step 0 — Clone the Repository

First, clone the repository locally:

```bash
git clone https://github.com/coder-irwin/voice_ai_agents_using-Gemini_live_api.git
```

Move into the project directory:
```bash
cd voice_ai_agents_using-Gemini_live_api
```

📦 Step 1 — Create Virtual Environment

Windows
```bash
python -m venv venv

venv\Scripts\activate
```

macOS / Linux
```bash
python3 -m venv venv

source venv/bin/activate
```

---

NovaVoice is an ultra-low latency, bidirectional streaming voice assistant that integrates the **Gemini Live API** (`BidiGenerateContent` WebSocket protocol) with **Google Calendar**, **Weather**, and **Email** tools for a truly multi-purpose voice experience.

This repository contains the production-ready full-stack core, split into:
1. **Interactive Glassmorphic UI (Frontend):** Manages user media devices, WebRTC audio streams, continuous WebSocket piping, active barge-in (interruption), and a visual visualizer orb.
2. **Secure Python Gateway (Backend):** Protects long-term OAuth keys (`token.json`) and handles calendar, weather, and email API queries.

---

## 🗺️ Architectural Flow

```
🗣️ User (Voice/Mic) 
       │
       ▼ (16kHz PCM Mono)
🖥️ Web Browser UI (index.html on Port 8000) ───[WebSocket WSS]───► 🤖 Gemini Live API
       │                                                                │
       ▼ (Intercepts function call JSON)                                ▼ (Emits toolCall event)
🐍 Python API Server (api_server.py on Port 5000) ◄───────────────────────┘
       │
       ├──► 📅 Google Calendar (book_meeting, check_availability)
       ├──► 🌤️ Open-Meteo API (get_weather)
       └──► ✉️ Gmail SMTP (send_reminder)
```

---

## 🚀 Installation & Prerequisites

### Step 1: Install Dependencies
```powershell
pip install -r requirements.txt
```

> [!NOTE]
> The dependencies include `flask`, `flask-cors`, `google-api-python-client`, `google-auth-oauthlib`, `requests`, and other standard helpers.

---

## 🔑 Configuration

### Step 2: Configure your `.env` File
Create a file named `.env` in the root directory:

```ini
# Google Calendar OAuth
GOOGLE_CLIENT_ID=your_google_oauth_client_id
GOOGLE_CLIENT_SECRET=your_google_oauth_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback
HOST_CALENDAR_ID=your_email@gmail.com
HOST_EMAIL=your_email@gmail.com
FRONTEND_URL=http://localhost:8000
SECRET_KEY=your_random_secret_key_for_sessions

# Email Reminders (Optional — needed for send_reminder tool)
SMTP_EMAIL=your_email@gmail.com
SMTP_APP_PASSWORD=your_gmail_app_password
```

> [!TIP]
> **Gmail App Password:** Go to https://myaccount.google.com/apppasswords to generate one.
> You need 2FA enabled on your Google account first. The email tool will work without these,
> but will return a friendly error asking the user to configure it.

---

### Step 3: Enable Google Calendar API
1. Go to the **Google Calendar API** page in the Google Cloud Console:
   👉 **[Google Calendar API Console](https://console.cloud.google.com/marketplace/product/google/calendar-json.googleapis.com)**
2. Select your Google Cloud Project.
3. Click the blue **Enable** button.
4. After enabling, click **Manage**, and select the **Credentials** tab from the left sidebar.

---

### Step 4: Create OAuth 2.0 Credentials
1. Click **`+ Create credentials`** at the top of the Credentials page, then select **`OAuth client ID`**.
2. For **Application type**, select **`Web application`**.
3. Name your application **`Calendar Integration`**.
4. Scroll down to configure the redirect paths:
   * **Authorized JavaScript origins:**
     ```text
     http://localhost:8000
     ```
   * **Authorized redirect URIs:**
     ```text
     http://localhost:8000/auth/callback
     ```
5. Click **Create** and copy your **Client ID** and **Client Secret** into your `.env` file.
6. **Enable User Access:** In the Cloud Console left sidebar, click **OAuth consent screen**. Scroll to the **Test users** section, click **Add Users**, and enter your login email address (the calendar account you want to give access to).

---

### Step 5: Generate OAuth Credentials (`token.json`)
Start the authentication server:

```powershell
python auth_server.py
```

1. Open **`http://localhost:8000`** in your browser.
2. Click **Authorize Google Calendar** and sign in using your designated Google account.
3. Once the dashboard shows success, close the page and press `Ctrl+C` in your terminal to shut down the server. 
4. A secure **`token.json`** file will now be populated in your project root!

---

## 🎙️ Running the Live Assistant

### 1. Launch the Secure API Bridge (Terminal Window 1)
```powershell
python api_server.py
```
*(Starts the bridge listening on port `5000` with calendar, weather, and email endpoints)*

### 2. Serve the UI Dashboard (Terminal Window 2)
```powershell
python -m http.server 8000
```
*(Serves your interactive interface on port `8000`)*

### 3. Connect & Converse!
1. Navigate to: **`http://localhost:8000`** in Google Chrome.
2. Paste your **Gemini API Key** into the prompt and click connect.
3. Click the **🎙️** button and try these voice commands:

| Voice Command | Tool Triggered |
|--------------|----------------|
| *"Check if my calendar is free tomorrow"* | 📅 `check_availability` |
| *"Book a demo meeting at 3pm tomorrow"* | 📅 `book_meeting` |
| *"What's the weather in Tokyo?"* | 🌤️ `get_weather` |
| *"Send a reminder to john@email.com about the meeting"* | ✉️ `send_reminder` |

4. Click **📥 Download Transcript** to save the entire conversation as a Markdown file!

---

## 📂 Project Structure

```
├── index.html          # Premium glassmorphic UI with all tools
├── api_server.py       # Flask API bridge (4 endpoints)
├── calendar_tool.py    # Google Calendar read/write
├── weather_tool.py     # Open-Meteo weather fetcher
├── email_tool.py       # Gmail SMTP email sender
├── auth_server.py      # OAuth 2.0 token generator
├── requirements.txt    # Python dependencies
├── .env                # Configuration (you create this)
└── token.json          # OAuth token (auto-generated)
```
