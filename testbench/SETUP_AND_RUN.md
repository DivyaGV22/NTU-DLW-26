# Step-by-Step Setup and Run Guide (Testbench)

This document gives judges a repeatable way to set up and run the project and verify that it works.

---

## Before You Start

- **Python 3.8+** and **Node.js 16+** (with npm) must be installed.
- Use two terminals: one for the backend, one for the frontend.

---

## Step 1: Get the code

1. Clone the repository (ensure it is **public**):
   ```bash
   git clone <repository-url>
   cd <repository-folder-name>
   ```
2. If the repo root does **not** contain `backend/` and `frontend/` directly, go into the project folder (often named `ntu hackathon DL`):
   ```bash
   cd "ntu hackathon DL"
   ```
   You must be in the folder that contains `backend/` and `frontend/`. This is the **project root** for all steps below.

---

## Step 2: Backend setup and run

1. **Install Python dependencies** (from project root):
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the backend** (from project root):
   ```bash
   cd backend
   python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Verify the backend:**
   - Open in a browser: **http://localhost:8000**  
     You should see something like: `{"message":"Learning Analytics API","version":"1.0.0"}`.
   - Open **http://localhost:8000/docs** to see the interactive API documentation.

4. Leave this terminal running. Use a **second terminal** for the frontend.

---

## Step 3: Frontend setup and run

1. **Open a new terminal** and go to the **project root** (the folder that contains `backend/` and `frontend/`).

2. **Install frontend dependencies:**
   ```bash
   cd frontend
   npm install
   ```

3. **Start the frontend:**
   ```bash
   npm run dev
   ```

4. **Verify the frontend:**
   - Open in a browser: **http://localhost:3000**
   - You should see the Learning Analytics dashboard (student selector, panels, etc.).

5. Leave this terminal running.

---

## Step 4: Load sample data (recommended for testing)

1. **Open a third terminal** (or use the one where you ran `npm run dev` after stopping it temporarily).

2. From the **project root**:
   ```bash
   cd backend
   python utils/sample_data.py
   ```

3. You should see output indicating that sample students and interactions were created.

4. Refresh **http://localhost:3000** and use the student dropdown to select a student. You should see learning state, charts, and recommendations.

---

## Step 5: Basic functional test (manual)

Follow these to confirm main features:

1. **Dashboard**
   - Go to http://localhost:3000.
   - Confirm the page loads and shows the dashboard layout.

2. **Create a student**
   - Use the "+ New Student" (or equivalent) control.
   - Enter a name and email, submit.
   - Confirm the new student appears in the student list/selector.

3. **Record an interaction**
   - Select the student you created.
   - Find the "Record Learning Activity" (or similar) form.
   - Submit one activity (e.g. type: study, topic: Mathematics, duration: 30 minutes, optional score).
   - Confirm the activity is recorded (e.g. in a list or chart).

4. **Learning state**
   - With the same student selected, check that a "Learning state" or similar section shows metrics (e.g. proficiency, engagement).

5. **Recommendations**
   - Open the recommendations panel for that student.
   - Confirm at least one recommendation appears with a short explanation or reasoning.

6. **API docs**
   - Open http://localhost:8000/docs.
   - Try "GET /students" (or "GET /") and confirm you get a valid response.

If all of the above work, the project is running correctly for judging purposes.

---

## Step 6: Optional — quick API checks (curl or browser)

From a terminal (backend must be running):

- Root:
  ```bash
  curl http://localhost:8000/
  ```
  Expected: JSON with `"message"` and `"version"`.

- List students:
  ```bash
  curl http://localhost:8000/students
  ```
  Expected: JSON array (possibly empty before adding students or running sample data).

- Create a student (PowerShell):
  ```powershell
  curl -X POST http://localhost:8000/students -H "Content-Type: application/json" -d "{\"name\":\"Test Student\",\"email\":\"test@example.com\"}"
  ```
  Expected: JSON object with the created student (id, name, email).

- Create a student (bash):
  ```bash
  curl -X POST http://localhost:8000/students -H "Content-Type: application/json" -d '{"name":"Test Student","email":"test@example.com"}'
  ```

---

## Troubleshooting

| Issue | What to do |
|-------|------------|
| `pip install` or `python` not found | Install Python 3.8+ and ensure `python` and `pip` are on PATH. On some systems use `python3` / `pip3`. |
| `npm` not found | Install Node.js 16+ (includes npm). |
| Backend import errors (e.g. `api.main`) | Run uvicorn from inside the `backend/` directory: `cd backend` then `python -m uvicorn api.main:app ...`. |
| Port 8000 already in use | Stop the other process or run backend on another port: `--port 8001`. If you change the port, the frontend still expects 8000 unless you change `frontend/src/services/api.js`. |
| Port 3000 already in use | Change the port in `frontend/vite.config.js` (e.g. `port: 3001`) or stop the other app. |
| Frontend shows "network error" or no data | Ensure the backend is running on http://localhost:8000 and that no firewall is blocking it. |
| No students or recommendations | Run `python utils/sample_data.py` from the `backend/` directory, then refresh the dashboard and select a student. |
| Database errors | The app uses SQLite; the file is created automatically in `backend/`. Ensure the process has write permission in `backend/`. |

---

## Summary checklist

- [ ] Repository cloned and project root identified (`backend/` and `frontend/` visible).
- [ ] `pip install -r requirements.txt` run from project root.
- [ ] Backend started from `backend/` with uvicorn; http://localhost:8000 and http://localhost:8000/docs work.
- [ ] `npm install` and `npm run dev` run in `frontend/`; http://localhost:3000 loads.
- [ ] (Optional) Sample data loaded via `python utils/sample_data.py` in `backend/`.
- [ ] Dashboard loads; can create student, record interaction, see state and recommendations.

Once all items are checked, the project is ready for evaluation.
