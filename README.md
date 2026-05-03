# AI-Powered Python Tutor

> A hybrid rule-based + GPT-4 mobile tutoring system for teaching beginner Python programming.
> Built with Flutter (mobile) and Flask (backend).

## Project Structure

```
Shelter Project/
├── backend/               # Flask REST API
│   ├── app/
│   │   ├── routes/        # Auth, Lessons, Practice, Chat, Progress endpoints
│   │   ├── models/        # SQLAlchemy database models
│   │   └── engine/        # Rule-Based Engine + Hybrid Controller + NLP Module
│   ├── knowledge_base/    # JSON/YAML rule files (updatable without redeployment)
│   ├── config.py
│   ├── requirements.txt
│   ├── run.py
│   └── .env.example       # Copy to .env and fill in your secrets
│
├── mobile/                # Flutter mobile app (Android + iOS)
│   ├── lib/
│   │   ├── constants/     # Theme, API URLs
│   │   ├── models/        # Dart data models
│   │   ├── screens/       # Auth, Home, Lesson, Chat, Practice, Progress
│   │   ├── services/      # Auth, API service classes
│   │   └── widgets/       # Reusable UI components
│   └── pubspec.yaml
│
└── AI_Python_Tutor_PRD.md # Product Requirements Document
```

## Getting Started

### Backend

```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env   # Then fill in your OPENAI_API_KEY and SECRET keys
python run.py
```

### Mobile (Flutter)

> **Requires Flutter SDK**: [Install Flutter](https://docs.flutter.dev/get-started/install/windows)

```bash
cd mobile
flutter pub get
flutter run
```

## Tech Stack

| Layer | Technology |
|---|---|
| Mobile | Flutter (Dart) |
| Backend | Flask (Python) |
| Database | SQLite |
| AI | GPT-4 (OpenAI API) |
| Auth | JWT + bcrypt |
