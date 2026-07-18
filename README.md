# 🎙️ VoiceNemo — Production-Grade Gemini Live API Voice Agent Platform

> Authored by **Rudra-clrscr** (https://github.com/Rudra-clrscr)

VoiceNemo is an ultra-low latency, bidirectional streaming voice assistant that integrates the **Gemini Live API** (`BidiGenerateContent` WebSocket protocol) with **Google Calendar**, **Weather**, and **Email** tools for a fully conversational developer utility experience. It features a bold, ultra-minimalist, neo-brutalist theme designed with robust grid patterns and dark high-contrast components.

---

## ✨ Features

| Tool | Description |
|------|-------------|
| 📅 **Calendar** | Check availability and book meetings on Google Calendar |
| 🌤️ **Weather** | Fetch real-time weather conditions globally via Open-Meteo (no API key needed) |
| ✉️ **Email** | Send stylized HTML reminders via Gmail SMTP |
| 📥 **Logs** | Download full conversation logs as Markdown |
| 🎨 **Bold UI** | Retro OS terminal theme with offset drop shadows, Space Grotesk, and JetBrains Mono typography |

---

## 🗺️ Architectural Flow

```
🗣️ User (Voice/Mic) 
       │
       ▼ (16kHz PCM Mono Audio)
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

## 🚀 Local Installation & Setup

### Step 1: Install Dependencies
Ensure you have Python 3.10+ installed. Clone the repository and install the dependencies:
```powershell
pip install -r requirements.txt
```

---

### Step 2: Configure your `.env` File
Create a `.env` file in the root directory and configure your credentials:
```ini
# Google Calendar OAuth (Configured in Google Cloud Console)
GOOGLE_CLIENT_ID=your_google_oauth_client_id
GOOGLE_CLIENT_SECRET=your_google_oauth_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback
HOST_CALENDAR_ID=your_email@gmail.com
HOST_EMAIL=your_email@gmail.com
FRONTEND_URL=http://localhost:8000
SECRET_KEY=your_random_secret_key_for_sessions

# Email Reminders (Gmail App Password)
SMTP_EMAIL=your_email@gmail.com
SMTP_APP_PASSWORD=your_gmail_app_password
```

> [!TIP]
> **Gmail App Password:** You must have 2FA enabled on your Google account. Go to https://myaccount.google.com/apppasswords to generate your SMTP App Password.

---

### Step 3: Google Cloud & Calendar OAuth Setup
1. Go to the **[Google Cloud Console Credentials Page](https://console.cloud.google.com/apis/credentials)**.
2. Select or create your developer project.
3. Enable the **Google Calendar API**.
4. Go to **OAuth consent screen**, set the project to **Testing**, and add your email to the **Test users** list.
5. Create **OAuth client ID** credentials for a **Web application**:
   - **Authorized JavaScript origins**: `http://localhost:8000`
   - **Authorized redirect URIs**: `http://localhost:8000/auth/callback`
6. Copy the Client ID and Secret into your `.env` file.
7. Run the local OAuth server:
   ```powershell
   python auth_server.py
   ```
8. Open `http://localhost:8000` in your browser, log in with your test account, authorize Google Calendar, and close the server. A secure `token.json` credentials token will be populated in your root directory!

---

## 🎙️ Running the Assistant

### 1. Launch the Secure API Bridge (Terminal 1)
```powershell
python api_server.py
```
*(Runs on port `5000` handling Calendar, Weather, and Email API calls)*

### 2. Serve the UI Dashboard (Terminal 2)
```powershell
python -m http.server 8000
```
*(Serves the frontend interface on port `8000`)*

### 3. Connect & Converse
1. Open **`http://localhost:8000`** in Google Chrome.
2. Enter your **Gemini API Key** in the installer prompt and click connect.
3. Tap the **🎙️** button and issue voice commands like:
   - *"Check if my calendar is free tomorrow."*
   - *"Book a demo meeting tomorrow at 3pm."*
   - *"What's the weather like in Tokyo?"*
   - *"Send a reminder email to my friend about the meeting."*
4. Click **📥 DOWNLOAD TRANSCRIPT** to save your conversation log as Markdown.
