# Goal Description

The goal is to create a comprehensive, step-by-step implementation plan for the AI-Powered Personalized Tutor for Teaching Basic Python Programming, based on the provided Product Requirements Document (PRD). The system is a hybrid application comprising a Flutter mobile frontend, a Flask REST API backend, and an intelligent tutoring system combining rule-based logic with OpenAI's GPT-4.

## User Review Required

Please review the proposed implementation phases below. Let me know if the ordering aligns with your expectations, or if you prefer a different approach (e.g., focusing entirely on the AI backend first before starting the mobile app).

> [!IMPORTANT]
> This plan breaks down the PRD into actionable, sequential development steps. Once approved, we will track our progress through a task list.

## Open Questions

- **Database:** Do you want to stick with SQLite for the initial local development, or jump straight to Firebase/PostgreSQL?
- **API Key:** Do you already have an OpenAI API key available for testing the GPT-4 integration?
- **Development Priority:** Do you prefer starting with the Flask Backend & AI Controller or the Flutter Mobile App? (The plan assumes Backend-first).

---

## Proposed Implementation Plan

The implementation is broken down into 8 logical phases to ensure structured development.

### Phase 1: Project Setup and Architecture Initialization
Establish the foundational environments for both frontend and backend.
- Initialize a Git repository for version control.
- Set up the **Flask backend** project structure (virtual environment, dependencies like `Flask`, `Flask-JWT-Extended`, `SQLAlchemy`, `openai`).
- Set up the **Flutter mobile** project structure (dependencies like `provider` or `riverpod` for state management, `http` or `dio` for API calls, `shared_preferences`).

### Phase 2: Database Design and Core API (Flask)
Implement the data models and core functional endpoints.
- Define the database schema (SQLite) for `User`, `Lesson`, `PracticeQuestion`, `UserProgress`, and `ChatLog`.
- Implement **Authentication endpoints** (`/auth/register`, `/auth/login`, `/auth/logout`) with JWT generation and password hashing (bcrypt).
- Implement **Lesson and Progress API endpoints** (`/lessons`, `/lessons/:id`, `/progress`, etc.).
- Implement **Practice endpoints** (`/practice/:id`, `/practice/:id/submit`).

### Phase 3: Knowledge Base and Content Population
Populate the system with the required educational content.
- Seed the database with the **9 beginner Python topics**, their explanations, and code examples.
- Seed the database with **practice questions** (5-10 per topic) and their corresponding hints.
- Create the **Rule-Based Engine JSON/YAML files** containing intents, keywords, and pre-authored responses for concepts and errors.

### Phase 4: Hybrid AI Engine Development (Flask)
Build the core intelligence of the application.
- **Rule-Based Engine:** Implement the keyword matching and intent classification logic (confidence ≥ 0.7 threshold).
- **NLP Module:** Implement the GPT-4 API integration using the structured prompt templates defined in the PRD.
- **Hybrid Controller:** Build the orchestrator that routes user queries, handles fallbacks (timeouts, errors), and validates GPT-4 responses against off-topic or advanced content constraints.
- Implement the `/chat` endpoint connecting the frontend to the Hybrid Controller.

### Phase 5: Mobile Frontend Foundation (Flutter)
Start building the mobile user interface and state management.
- Set up theme and styling (adhering to WCAG 2.1 Level AA and beginner-friendly UI).
- Implement the **Onboarding and Authentication flows** (Splash screen, Login, Registration) and secure token storage.
- Build the **Home Dashboard** displaying the user's name, last topic, and a list of all 9 topics.

### Phase 6: Mobile Core Features Integration (Flutter)
Connect the mobile UI to the backend content and interactive features.
- Implement the **Lesson Screen** (Explanation card, annotated code snippet with syntax highlighting, key points).
- Implement the **Practice & Assessment flow** (Multiple choice UI, displaying rule-based hints on incorrect answers, score summary).
- Implement the **Progress Screen** showing completion percentages and mastery badges.

### Phase 7: Mobile Chat Interface Integration (Flutter)
Integrate the conversational tutoring feature.
- Build the **Chat Screen UI** (chat history bubbles, typing indicators).
- Connect the chat UI to the `/chat` backend endpoint.
- Implement suggested "quick question" chips above the chat input field.

### Phase 8: Testing, Refinement, and Deployment
Ensure the system meets the non-functional requirements and deploy the prototype.
- **Functional Testing:** Test all API endpoints (via Postman) and mobile flows.
- **Performance & Accuracy Testing:** Verify chat response time (< 5 seconds) and validate hybrid controller accuracy.
- **Deployment:** Deploy the Flask backend to Render or Railway. Configure environment variables (GPT-4 API key).
- Build the Android APK for prototype testing.

## Verification Plan

### Automated/API Verification
- Use Postman to test backend endpoints (`auth`, `lessons`, `chat`).
- Verify rate limiting and timeout fallbacks in the AI module.

### Manual Verification
- Run the Flutter app on an Android emulator or physical device.
- Step through the complete user journey (Register -> Read Lesson -> Ask Question -> Take Practice Quiz -> View Progress).
- Verify UI responsiveness and error handling.
