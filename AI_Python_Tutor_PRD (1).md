# PRODUCT REQUIREMENTS DOCUMENT (PRD)

## Project Title
AI-Powered Personalized Tutor for Teaching Basic Python Programming Using a Hybrid Rule-Based and NLP Approach

---

**Author:** Ayegba Shelter Iye
**Matric Number:** U22CS1030
**Supervisor:** Mrs. Onyinye Vivian Okpoko
**Institution:** Department of Computer Science, Airforce Institute of Technology (AFIT)
**Degree:** Bachelor of Science (B.Sc.) in Computer Science
**Document Version:** 1.0

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Product Overview](#2-product-overview)
3. [User Personas](#3-user-personas)
4. [User Journey Flow](#4-user-journey-flow)
5. [Functional Requirements](#5-functional-requirements)
6. [Non-Functional Requirements](#6-non-functional-requirements)
7. [System Architecture](#7-system-architecture)
8. [API Design](#8-api-design)
9. [Data Models](#9-data-models)
10. [NLP Integration (GPT-4)](#10-nlp-integration-gpt-4)
11. [Rule-Based Engine Design](#11-rule-based-engine-design)
12. [Hybrid Controller Design](#12-hybrid-controller-design)
13. [Security Design](#13-security-design)
14. [Tools and Technologies](#14-tools-and-technologies)
15. [Hardware Requirements](#15-hardware-requirements)
16. [Testing Strategy](#16-testing-strategy)
17. [Deployment Plan](#17-deployment-plan)
18. [Ethical Considerations](#18-ethical-considerations)
19. [System Constraints and Limitations](#19-system-constraints-and-limitations)
20. [Assumptions](#20-assumptions)
21. [Future Improvements](#21-future-improvements)
22. [Glossary](#22-glossary)

---

## 1. Introduction

### 1.1 Purpose

This document defines the complete functional and non-functional requirements for an AI-powered mobile tutoring system designed to teach basic Python programming to beginners. The system uses a hybrid architecture that combines a deterministic rule-based engine with a generative NLP model (GPT-4), coordinated by a hybrid controller to deliver accurate, beginner-friendly, and personalized learning support.

### 1.2 Background

Programming education in Nigeria faces persistent challenges: large class sizes, limited one-on-one guidance, and inadequate learning materials leave many beginners struggling with foundational concepts. Studies confirm that beginners require timely feedback, scaffolded explanations, and simplified instruction to build confidence and overcome early difficulties in coding.

Purely rule-based tutoring systems are reliable but rigid — they cannot handle open-ended conceptual questions. Purely generative NLP systems are flexible but prone to producing inaccurate or inconsistent explanations for novice learners. This project directly addresses that gap by combining both approaches in a hybrid architecture.

### 1.3 Aim

To develop an AI-powered personalized tutor for teaching basic Python programming using a hybrid rule-based and NLP approach, deployed as a Flutter mobile application with a Flask backend.

### 1.4 Objectives

- **OBJ-01:** Design a mobile-based AI tutor using Flutter (frontend) and Flask (backend) that delivers interactive, personalized learning support.
- **OBJ-02:** Implement a hybrid intelligent tutoring architecture that integrates a structured rule-based Python knowledge base with a generative NLP model (GPT-4).
- **OBJ-03:** Evaluate the system's performance, accuracy, usability, and learning effectiveness through functional testing, accuracy testing, performance testing, and a user study.

### 1.5 Scope

The system will:
- Be deployed as a Flutter mobile application supporting Android 8.0+ and iOS 13+.
- Cover beginner Python topics: variables, data types, operators, conditionals, loops, functions, lists, dictionaries, and basic error explanations.
- Provide interactive features: lesson explanations, step-by-step guidance, code examples, practice questions, chat-based assistance, topic navigation, and basic progress tracking.
- Use a hybrid architecture combining a JSON/YAML rule-based knowledge base with GPT-4 for adaptive NLP explanations.
- Use a Flask backend for inference coordination, rule-based retrieval, and response filtering.

The system will **not**:
- Execute Python code directly (no live sandboxed execution environment).
- Cover advanced Python topics (OOP, file handling, external libraries, data structures beyond lists and dictionaries).
- Function fully offline (generative NLP requires active internet).
- Provide a web or desktop version in this development phase.

---

## 2. Product Overview

### 2.1 Target Users

| User Type | Description |
|---|---|
| Primary | Absolute beginners in Python with no prior programming experience |
| Secondary | Students in Nigerian universities learning Python for the first time |
| Tertiary | Self-paced learners seeking foundational Python knowledge |

### 2.2 Key Features

| Feature | Description |
|---|---|
| Hybrid AI Tutoring | Rule-based engine + GPT-4 NLP, validated by a hybrid controller |
| Structured Lessons | Curriculum of 9 beginner Python topics with examples and exercises |
| Conversational Chat | Chat interface for asking questions and receiving explanations |
| Practice Questions | Per-topic exercises with rule-validated hint and feedback responses |
| Progress Tracking | User progress stored per topic and per session |
| Topic Navigation | Browse topics freely after registration |
| Beginner-Friendly UI | Simple, clean mobile UI optimized for low-literacy tech users |

### 2.3 Platform

- **Mobile App:** Flutter (Android 8.0+, iOS 13+)
- **Backend:** Flask (Python)
- **AI Model:** GPT-4 API (OpenAI)
- **Rule Base:** JSON/YAML files + Python scripts
- **Database:** SQLite (prototype)

---

## 3. User Personas

### Persona 1 — Amina (Primary User)
- **Age:** 19
- **Background:** First-year Computer Science student at AFIT with zero programming experience
- **Goals:** Understand what variables and loops mean; pass her intro to programming course
- **Pain Points:** Lecture content moves too fast; afraid to ask questions in class
- **Device:** Android smartphone (4GB RAM)
- **Connectivity:** Moderate internet access (Wi-Fi at school, data at home)

### Persona 2 — Chukwuemeka (Self-Paced Learner)
- **Age:** 24
- **Background:** HND graduate learning Python independently to improve job prospects
- **Goals:** Learn Python basics at his own pace, practice with exercises
- **Pain Points:** Online tutorials are too advanced or too fast
- **Device:** Android smartphone (3GB RAM)
- **Connectivity:** Limited data; prefers short sessions

### Persona 3 — Instructor (Admin User)
- **Role:** Lecturer or academic supervisor
- **Goals:** Monitor student progress, update lesson content, review rule entries
- **Access:** Admin dashboard (backend-facing, not in mobile app scope for v1)

---

## 4. User Journey Flow

The user journey is divided into five major stages: **Onboarding**, **Learning**, **Conversational Tutoring**, **Practice & Assessment**, and **Progress Review**.

---

### 4.1 Stage 1 — Onboarding

```
[User downloads app]
        │
        ▼
[Splash Screen — App logo, brief tagline]
        │
        ▼
[Welcome Screen]
    ┌───┴───┐
    │       │
[Sign Up] [Log In]
    │       │
    ▼       ▼
[Registration Form]       [Login Form]
  - Full Name              - Email
  - Email                  - Password
  - Password               │
  - Confirm Password        ▼
  - Skill Level (None /    [Auth Token Issued]
    Little / Some)          │
    │                       ▼
    ▼                  [Home Dashboard]
[Profile Created]
    │
    ▼
[Short Onboarding Tour — 3 slides]
  Slide 1: "Ask me anything about Python"
  Slide 2: "Learn step by step with lessons"
  Slide 3: "Track your progress"
    │
    ▼
[Home Dashboard]
```

**Home Dashboard Elements:**
- Greeting with user's name
- "Continue Learning" card (last topic accessed)
- Topic list (9 beginner topics)
- Progress bar (% of topics completed)
- Chat button (floating action button)

---

### 4.2 Stage 2 — Structured Learning

```
[Home Dashboard]
        │
        ▼
[Topic List Screen]
  - Variables & Data Types
  - Operators
  - Conditionals (if/else)
  - Loops (for/while)
  - Functions
  - Lists
  - Dictionaries
  - Error Types & Debugging
  - Basic I/O (input/print)
        │
        ▼ (User selects a topic)
[Lesson Screen]
  ┌─────────────────────────────────┐
  │  Topic Title                    │
  │  ─────────────────────────────  │
  │  [Explanation Card]             │
  │   - Plain-language definition   │
  │   - Real-world analogy          │
  │  ─────────────────────────────  │
  │  [Code Example Card]            │
  │   - Highlighted code snippet    │
  │   - Line-by-line breakdown      │
  │  ─────────────────────────────  │
  │  [Key Points Summary]           │
  │  ─────────────────────────────  │
  │  [Next: Practice Question →]    │
  └─────────────────────────────────┘
        │
        ▼
[Mark Topic as "Studied"]
  → Progress updated in database
  → "Practice" button enabled
```

---

### 4.3 Stage 3 — Conversational Tutoring (Chat)

```
[User taps Chat FAB or "Ask a Question" button]
        │
        ▼
[Chat Screen]
  - Conversation history shown
  - Text input field at bottom
        │
        ▼ (User types a question)
[User Query Sent to Flask Backend]
        │
        ▼
[Hybrid Controller — Processing Pipeline]
  ┌─────────────────────────────────────┐
  │  Step 1: Intent Detection           │
  │   - Is it a Python concept query?   │
  │   - Is it a hint request?           │
  │   - Is it off-topic?                │
  │                                     │
  │  Step 2: Rule-Base Lookup           │
  │   - Match query keywords to JSON    │
  │     rule entries                    │
  │   - If match found → use rule       │
  │     response as grounding context   │
  │                                     │
  │  Step 3: GPT-4 NLP Generation       │
  │   - Send grounded prompt to GPT-4   │
  │   - Include lesson context +        │
  │     rule-base snippet               │
  │   - Receive generated explanation   │
  │                                     │
  │  Step 4: Hybrid Validation          │
  │   - Check for Python keyword        │
  │     accuracy                        │
  │   - Check response stays within     │
  │     beginner scope                  │
  │   - If flagged → fallback to        │
  │     rule-based answer               │
  └─────────────────────────────────────┘
        │
        ▼
[Response Displayed in Chat Bubble]
  - If rule-based: "Here's what I know..."
  - If NLP-generated: "Let me explain..."
  - If off-topic: "I can only help with
    Python basics. Try asking about loops
    or variables."
        │
        ▼
[User may follow up or return to lesson]
```

---

### 4.4 Stage 4 — Practice & Assessment

```
[User taps "Practice" on a completed topic]
        │
        ▼
[Practice Screen]
  - Multiple-choice question displayed
  - 4 options shown
  - "Submit Answer" button
        │
    ┌───┴───────────────────┐
    │                       │
[Correct Answer]     [Wrong Answer]
    │                       │
    ▼                       ▼
[Positive Feedback]   [Rule-Based Hint]
 "Great job! Here's   "That's not right.
  why this is right"   Hint: Variables
    │                   store values.
    │                   Try again?"
    ▼                       │
[Next Question]   ←─────────┘
    │
    ▼ (After all questions)
[Score Summary Screen]
  - Score out of total (e.g., 7/10)
  - "Mastered" badge if score ≥ 70%
  - "Review Topic" button if score < 70%
  - "Next Topic" button if mastered
        │
        ▼
[Progress Updated in Database]
```

---

### 4.5 Stage 5 — Progress Review

```
[User taps "Progress" in navigation bar]
        │
        ▼
[Progress Screen]
  ┌─────────────────────────────────┐
  │  Overall Progress: 45%          │
  │  ████████░░░░░░░░░░             │
  │                                 │
  │  Topic Breakdown:               │
  │  ✅ Variables        Mastered   │
  │  ✅ Operators        Mastered   │
  │  🔄 Conditionals    In Progress │
  │  🔒 Loops           Not Started │
  │  🔒 Functions       Not Started │
  │  ...                            │
  │                                 │
  │  [Resume Learning →]            │
  └─────────────────────────────────┘
```

---

### 4.6 Complete End-to-End Journey Summary

```
Download App
    ↓
Register / Login
    ↓
Onboarding Tour
    ↓
Home Dashboard
    ↓
Select Topic → Read Lesson → Ask Questions in Chat
    ↓
Complete Practice Questions
    ↓
Score ≥ 70%? → Mark Topic Mastered → Unlock Next Topic
Score < 70%? → Review Hints → Retry Practice
    ↓
View Overall Progress
    ↓
Repeat for all 9 topics
    ↓
All Topics Mastered → Completion Badge Awarded
```

---

## 5. Functional Requirements

Each requirement is labeled with a unique ID, priority (High / Medium / Low), and its source component.

---

### 5.1 User Management

| ID | Requirement | Priority |
|---|---|---|
| FR-UM-01 | The system shall allow a new user to register with a full name, valid email address, password (minimum 8 characters), and self-reported skill level (None / Little / Some). | High |
| FR-UM-02 | The system shall authenticate registered users via email and password, issuing a JWT session token valid for 7 days. | High |
| FR-UM-03 | The system shall store user profile data (name, email, hashed password, skill level, registration date) in the database. | High |
| FR-UM-04 | The system shall allow a logged-in user to view and update their profile name and skill level. | Medium |
| FR-UM-05 | The system shall implement a password reset flow via email OTP (one-time password). | Medium |
| FR-UM-06 | The system shall log the user out by invalidating the JWT token on both client and server sides. | High |
| FR-UM-07 | The system shall restrict all tutoring and progress features to authenticated users only. | High |

---

### 5.2 Lesson and Content System

| ID | Requirement | Priority |
|---|---|---|
| FR-LC-01 | The system shall deliver structured lessons for exactly 9 beginner Python topics: Variables & Data Types, Operators, Conditionals, Loops, Functions, Lists, Dictionaries, Error Types & Debugging, and Basic I/O. | High |
| FR-LC-02 | Each lesson shall contain three sections in this order: (1) a plain-language explanation with a real-world analogy, (2) an annotated code example with line-by-line breakdown, and (3) a key points summary. | High |
| FR-LC-03 | The system shall present lessons in sequential order; a topic is unlocked only after the previous topic is marked as studied. | Medium |
| FR-LC-04 | The system shall allow a user to revisit any previously studied topic at any time. | High |
| FR-LC-05 | Lesson content shall be stored in the backend database and retrieved via API; it shall not be hardcoded in the mobile client. | Medium |
| FR-LC-06 | The system shall display code examples using a monospace font with syntax highlighting in the mobile UI. | Medium |
| FR-LC-07 | Each lesson page shall include a "Mark as Studied" button; tapping it updates the user's progress record and enables the Practice feature for that topic. | High |

---

### 5.3 Rule-Based Engine

| ID | Requirement | Priority |
|---|---|---|
| FR-RB-01 | The rule-based engine shall contain a structured JSON/YAML knowledge base covering all 9 lesson topics, common beginner syntax errors, and at least 3 hint entries per topic. | High |
| FR-RB-02 | The rule engine shall classify incoming user queries into one of four intent categories: concept_question, hint_request, error_explanation, or out_of_scope. | High |
| FR-RB-03 | The rule engine shall match a user's query against rule entries using keyword matching. If a match with confidence ≥ 0.7 is found, the corresponding rule entry shall be used as grounding context. | High |
| FR-RB-04 | The rule engine shall return a pre-authored fallback response for queries classified as out_of_scope (e.g., questions not related to beginner Python topics). | High |
| FR-RB-05 | The rule engine shall provide deterministic hint responses for practice questions, returning a different hint on each of up to 3 failed attempts before revealing the answer. | High |
| FR-RB-06 | Rule entries shall be updatable by an admin without requiring a code redeployment (i.e., stored in editable JSON/YAML files on the server). | Medium |
| FR-RB-07 | The rule engine shall classify Python errors into two categories — syntax errors and logic errors — and return a category-specific explanation for each. | Medium |

---

### 5.4 NLP Engine (GPT-4 Integration)

| ID | Requirement | Priority |
|---|---|---|
| FR-NLP-01 | The NLP module shall send user queries to the GPT-4 API with a carefully structured prompt that includes: the user's query, the current lesson topic context, and a grounding snippet from the rule-base (if available). | High |
| FR-NLP-02 | All GPT-4 prompts shall include a system-level instruction constraining responses to beginner Python topics only, using simple vocabulary suitable for a first-time learner. | High |
| FR-NLP-03 | The NLP module shall receive and parse the GPT-4 API response, extracting the text content from the response payload. | High |
| FR-NLP-04 | If the GPT-4 API returns an error (e.g., rate limit exceeded, network timeout), the system shall fall back to the rule-based engine's stored response for that query category. | High |
| FR-NLP-05 | GPT-4 API calls shall be rate-limited to a maximum of 20 calls per user per hour to manage API cost and prevent abuse. | Medium |
| FR-NLP-06 | The NLP module shall log each API call (timestamp, topic context, query hash — no PII) for monitoring and prompt refinement purposes. | Low |

---

### 5.5 Hybrid Controller

| ID | Requirement | Priority |
|---|---|---|
| FR-HC-01 | The hybrid controller shall serve as the single orchestrator between the rule-based engine and the NLP module; no response shall be returned to the client without passing through it. | High |
| FR-HC-02 | The hybrid controller shall implement the following decision logic: if the rule engine finds a match with confidence ≥ 0.7, use the rule snippet as the grounding context in the GPT-4 prompt; if no rule match is found, send the query to GPT-4 without a grounding snippet but with the lesson topic context only. | High |
| FR-HC-03 | The hybrid controller shall validate GPT-4 responses against a list of banned terms and off-topic markers (e.g., responses mentioning advanced OOP concepts, unrelated topics). If validation fails, the system shall substitute the rule-based fallback response. | High |
| FR-HC-04 | The hybrid controller shall label each response with its source — "rule_based", "nlp_grounded", or "nlp_only" — and include this metadata in the API response payload for logging. | Medium |
| FR-HC-05 | The hybrid controller shall complete its full pipeline (intent detection → rule lookup → NLP call → validation) and return a response within 5 seconds under normal network conditions. | High |

---

### 5.6 Chat Interface

| ID | Requirement | Priority |
|---|---|---|
| FR-CH-01 | The system shall provide a chat screen where users can type free-text questions and receive responses from the hybrid controller. | High |
| FR-CH-02 | The chat screen shall display conversation history in chronological order (user messages on the right, tutor responses on the left) for the duration of a session. | High |
| FR-CH-03 | The system shall display a typing indicator ("Tutor is thinking...") while awaiting a response from the backend. | Medium |
| FR-CH-04 | The system shall allow users to tap suggested quick questions (e.g., "What is a variable?", "Explain for loops") displayed as chips above the input field. | Medium |
| FR-CH-05 | If a user's message is classified as out_of_scope, the tutor shall respond with: "I can only help with beginner Python topics. Try asking about variables, loops, or functions." | High |
| FR-CH-06 | Chat history from previous sessions shall not be persisted; each new session starts with an empty chat history. | Low |

---

### 5.7 Practice and Assessment

| ID | Requirement | Priority |
|---|---|---|
| FR-PA-01 | Each topic shall have a minimum of 5 and a maximum of 10 multiple-choice practice questions with 4 options each. | High |
| FR-PA-02 | The system shall evaluate each submitted answer immediately and display whether it is correct or incorrect. | High |
| FR-PA-03 | For an incorrect answer, the system shall display a rule-based hint specific to the question. A different, progressively revealing hint shall appear on each retry (up to 3 attempts per question). | High |
| FR-PA-04 | After all questions in a topic are attempted, the system shall display a score summary (e.g., "7 out of 10 correct"). | High |
| FR-PA-05 | A topic shall be marked "Mastered" in the user's progress record if the practice score is ≥ 70%. | High |
| FR-PA-06 | If a score is < 70%, the system shall prompt the user to review the lesson and offer a "Retry Practice" option. | Medium |
| FR-PA-07 | Practice questions shall be stored in the backend database and retrieved via API, allowing content updates without a client-side rebuild. | Medium |

---

### 5.8 Progress Tracking

| ID | Requirement | Priority |
|---|---|---|
| FR-PT-01 | The system shall record, per user and per topic: study status (not_started, studied, mastered), last accessed timestamp, and practice score. | High |
| FR-PT-02 | The system shall display a progress screen showing overall completion percentage and per-topic status with visual indicators (e.g., ✅ Mastered, 🔄 In Progress, 🔒 Not Started). | High |
| FR-PT-03 | The home dashboard shall display the last topic the user accessed and their overall progress percentage. | Medium |
| FR-PT-04 | The system shall award a "Python Basics Complete" badge when all 9 topics reach "Mastered" status. | Low |

---

### 5.9 Admin Capabilities (Backend/Phase 2)

| ID | Requirement | Priority |
|---|---|---|
| FR-AD-01 | An admin shall be able to add, update, or delete lesson content via direct edits to the backend content files/database, with changes reflected in the app within 5 minutes. | Medium |
| FR-AD-02 | An admin shall be able to update rule-base entries (JSON/YAML files) without requiring app redeployment. | Medium |
| FR-AD-03 | The backend shall expose an admin API endpoint for retrieving aggregated usage analytics (total users, sessions per day, most-asked topics). | Low |

---

## 6. Non-Functional Requirements

### 6.1 Performance

| ID | Requirement |
|---|---|
| NFR-PF-01 | The hybrid controller shall return a chat response within **5 seconds** under normal network conditions (≥ 3G connectivity). |
| NFR-PF-02 | Lesson content and practice questions shall load within **2 seconds** on a standard mobile connection. |
| NFR-PF-03 | The Flask backend API shall handle at least **50 concurrent requests** without degradation in prototype testing. |
| NFR-PF-04 | GPT-4 API calls shall have a client-side timeout of **8 seconds**; if exceeded, the rule-based fallback shall be returned. |

### 6.2 Reliability

| ID | Requirement |
|---|---|
| NFR-RL-01 | The backend system shall target **≥ 99% uptime** when deployed on a cloud platform. |
| NFR-RL-02 | The system shall degrade gracefully: if the GPT-4 API is unavailable, all responses shall be served from the rule-based engine without crashing the app. |
| NFR-RL-03 | User progress data shall be persisted after every completed action (lesson study, practice submission) to prevent data loss on app close. |

### 6.3 Security

| ID | Requirement |
|---|---|
| NFR-SC-01 | All API communication between the Flutter app and Flask backend shall use **HTTPS (TLS 1.2+)**. |
| NFR-SC-02 | User passwords shall be hashed using **bcrypt** (cost factor ≥ 12) before storage; plaintext passwords shall never be stored. |
| NFR-SC-03 | Session tokens shall be **JWT**, signed with a server-side secret key, and shall expire after 7 days. |
| NFR-SC-04 | The Flask backend shall enforce **input validation and sanitization** on all incoming API fields to prevent injection attacks. |
| NFR-SC-05 | GPT-4 API keys shall be stored as **server-side environment variables** and shall never be embedded in the client-side Flutter app. |
| NFR-SC-06 | The system shall enforce a **rate limit of 20 GPT-4 calls per user per hour** to prevent abuse. |

### 6.4 Usability

| ID | Requirement |
|---|---|
| NFR-US-01 | The mobile UI shall comply with WCAG 2.1 Level AA color contrast guidelines. |
| NFR-US-02 | All navigation actions shall require no more than **3 taps** from the home dashboard to reach any feature. |
| NFR-US-03 | Error messages (network failure, wrong password, etc.) shall be displayed in plain, non-technical language. |
| NFR-US-04 | The app shall support both **Android 8.0+** and **iOS 13+** without platform-specific UI differences. |
| NFR-US-05 | The app shall remain functional and usable on devices with a minimum of **2GB RAM** and a 5-inch screen. |

### 6.5 Scalability

| ID | Requirement |
|---|---|
| NFR-SL-01 | The system architecture shall be modular such that the rule-based engine, NLP module, and hybrid controller can each be updated or replaced independently. |
| NFR-SL-02 | The database schema shall support adding new topics without requiring structural changes to existing tables. |

### 6.6 Maintainability

| ID | Requirement |
|---|---|
| NFR-MT-01 | Rule-base content (JSON/YAML files) shall be updatable by a non-developer admin without modifying Python source code. |
| NFR-MT-02 | Backend code shall follow PEP 8 Python style guidelines and include inline comments for all non-obvious logic. |
| NFR-MT-03 | All Flask API endpoints shall be documented in a README or Postman collection. |

### 6.7 Accessibility and Inclusivity

| ID | Requirement |
|---|---|
| NFR-AC-01 | The app shall be functional on **low-bandwidth connections (≥ 2G / 100 kbps)** by using compressed API payloads and lazy loading of content. |
| NFR-AC-02 | The system shall use simple English vocabulary at a maximum **Grade 7 reading level** in all tutor responses and UI text. |
| NFR-AC-03 | The app shall support responsive layout for screen sizes from 5 inches to 7 inches. |

### 6.8 Logging and Analytics

| ID | Requirement |
|---|---|
| NFR-LA-01 | The backend shall log all API requests with: timestamp, endpoint, user ID (hashed), HTTP status code, and response latency. |
| NFR-LA-02 | The system shall log each GPT-4 API call with: timestamp, topic context, intent category, response source (rule/nlp), and latency — without logging user query text to protect privacy. |
| NFR-LA-03 | The backend shall store aggregated progress analytics (topics studied per day, average scores per topic) for academic evaluation purposes. |

---

## 7. System Architecture

### 7.1 Architecture Style

- **Hybrid Architecture** — Rule-Based Engine + Generative NLP, orchestrated by a Hybrid Controller
- **Client-Server Model** — Flutter mobile client communicating with Flask REST API backend
- **Stateless API** — JWT-authenticated stateless REST endpoints

### 7.2 Component Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                     FLUTTER MOBILE APP                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐  │
│  │  Auth UI  │  │ Lesson UI │  │  Chat UI │  │Progress UI │  │
│  └────┬─────┘  └────┬──────┘  └────┬─────┘  └─────┬──────┘  │
└───────┼─────────────┼──────────────┼───────────────┼─────────┘
        │             │              │               │
        │          HTTPS REST API (JWT Auth)         │
        │             │              │               │
┌───────┼─────────────┼──────────────┼───────────────┼─────────┐
│                     FLASK BACKEND (Python)                    │
│  ┌────┴─────┐  ┌────┴──────┐  ┌───┴──────────────────────┐  │
│  │Auth Module│  │Content API│  │     HYBRID CONTROLLER     │  │
│  └──────────┘  └─────┬─────┘  │  ┌────────────────────┐   │  │
│                       │        │  │ Intent Classifier  │   │  │
│  ┌──────────────────┐ │        │  └────────┬───────────┘   │  │
│  │    DATABASE       │ │        │           │               │  │
│  │  (SQLite/Firebase)│◄┘        │  ┌────────▼───────────┐   │  │
│  │  - users          │          │  │  Rule-Based Engine  │   │  │
│  │  - lessons        │          │  │  (JSON/YAML KB)    │   │  │
│  │  - questions      │          │  └────────┬───────────┘   │  │
│  │  - progress       │          │           │               │  │
│  └──────────────────┘          │  ┌────────▼───────────┐   │  │
│                                 │  │  GPT-4 NLP Module  │   │  │
│                                 │  │  (OpenAI API)      │   │  │
│                                 │  └────────┬───────────┘   │  │
│                                 │           │               │  │
│                                 │  ┌────────▼───────────┐   │  │
│                                 │  │ Validation & Output │   │  │
│                                 │  └────────────────────┘   │  │
│                                 └──────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

### 7.3 Component Descriptions

| Component | Technology | Responsibility |
|---|---|---|
| Flutter Mobile App | Flutter (Dart) | User interface, lesson display, chat, progress view |
| Auth Module | Flask + JWT | Registration, login, token issuance and validation |
| Content API | Flask | Serve lesson content and practice questions from DB |
| Hybrid Controller | Python (Flask service) | Orchestrate rule engine + GPT-4, validate output |
| Rule-Based Engine | Python + JSON/YAML | Intent classification, keyword matching, hint rules |
| GPT-4 NLP Module | OpenAI API (GPT-4) | Generate adaptive natural language explanations |
| Database | SQLite / Firebase | Store users, lessons, questions, progress logs |

---

## 8. API Design

All endpoints are prefixed with `/api/v1/`. All requests and responses use `Content-Type: application/json`. Protected endpoints require `Authorization: Bearer <JWT>` header.

### 8.1 Authentication Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/auth/register` | None | Register a new user |
| POST | `/auth/login` | None | Log in and receive JWT |
| POST | `/auth/logout` | Required | Invalidate user session |
| POST | `/auth/reset-password` | None | Request OTP for password reset |
| POST | `/auth/reset-password/confirm` | None | Confirm OTP and set new password |

**POST /auth/register — Request Body:**
```json
{
  "full_name": "Amina Yusuf",
  "email": "amina@example.com",
  "password": "SecurePass123",
  "skill_level": "none"
}
```

**POST /auth/login — Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": { "id": "u_001", "full_name": "Amina Yusuf", "skill_level": "none" }
}
```

---

### 8.2 Lesson Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/lessons` | Required | Get list of all 9 topics with user's study status |
| GET | `/lessons/:topic_id` | Required | Get full lesson content for a specific topic |
| POST | `/lessons/:topic_id/study` | Required | Mark a topic as studied; updates progress |

**GET /lessons — Response:**
```json
{
  "lessons": [
    { "id": "L01", "title": "Variables & Data Types", "status": "mastered" },
    { "id": "L02", "title": "Operators", "status": "studied" },
    { "id": "L03", "title": "Conditionals", "status": "not_started" }
  ]
}
```

---

### 8.3 Practice Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/practice/:topic_id` | Required | Get practice questions for a topic |
| POST | `/practice/:topic_id/submit` | Required | Submit an answer; receive feedback and hint |
| POST | `/practice/:topic_id/complete` | Required | Submit final score; updates mastery status |

**POST /practice/:topic_id/submit — Request:**
```json
{ "question_id": "Q03", "selected_option": "B", "attempt_number": 1 }
```

**POST /practice/:topic_id/submit — Response:**
```json
{
  "correct": false,
  "hint": "Remember: a variable is like a labelled box that stores a value.",
  "correct_option": null
}
```

---

### 8.4 Chat / Tutor Endpoint

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/chat` | Required | Send a user query; receive hybrid tutor response |

**POST /chat — Request:**
```json
{
  "query": "What is the difference between a list and a dictionary?",
  "current_topic_id": "L06"
}
```

**POST /chat — Response:**
```json
{
  "response": "Great question! A list stores items in order using index numbers (0, 1, 2...), while a dictionary stores items as key-value pairs, like a real dictionary where you look up a word (key) to find its meaning (value).",
  "source": "nlp_grounded",
  "topic_context": "Lists"
}
```

---

### 8.5 Progress Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/progress` | Required | Get full progress summary for the logged-in user |
| GET | `/progress/:topic_id` | Required | Get detailed progress for a specific topic |

---

## 9. Data Models

### 9.1 User

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | String (UUID) | PK, unique | Auto-generated user ID |
| full_name | String | Required, max 100 chars | User's display name |
| email | String | Required, unique, valid email | Login credential |
| password_hash | String | Required | bcrypt-hashed password |
| skill_level | Enum | none / little / some | Self-reported at registration |
| created_at | DateTime | Auto | Account creation timestamp |
| last_login | DateTime | Auto | Last successful login |

### 9.2 Lesson

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | String | PK, e.g. "L01" | Topic identifier |
| title | String | Required | Topic title |
| explanation | Text | Required | Plain-language explanation |
| code_example | Text | Required | Annotated code snippet |
| key_points | Text | Required | Summary bullet points |
| order_index | Integer | Required, unique | Display order in topic list |
| difficulty | Enum | beginner (all topics in v1) | Difficulty level |

### 9.3 PracticeQuestion

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | String | PK | Question identifier |
| topic_id | String | FK → Lesson.id | Associated topic |
| question_text | Text | Required | The question prompt |
| option_a/b/c/d | String | Required | Four answer options |
| correct_option | Enum | A / B / C / D | Correct answer key |
| hint_1 | Text | Required | First hint (after attempt 1) |
| hint_2 | Text | Required | Second hint (after attempt 2) |
| hint_3 | Text | Required | Third hint + reveal answer (after attempt 3) |

### 9.4 UserProgress

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | String | PK | Progress record ID |
| user_id | String | FK → User.id | Owning user |
| topic_id | String | FK → Lesson.id | Associated topic |
| status | Enum | not_started / studied / mastered | Current status |
| practice_score | Integer | 0–100, nullable | Last practice score (%) |
| last_accessed | DateTime | Auto | Last activity on this topic |
| attempt_count | Integer | Default 0 | Number of practice attempts |

### 9.5 ChatLog (Analytics Only — No PII)

| Field | Type | Description |
|---|---|---|
| id | String | Log entry ID |
| user_id_hash | String | SHA-256 hash of user ID (not reversible) |
| topic_context | String | Topic ID at time of query |
| intent_category | Enum | concept_question / hint_request / error_explanation / out_of_scope |
| response_source | Enum | rule_based / nlp_grounded / nlp_only / fallback |
| latency_ms | Integer | Response time in milliseconds |
| timestamp | DateTime | Log timestamp |

---

## 10. NLP Integration (GPT-4)

### 10.1 Model Configuration

| Parameter | Value |
|---|---|
| Model | gpt-4 (OpenAI API) |
| Max Tokens | 300 (to keep responses brief and beginner-friendly) |
| Temperature | 0.3 (low — for consistent, factual explanations) |
| Top-p | 1.0 |
| Timeout | 8 seconds (client-side hard cutoff) |

### 10.2 System Prompt Template

```
You are a friendly Python tutor helping absolute beginners.
You ONLY explain beginner Python concepts: variables, data types, operators,
conditionals, loops, functions, lists, dictionaries, basic errors, and input/output.
Do NOT explain advanced topics (OOP, file handling, external libraries, etc.).
Keep all explanations under 150 words.
Use simple English. Avoid technical jargon.
Use a real-world analogy if helpful.
If the question is unrelated to beginner Python, respond only with:
"I can only help with beginner Python topics."
Current lesson context: {topic_title}
```

### 10.3 User Prompt Template

```
Rule-base grounding (if available): {rule_snippet}

Student question: {user_query}

Please explain this to a complete beginner.
```

### 10.4 Fallback Behavior

| Trigger | Fallback Action |
|---|---|
| GPT-4 API timeout (> 8s) | Return rule-based stored response for detected intent |
| GPT-4 API error (4xx/5xx) | Return rule-based fallback; log error |
| Validation failure (off-topic response) | Return rule-based fallback; log incident |
| No internet connectivity | Return cached rule-based responses for common queries |

---

## 11. Rule-Based Engine Design

### 11.1 Knowledge Base Structure (JSON)

```json
{
  "topic": "variables",
  "rules": [
    {
      "id": "RB-VAR-01",
      "keywords": ["variable", "store", "assign", "what is"],
      "intent": "concept_question",
      "response": "A variable is a named container that stores a value. In Python, you create one by writing: name = value. For example: age = 19 means a variable called 'age' holds the number 19."
    },
    {
      "id": "RB-VAR-02",
      "keywords": ["syntax error", "invalid syntax", "SyntaxError"],
      "intent": "error_explanation",
      "error_type": "syntax",
      "response": "A SyntaxError means Python cannot understand your code because of a typo or missing symbol. Check for missing colons, brackets, or quotes."
    }
  ]
}
```

### 11.2 Intent Classification Logic

```
1. Tokenize and lowercase the user's query.
2. Match against keyword lists in all rule entries.
3. For each match, compute a confidence score = (matched_keywords / total_keywords_in_rule).
4. Select the rule with the highest confidence score.
5. If highest score ≥ 0.7 → classify as that rule's intent, use snippet as grounding.
6. If highest score < 0.7 → classify as concept_question, no grounding snippet.
7. If no keywords match any rule → classify as out_of_scope.
```

### 11.3 Hint Progression Logic

```
Attempt 1 → Return hint_1 (general nudge)
Attempt 2 → Return hint_2 (more specific clue)
Attempt 3 → Return hint_3 (reveal reasoning + correct answer)
```

---

## 12. Hybrid Controller Design

### 12.1 Decision Flow

```
User Query Received
        │
        ▼
[Step 1: Intent Classification (Rule Engine)]
        │
   ┌────┴──────────┐
   │               │
out_of_scope    in_scope
   │               │
   ▼               ▼
Return         [Step 2: Rule KB Lookup]
Fallback            │
Message        ┌────┴──────────────────┐
               │                       │
          Match ≥ 0.7           Match < 0.7
               │                       │
               ▼                       ▼
       Grounded Prompt           Topic-Only Prompt
               │                       │
               └──────────┬────────────┘
                           │
                    [Step 3: GPT-4 Call]
                           │
                    [Step 4: Validation]
                      │           │
                  Pass          Fail
                    │             │
                    ▼             ▼
            Return NLP       Return Rule-Based
            Response         Fallback Response
                    │
                    ▼
              Tag source + Return to Client
```

### 12.2 Validation Checks

| Check | Condition | Action on Failure |
|---|---|---|
| Off-topic check | Response mentions terms outside beginner Python scope | Use rule fallback |
| Length check | Response > 300 words | Truncate or use rule fallback |
| Python accuracy check | Response contradicts Python syntax rules | Use rule fallback |
| Coherence check | Response does not address the query topic | Use rule fallback |

---

## 13. Security Design

| Area | Measure |
|---|---|
| Authentication | JWT tokens, bcrypt password hashing, 7-day expiry |
| Transport | HTTPS (TLS 1.2+) for all client-server communication |
| API Keys | GPT-4 API key stored in server-side `.env` file; never in client |
| Input Validation | All POST body fields validated and sanitized on Flask backend |
| Rate Limiting | 20 GPT-4 calls/user/hour; 100 API requests/user/hour overall |
| Data Privacy | Chat query text is never stored; only hashed user ID and metadata logged |
| No Code Execution | The system does not execute Python code; no sandboxing required |
| User Data | No sensitive personal data beyond name and email; no payment data |

---

## 14. Tools and Technologies

| Component | Tool / Technology | Justification |
|---|---|---|
| Mobile Frontend | Flutter (Dart) | Cross-platform (Android + iOS), mobile-first, rich UI components |
| Backend Framework | Flask (Python) | Lightweight, flexible, ideal for AI service integration |
| AI Model | GPT-4 API (OpenAI) | High-quality generative explanations; suitable for grounded prompting |
| Rule Base | JSON/YAML + Python | Easy to read, edit, and maintain without redeployment |
| Database (Dev) | SQLite | Zero-config, sufficient for prototype and single-server deployment |
| Database (Prod) | Firebase Firestore | Scalable, real-time sync, suitable for mobile apps |
| API Testing | Postman | Industry-standard for REST API functional testing |
| Mobile Testing | Android Emulator (AVD) | Test on virtual Android devices during development |
| Version Control | Git + GitHub | Standard collaborative development practice |
| Deployment (Backend) | Render / Railway | Free-tier cloud Flask deployment for prototype |

---

## 15. Hardware Requirements

### Development Machine

| Spec | Minimum | Recommended |
|---|---|---|
| Processor | Intel Core i3 / AMD Ryzen 3 | Intel Core i5 / AMD Ryzen 5 |
| RAM | 8 GB | 16 GB |
| Storage | 256 GB SSD | 512 GB SSD |
| OS | Windows 10 / macOS 11 / Ubuntu 20.04 | Any of the above |
| Internet | Stable broadband (for GPT-4 API calls) | Stable broadband |

### Target Mobile Device (End User)

| Spec | Minimum |
|---|---|
| OS | Android 8.0 (Oreo) or iOS 13 |
| RAM | 2 GB |
| Storage | 16 GB (app size < 50 MB) |
| Screen | 5-inch display, 720p resolution |
| Internet | 2G / 100 kbps minimum for lesson content; 3G for chat |

---

## 16. Testing Strategy

### 16.1 Functional Testing

| Test Area | Test Cases | Tool |
|---|---|---|
| Auth | Register, login, logout, invalid credentials, token expiry | Postman, manual |
| Lessons | Fetch all topics, fetch single topic, mark as studied | Postman, manual |
| Practice | Submit correct/incorrect answer, hint progression, score calculation | Postman, unit tests |
| Chat | Python query, off-topic query, API timeout fallback | Postman, manual |
| Progress | Progress update on study, mastery update on score ≥ 70% | Postman, unit tests |

### 16.2 Performance Testing

| Metric | Target | Method |
|---|---|---|
| Chat response time | < 5 seconds | Stopwatch test on 3G device |
| Lesson load time | < 2 seconds | Manual timing on emulator |
| API concurrent load | 50 requests without crash | Postman Collection Runner |
| GPT-4 fallback trigger | Fires within 8s timeout | Simulated slow network |

### 16.3 Accuracy Testing

- 50 beginner Python questions evaluated by an expert (supervisor) and by the hybrid system.
- Accuracy score = (correct/acceptable responses) / total questions × 100%.
- Target: ≥ 80% accuracy on concept questions; 100% accuracy on rule-based hint responses.

### 16.4 User Study

| Metric | Measurement Method |
|---|---|
| Clarity of explanations | 5-point Likert scale survey (n ≥ 10 participants) |
| Helpfulness of hints | 5-point Likert scale survey |
| Ease of navigation | Task completion rate (time to find topic and ask question) |
| Perceived learning improvement | Pre/post self-assessment score comparison |
| Overall satisfaction | Net Promoter Score (NPS) question |

**Participant Profile:** AFIT Computer Science freshers or equivalently inexperienced beginners.

---

## 17. Deployment Plan

### 17.1 Development Environment

- Local Flask server (`localhost:5000`)
- Flutter app connected to local backend via USB debugging or local Wi-Fi IP
- SQLite database file stored locally

### 17.2 Prototype Deployment (Phase 1)

| Component | Platform |
|---|---|
| Flask Backend | Render (free tier) or Railway |
| Database | SQLite (local on Render instance) |
| Flutter App | APK sideloaded for testing; not published to Play Store |

### 17.3 Phase 2 Deployment (Post-Evaluation)

| Component | Platform |
|---|---|
| Flask Backend | Render paid tier / AWS EC2 |
| Database | Firebase Firestore |
| Flutter App | Google Play Store (Android) |

### 17.4 CI/CD

Not required for Phase 1 (student project). Manual deployment to Render via GitHub push.

---

## 18. Ethical Considerations

| Concern | Mitigation |
|---|---|
| User data privacy | No query text stored; only hashed user IDs in analytics logs. Explicit privacy notice shown at registration. |
| AI misinformation | Hybrid controller validation + rule-based fallback reduces chance of incorrect explanations reaching the user. |
| Informed consent | Users informed at registration that responses are AI-generated and may occasionally need verification. |
| Algorithmic bias | Rule base authored from open educational resources (W3Schools, Python docs, Think Python); no demographic data used in AI routing. |
| Academic integrity | System designed as a learning aid; it does not solve assignments or write complete programs for users. |
| AI dependency | System encourages understanding, not copying; hints are progressive and explanatory, not answer-providing. |

---

## 19. System Constraints and Limitations

| Constraint | Description |
|---|---|
| No code execution | The system does not run Python code. Code examples are for reading only. This is by design due to infrastructure constraints. |
| Internet required for NLP | The GPT-4 NLP module requires an active internet connection. Offline mode serves rule-based responses only. |
| Beginner topics only | The system covers 9 beginner topics. Advanced Python (OOP, file I/O, libraries) is out of scope for v1. |
| Mobile only (v1) | No web or desktop version in this phase. |
| GPT-4 API cost | API calls are rate-limited (20/user/hour) to manage cost within a student project budget. |
| Limited concurrent users | Prototype infrastructure targets 50 concurrent users. Not suitable for institution-wide deployment without infrastructure upgrade. |
| English only | All content and tutor responses are in English only. |

---

## 20. Assumptions

- Users have basic computer literacy and can operate a smartphone.
- Users have access to an internet connection for generative NLP features.
- Users self-report their skill level honestly during registration.
- The GPT-4 API remains accessible at its current pricing tier during development.
- Lesson content and rule entries will be authored by the researcher and verified by the project supervisor.
- The project is a prototype/MVP; production-grade scalability is a future concern.

---

## 21. Future Improvements

| Feature | Description |
|---|---|
| Voice-based tutor | Allow users to ask questions via speech; tutor responds via text-to-speech |
| Code execution sandbox | Integrate a sandboxed Python interpreter (e.g., Pyodide in WebView) in a v2 update |
| Offline mode | Cache lesson content and rule-based responses for full offline support |
| Advanced topics | Extend curriculum to OOP, file handling, and basic data structures |
| RAG grounding | Replace keyword-matching with Retrieval-Augmented Generation for more accurate rule lookup |
| Multi-language support | Add Hausa/Yoruba/Igbo translations of lesson content for Nigerian language accessibility |
| Web version | Develop a companion web app using React for desktop access |
| Adaptive difficulty | Dynamically adjust lesson pacing and question difficulty based on user performance history |
| Push notifications | Remind users to continue their learning streak |

---

## 22. Glossary

| Term | Definition |
|---|---|
| Hybrid Controller | The Flask service component that orchestrates the rule-based engine and GPT-4 module, validates outputs, and selects the final response. |
| Rule-Based Engine | The deterministic component that uses a JSON/YAML knowledge base of Python rules, error patterns, and hints to provide reliable, pre-authored answers. |
| NLP Module | The generative AI component powered by the GPT-4 API that produces natural language explanations based on a structured prompt. |
| Intent Classification | The process of categorizing a user query into one of four categories: concept_question, hint_request, error_explanation, or out_of_scope. |
| Grounded Prompt | A GPT-4 prompt that includes a rule-base snippet as factual context to constrain and improve the accuracy of the generated response. |
| Mastery | A topic status indicating the user scored ≥ 70% on its practice questions. |
| JWT | JSON Web Token — a compact, signed token used for stateless authentication between the Flutter app and the Flask backend. |
| Flutter | Google's open-source UI toolkit for building natively compiled applications for mobile (Android/iOS) from a single codebase. |
| Flask | A lightweight Python web framework used to build the REST API backend. |
| SQLite | A lightweight, file-based relational database used for prototype data storage. |


