# InfraScore - DevOps Readiness Platform

InfraScore is a comprehensive, interactive quiz platform designed to prepare engineers for DevOps interviews and certifications. It features real-world scenarios, AI-powered grading, and a dynamic dashboard to track progress.

## 🏗️ Architecture Overview

The application is containerized using Docker and consists of three main services:

1.  **Backend (Flask)**: The core API and application logic (`backend/`).
2.  **Database (PostgreSQL)**: Stores user profiles, quiz questions, and history.
3.  **Admin (pgAdmin)**: Web interface for database management.

---

## 🧠 How the Backend Works

The backend is built with **Python (Flask)** and serves both the API endpoints and the HTML frontend.

### Key Components:

*   **`backend/app.py`**: The main entry point. Initializes the Flask app, connects to the database, and defines all routes.
    *   **Routes**: Handles pages (`/`, `/dashboard`, `/quiz`) and API endpoints (`/api/quiz/submit-answer`, `/api/history/all`).
    *   **State Management**: Uses **Server-Side Sessions** (filesystem-based) to securely store active quiz state (current question, user answers, score) without exposing it to the client.

*   **`backend/ai_grader.py`**: A specialized module that connects to **Google's Gemini API**.
    *   It receives the user's answer and the question context.
    *   It evaluates the answer (0-10 score) and provides detailed feedback.
    *   It handles API quotas and errors gracefully (falling back to simpler logic if needed).

---

## ❓ Where Do the Questions Come From?

The questions are sourced from a curated dataset and loaded into the database during the container startup or manual seeding process.

### The Question Pipeline:

1.  **Raw Data**: The project includes a massive repository of raw interview questions (PDFs, Markdown) located in:
    *   `database/datasets/Raw-Questions-Repo/`

2.  **Processed Dataset**: These raw files were processed into a structured JSON file:
    *   `database/datasets/final_quiz_dataset.json`

3.  **Database Loading (Seeding)**:
    The primary script responsible for loading these questions into PostgreSQL is **`backend/seed_db.py`**.

    *   **Lines 40-46**: The script looks for the JSON dataset file (`/app/final_quiz_dataset.json` inside the container).
        ```python
        json_file_path = '/app/final_quiz_dataset.json'
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as f:
                data = json.load(f)
        ```
    *   **Lines 50-76**: It iterates through the JSON data and maps it to the database schema.
    *   **Lines 93-108**: It executes an SQL `INSERT` command for each question.

    *Alternative (Hardcoded Fallback)*: If the JSON file is missing, the script falls back to a hardcoded list defined in **Lines 84-89**.

---

## 🚀 Setup & Usage

### Prerequisites
*   Docker & Docker Compose
*   Gemini API Key (for AI grading)

### Starting the Project
1.  **Configure Environment**:
    Edit the `.env` file to add your API Key:
    ```bash
    GEMINI_API_KEY=your_key_here
    ```

2.  **Run with Docker**:
    ```bash
    docker-compose up --build
    ```
    This command builds the backend image, starts PostgreSQL, and seeds the database automatically.

3.  **Access the App**:
    *   **App**: `http://localhost:5001`
    *   **pgAdmin**: `http://localhost:8080`

### Useful Commands
*   **Restart Backend** (reload code/config):
    ```bash
    docker-compose restart flask-app
    ```
*   **Re-seed Database** (reset questions):
    ```bash
    docker exec -it devops_quiz_app python backend/seed_db.py
    ```
*   **Check AI Models**:
    ```bash
    docker exec -it devops_quiz_app python backend/check_models.py
    ```

---

## 📂 Key File Structure

```
InfraScore/
├── backend/
│   ├── app.py                # Main Application Logic
│   ├── ai_grader.py          # AI Integration Logic
│   ├── seed_db.py            # Database Seeder (Questions Source)
│   └── check_db.py           # Diagnostic Utility
├── frontend/
│   ├── templates/            # HTML Files (Dashboard, Quiz, History)
│   └── static/               # Assets (Favicon, CSS)
├── database/
│   └── datasets/             # Raw and Processed Question Data
├── docker-compose.yml        # Service Orchestration
└── .env                      # Secrets & Config
```
