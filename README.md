# 🎓 StudySense: AI-Powered Adaptive Learning Platform

![AI Learning](https://img.shields.io/badge/AI-Personalized_Learning-blueviolet?style=for-the-badge&logo=openai)
![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Flutter](https://img.shields.io/badge/Frontend-Flutter-02569B?style=for-the-badge&logo=flutter)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi)

**StudySense** is an intelligent, adaptive learning platform that uses AI to analyze student behavior, performance, and learning styles — delivering a custom-tailored educational experience instead of generic notes.

> ⚠️ **Never commit your `.env` file.** It is listed in `.gitignore`. Use `.env.example` as a safe template (see [Environment Variables](#environment-variables)).

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Quickstart](#quickstart)
- [Environment Variables](#environment-variables)
- [AI System](#ai-system)
- [Running Tests](#running-tests)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

StudySense comprises a Python FastAPI backend (AI services, adaptive engine, database access) and a Flutter frontend (Android, iOS, Web). The backend exposes REST endpoints for authentication, student data, courses, progress tracking, and AI services (doubt solver, recommendations). The AI engine uses ML models to predict student performance and personalize learning paths in real time.

---

## Key Features

### 🧠 AI Adaptive Learning Path
Tracks study speed, accuracy, and weak topics to dynamically adjust the curriculum.
- **Smart Pacing:** More examples when you struggle; fast-tracks when you're ahead.
- **Mastery-Based Progression:** Solid foundations before moving forward.

### 📷 Smart Doubt Solver
- **OCR Integration:** Upload images of handwritten or printed questions.
- **Step-by-Step Explanations:** LLM-powered reasoning, not just final answers.

### 📅 Automated Study Planner
- **Dynamic Schedules:** Daily/weekly study slots generated from your goals.
- **Calendar Sync:** Integrates with Google/Outlook calendars for real-time reminders.

### 🗺️ Weak-Spot Identification Dashboard
- **Knowledge Heatmap:** Visual overview of mastered vs. weak concepts.
- **Micro-Learning:** Targeted 5-minute sessions to close specific knowledge gaps.

---

## Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | Flutter (Android, iOS, Web) |
| **Backend** | Python (FastAPI) |
| **Database** | PostgreSQL (Relational), Pinecone (Vector Search) |
| **AI Engine** | OpenAI GPT-4o, LangChain, Scikit-Learn |
| **Auth** | Firebase Auth or Supabase Auth |

---

## Project Structure

```
studysense/
├── frontend/                           # Flutter application
│   ├── lib/
│   │   ├── main.dart                   # App entrypoint
│   │   ├── screens/                    # UI screens (Dashboard, Study Room, Doubt Solver)
│   │   ├── widgets/                    # Reusable UI components (Heatmaps, Charts)
│   │   └── services/                   # API client, auth, local storage
│   ├── pubspec.yaml                    # Flutter dependencies
│   └── test/                           # Widget & unit tests
├── Backend/
│   ├── app.py                          # FastAPI entrypoint
│   ├── config.py                       # Loads .env settings
│   ├── requirements.txt
│   ├── .env.example                    # ← Safe template; copy to .env and fill in values
│   ├── routes/                         # API route handlers
│   │   └── ai_routes_examples.py       # AI endpoint examples
│   ├── services/
│   │   ├── adaptive_engine.py
│   │   └── enhanced_adaptive_engine.py # ML-powered recommendations
│   └── ml/
│       ├── QUICKSTART.md
│       ├── AI_TRAINING_GUIDE.md
│       ├── recommendation_model.py
│       └── training/
│           ├── data_generator.py       # Synthetic student data
│           ├── adaptive_model.py       # Neural network model
│           ├── training_pipeline.py    # End-to-end training orchestration
│           ├── train.py                # CLI training interface
│           ├── example_usage.py        # Working code examples
│           └── trained_models/         # Created after first training run (git-ignored)
├── docs/                               # Design docs and guides
├── .gitignore
└── verify_ai_system.py                 # Health check script
```

---

## Quickstart

### Prerequisites

- Python 3.10+
- [Flutter SDK](https://docs.flutter.dev/get-started/install) 3.0+
- PostgreSQL (or Supabase)
- OpenAI or Hugging Face API key (for LLM features)

### 1. Clone the repo

```bash
git clone https://github.com/your-username/studysense.git
cd studysense
```

### 2. Backend Setup

```bash
# Create and activate a virtual environment
cd Backend
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .\.venv\Scripts\Activate.ps1  # Windows PowerShell

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Set up environment variables (see Environment Variables section)
cp .env.example .env
# Edit .env and fill in your actual values — do NOT commit this file

# Start the API server
python app.py
# or: uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

API available at `http://127.0.0.1:8000` — OpenAPI docs at `/docs`.

### 3. Flutter Frontend Setup

```bash
cd frontend

# Get dependencies
flutter pub get

# Run on a connected device or emulator
flutter run

# Build for web
flutter build web

# Build for Android
flutter build apk

# Build for iOS (macOS only)
flutter build ios
```

The Flutter app reads the backend URL from its own config. Update `lib/services/api_client.dart` (or equivalent) to point to your backend URL.

### 4. Train the AI Model

```bash
cd Backend/ml/training

# Quick mode (~2 minutes)
python train.py --quick
```

Output files created in `trained_models/` (this folder is git-ignored):
- `adaptive_model_YYYYMMDD_HHMMSS.pkl` — trained model
- `training_data.json` — training dataset
- `results.json` — evaluation metrics

---

## Environment Variables

**Never commit real credentials.** The `.env` file is listed in `.gitignore`.

Copy the example file and fill in your own values:

```bash
cp Backend/.env.example Backend/.env
```

`Backend/.env.example` (safe to commit — contains no real secrets):

```env
# Database
DATABASE_URL=postgresql://USER:PASSWORD@localhost:5432/adaptive_learning
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=replace-with-a-long-random-string

# AI / LLM providers — add only the key(s) you use
OPENAI_API_KEY=          # sk-...
HF_API_KEY=              # hf_...

# Supabase (if using Supabase instead of self-hosted PostgreSQL)
SUPABASE_URL=            # https://your-project.supabase.co
SUPABASE_KEY=            # your-anon-or-service-key

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=True               # Set to False in production
```

`config.py` loads `.env` automatically via `python-dotenv`.

### Keeping secrets safe on GitHub

Your `.gitignore` should include at minimum:

```
# Environment files
.env
.env.local
*.env

# Trained model artifacts
Backend/ml/training/trained_models/

# Python
__pycache__/
*.pkl
*.pyc
.venv/

# Flutter
frontend/.dart_tool/
frontend/build/
```

---

## AI System

### Model Architecture

The adaptive model is a neural network trained on student interaction data:

```
Input Features (5)
    ↓
Hidden Layer: 16 neurons (ReLU)
    ↓
Output: Predicted Performance Score (0–100)
```

**Input features:** Student level, course difficulty, engagement score, learning speed, time spent.

**Training:** Mini-batch SGD with Adam-style optimization, early stopping (patience=10), 20% validation split.

**Typical metrics:** MAE 8–10 pts · RMSE 10–12 pts · R² 0.88–0.92

### Key Capabilities

**Performance Prediction**
```python
prediction = engine.predict_performance(
    student_level=70,
    course_difficulty=75,
    engagement_score=0.8,
    learning_speed=1.2,
    time_spent_hours=10
)
# → {'predicted_score': 78.5, 'confidence': 0.92, ...}
```

**Course Recommendations** — ranks courses by predicted success, difficulty fit, and prediction confidence.

**Adaptive Difficulty Adjustment**
- Score > 80%: increase difficulty
- Score 50–80%: maintain
- Score < 50%: decrease difficulty

**Next Lesson Suggestion** — recommends the best next lesson based on student level, predicted performance, and completion likelihood.

### Integration Steps

1. **Train the model** — `python train.py --quick` (2 min)
2. **Add API routes** — copy `routes/ai_routes_examples.py` → `routes/ai_routes.py` and mount in `app.py` (30 min)
3. **Connect real data** — replace synthetic queries with live DB calls (1 hr)
4. **Flutter integration** — call the prediction and recommendation endpoints from `lib/services/` (1–2 hr)

See `Backend/ml/AI_TRAINING_GUIDE.md` and `Backend/IMPLEMENTATION_CHECKLIST.md` for detailed guidance.

---

## Running Tests

**Backend:**
```bash
# From repo root
pytest -q

# Quick AI system health check
python verify_ai_system.py
```

**Flutter:**
```bash
cd frontend

# Unit & widget tests
flutter test

# Integration tests
flutter test integration_test/
```

---

## Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Add tests where applicable
4. Open a pull request with a clear description of your changes

Please follow the existing code style and keep changes focused. Make sure no secrets or `.env` files are included in your PR.

---

## License

This project is licensed under the MIT License. Add a `LICENSE` file at the repo root to formalize it.
