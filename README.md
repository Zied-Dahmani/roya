# Roya - AI SMS Agent

AI-powered SMS generation agent using LangGraph and Grok.

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Google Sheets Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project and enable Google Sheets API
3. Create a Service Account and download `credentials.json`
4. Share your Google Sheet with the service account email

### 3. Grok API Setup

1. Get your API key from [xAI](https://x.ai/)
2. Add to `.env` file

### 4. Configure Environment

```bash
cp .env.example .env
# Edit .env with your values
```

### 5. Google Sheet Format

Create a sheet with these columns:

| Name | Phone | Product | Last Visit | SMS Sent | Reply | Chat History |
|------|-------|---------|------------|----------|-------|--------------|

## Usage

```bash
python main.py
```

The agent will:
1. Fetch leads from Google Sheet
2. Classify each as first contact or follow-up
3. Generate personalized SMS using Grok
4. Display SMS in console for manual sending
5. Optionally update sheet with chat history

## Project Structure

```
roya/
├── main.py              # Entry point
├── requirements.txt
├── .env.example
│
└── src/
    ├── config/          # Settings & constants
    ├── prompts/         # AI prompt templates
    ├── services/        # External integrations
    ├── agent/           # LangGraph flow
    ├── models/          # Data models
    └── utils/           # Helpers
```
