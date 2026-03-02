# NTU Hackathon Submission — AI-Powered Learning Analytics & Recommendation System

**Repository:** Please ensure this repository is **public** so judges can access it.

This repository contains the complete source code for an intelligent learning analytics system that models students' evolving learning state and provides personalized, actionable recommendations.

---

## What's Inside

| Item | Description |
|------|-------------|
| **Source code** | Full backend (FastAPI + ML) and frontend (React + Vite) in the project folder |
| **README** | This file — setup, dependencies, and how to run |
| **testbench/** | Test materials and a **step-by-step setup and run guide** for judges (see [testbench/SETUP_AND_RUN.md](testbench/SETUP_AND_RUN.md)) |

---

## Repository Structure

After cloning, you will see:

```
├── README.md                 ← You are here
├── testbench/
│   ├── SETUP_AND_RUN.md      ← Step-by-step guide for testing (for judges)
│   └── ...                   ← Helper scripts and test info
└── ntu hackathon DL/         ← Main project (backend + frontend)
    ├── backend/
    ├── frontend/
    ├── requirements.txt
    └── ...
```

**Project root** = the folder that contains `backend/` and `frontend/`.  
If you cloned the full repo, that is **`ntu hackathon DL`**. Run this first when needed:

```bash
cd "ntu hackathon DL"
```

---

## Prerequisites

- **Python 3.8+** with `pip`
- **Node.js 16+** and **npm**
- A terminal (PowerShell, CMD, or bash)

---

## Dependencies

### Backend (Python)

- FastAPI, Uvicorn, Pydantic  
- SQLAlchemy, Pandas, NumPy  
- scikit-learn, SciPy (ML and analytics)  
- See **`ntu hackathon DL/requirements.txt`** for the full list.

### Frontend (Node)

- React 18, React Router  
- Vite, Axios, Recharts, date-fns, lucide-react  
- See **`ntu hackathon DL/frontend/package.json`**.

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <repo-folder>
```

If the repo contains the outer folder, go into the project:

```bash
cd "ntu hackathon DL"
```

### 2. Backend setup

From the **project root** (folder containing `backend/` and `frontend/`):

```bash
pip install -r requirements.txt
cd backend
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

Leave this terminal open. You should see the API running.

- **API base:** http://localhost:8000  
- **Interactive docs:** http://localhost:8000/docs  

### 3. Frontend setup (new terminal)

From the **project root**:

```bash
cd frontend
npm install
npm run dev
```

- **Dashboard:** http://localhost:3000  

### 4. (Optional) Sample data

To preload sample students and interactions:

From the **project root**:

```bash
cd backend
python utils/sample_data.py
```

Then refresh the dashboard and select a student to see state and recommendations.

---

## How to Run (Quick Reference)

| Step | Command (from project root) |
|------|-----------------------------|
| Start backend | `cd backend && python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000` |
| Start frontend | `cd frontend && npm run dev` |
| Optional: sample data | `cd backend && python utils/sample_data.py` |

**Windows:** You can use the provided scripts from the project root:

- `start_backend.bat` — start backend  
- `start_frontend_simple.bat` — start frontend (run after `npm install` in `frontend`)  

---

## Using the Application

1. Open **http://localhost:3000** in a browser.  
2. **Create a student** (e.g. "+ New Student") with name and email.  
3. **Record learning activities** (study, quiz, assignment, video, reading) with topic, duration, and optional score.  
4. **View learning state** — proficiency, engagement, velocity, risk.  
5. **View recommendations** — personalized suggestions with explanations.  
6. **Mark recommendations** as viewed or completed as needed.

---

## Testing and Judging

For a **step-by-step setup and run document** and testbench materials, see:

- **[testbench/SETUP_AND_RUN.md](testbench/SETUP_AND_RUN.md)** — intended for judges to set up and run the project and verify behaviour.

---

## Troubleshooting

- **Backend import errors:** Run backend commands from the `backend/` directory (e.g. `cd backend` then `python -m uvicorn api.main:app ...`).  
- **Database:** SQLite DB is created automatically on first run (`backend/learning_analytics.db`).  
- **Port in use:** Use `--port 8001` for the API or change the frontend port in `frontend/vite.config.js`.  
- **Frontend cannot reach API:** Ensure the backend is running on port 8000; the frontend uses `http://localhost:8000` for API calls.  
- **CORS:** Backend allows `localhost:3000` and `localhost:5173`; if you use another port, you may need to add it in `backend/api/main.py`.

---

## License and Contact

Part of the NTU Hackathon submission. For questions, use the repository’s issue or contact mechanism.
