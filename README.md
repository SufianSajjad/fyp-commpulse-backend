# CommPulse – Backend API

This is the backend component of **CommPulse**, an AI-driven meeting quality monitoring system. It provides APIs for audio processing, transcription, sentiment analysis, speaker diarization, agenda-based summarization, and user authentication.

## 🚀 Features

- 🎙️ Audio Capturing & Storage
- 🧠 Speaker Diarization
- 😊 Sentiment Analysis (per speaker)
- 📝 Agenda-Based Meeting Summarization
- 🔒 User Management & Authentication (JWT)
- 📊 Active Participation & Metric Generation

## 🧰 Tech Stack

- **Language**: Python
- **Framework**: Flask
- **Database**: PostgreSQL
- **AI Services**: Azure OpenAI, MS Teams SDK, SentenceTransformers
- **APIs**: RESTful JSON APIs for frontend integration

## 🗂️ Project Structure

```
commpulse-backend/
├── app.py
├── routes/
│   ├── auth/
│   ├── meeting_metrics/
├── utils/
├── models/
└── config.py
```

## 🛠️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/commpulse-backend.git
cd commpulse-backend
```

### 2. Create Virtual Environment & Install Dependencies

```bash
python -m venv venv
venv\Scripts\activate   # Windows
# or source venv/bin/activate  # Linux/macOS

pip install -r requirements.txt
```

### 3. Set Environment Variables

Create a `.env` file in the root with values like:

```
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=postgresql://user:password@localhost/db_name
AZURE_OPENAI_KEY=your_key
```

### 4. Run the App

```bash
python app.py
```

## 📌 License

This is a Final Year Project for FAST NUCES. Not intended for commercial use.
