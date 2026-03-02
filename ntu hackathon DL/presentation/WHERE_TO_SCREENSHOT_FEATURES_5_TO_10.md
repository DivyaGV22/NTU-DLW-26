# Where to Find Features 3 and 5–10 for Screenshots

Use this when you don’t know where to look. **Backend must be running** at `http://localhost:8000`.

---

## Feature 3: Bayesian Knowledge Tracing (BKT)

**Best option: dashboard “Topic Proficiencies” chart**

1. Open your **frontend** (e.g. http://localhost:5173 or http://localhost:3004).
2. Select a **student** that has at least a few **interactions** (so the system has computed learning state and topic proficiencies).
3. On the dashboard, scroll to the **“Learning Analytics”** section (below the Learning State card).
4. Find the chart titled **“Topic Proficiencies”** — a **pie chart** with topic names and percentages (e.g. “Mathematics: 75%”, “Physics: 60%”).
5. **Screenshot that chart.**  
   Save as: `screenshots/feature3.png`

**Why this is Feature 3:** Those percentages come from the learning state model, which uses BKT for per-topic mastery. The pie chart is the visual for “probabilistic mastery per topic.”

**If the Topic Proficiencies chart doesn’t appear:**  
The student may have no interactions yet, or the learning state may not have topic data. Record a few interactions (different topics) for that student, wait for the dashboard to refresh, then look again.  
**Fallback:** Open **http://localhost:8000/students/1/state** in the browser and screenshot the JSON (it includes `topic_proficiencies`). Or use **http://localhost:8000/docs** → **GET /students/{student_id}/state** → Try it out → Execute → screenshot the response.

---

## Feature 5: Mistake Intelligence

**There is no dedicated page in the React app.** The feature is in the **API**.

### Option A – Browser (raw JSON)
1. Open in Chrome/Edge:  
   **http://localhost:8000/students/1/mistake-analysis**
2. You’ll see a JSON response (breakdown by error type, insights).
3. Screenshot that page.  
   Save as: `screenshots/feature5.png`

### Option B – Swagger UI (nicer for slides)
1. Open **http://localhost:8000/docs**
2. Find **GET** `/students/{student_id}/mistake-analysis`
3. Click **Try it out** → leave `student_id` as `1` → **Execute**
4. Screenshot the **Response body** section (the JSON).  
   Save as: `screenshots/feature5.png`

**If you get an error:** The student may have no interactions. Add a few interactions for student 1 from the dashboard, then try again.

---

## Feature 6: Study ROI Optimizer

**No UI in the app.** Shown only via the **API**.

### Option A – Browser (raw JSON)
1. Open:  
   **http://localhost:8000/students/1/study-plan/60**
2. You’ll see JSON with topics, time allocation, expected improvement.
3. Screenshot that page.  
   Save as: `screenshots/feature6.png`

### Option B – Swagger UI
1. Open **http://localhost:8000/docs**
2. Find **GET** `/students/{student_id}/study-plan/{time_minutes}`
3. **Try it out** → `student_id`: `1`, `time_minutes`: `60` → **Execute**
4. Screenshot the response.  
   Save as: `screenshots/feature6.png`

**If you get “No topic data”:** Student 1 needs interactions with topics first. Record some from the dashboard, then retry.

---

## Feature 7: Digital Learning Twin

**No UI in the app.** Shown only via the **API**.

### Option A – Browser (raw JSON)
1. Open (use a topic that exists for your student, e.g. from their interactions):  
   **http://localhost:8000/students/1/learning-twin/predict/Mathematics?days=7**  
   If your data uses different topic names, try e.g. `Math`, `Algebra`, or whatever appears in the dashboard.
2. You’ll see JSON with retention/decay prediction.
3. Screenshot that page.  
   Save as: `screenshots/feature7.png`

### Option B – Swagger UI
1. Open **http://localhost:8000/docs**
2. Find **GET** `/students/{student_id}/learning-twin/predict/{topic}`
3. **Try it out** → `student_id`: `1`, `topic`: `Mathematics`, `days`: `7` → **Execute**
4. Screenshot the response.  
   Save as: `screenshots/feature7.png`

---

## Feature 8: Burnout & Inactivity Detection

**Location: main dashboard (React app).**

1. Open your **frontend** (e.g. http://localhost:5173 or http://localhost:3004).
2. Select **Student 1** (or any student).
3. Look at the **right-hand panel**: **“Personalized Recommendations”**.
4. You need a card that is either:
   - **Break** (☕ icon), e.g. “Take a Short Break”, or  
   - **Study** (📚) about inactivity, e.g. “Resume Your Learning Journey”.
5. **Screenshot that recommendation card** (expand it with **+** so reasoning/action items show if you want).  
   Save as: `screenshots/feature8.png`

**If you don’t have a break/inactivity card:**  
- The engine only creates them when conditions are met (e.g. many hours in a short period, or many days inactive).  
- You can still screenshot **any** recommendation card and in the presentation say: “The system also generates break and inactivity recommendations when it detects burnout or long gaps.”

---

## Feature 9: One Dashboard, Full Picture

**Location: same React app – the whole dashboard.**

1. Open the **frontend** and select a student.
2. Make sure the dashboard is fully loaded (state, charts, recommendations, form).
3. Take a **full-page screenshot** of the dashboard:
   - **Left/main area:** Learning State card + Analytics charts + “Record interaction” form.
   - **Right sidebar:** Recommendations list.
4. If one screenshot can’t fit everything, take two and use the one that shows “state + charts + recommendations” as the main slide.  
   Save as: `screenshots/feature9.png`

**Tip:** Use “Capture full page” (browser extension or Win+Shift+S and scroll) so the whole layout is visible.

---

## Feature 10: API-First & Extensible

**Location: API docs (Swagger).**

1. Open in the browser:  
   **http://localhost:8000/docs**
2. You’ll see the **FastAPI Swagger** page with all endpoints listed.
3. Scroll so the list of endpoints is visible (students, interactions, state, dashboard, recommendations, study-plan, learning-twin, mistake-analysis, etc.).
4. Screenshot that **docs page** (the list of operations).  
   Save as: `screenshots/feature10.png`

No need to click into any endpoint unless you want to show request/response details on the slide.

---

## Quick reference

| Feature | Where | Exact URL or place |
|--------|--------|---------------------|
| **5** Mistake Intelligence | API only | http://localhost:8000/students/1/mistake-analysis (or /docs → try that endpoint) |
| **6** Study ROI Optimizer | API only | http://localhost:8000/students/1/study-plan/60 (or /docs → try that endpoint) |
| **7** Digital Learning Twin | API only | http://localhost:8000/students/1/learning-twin/predict/Mathematics?days=7 (or /docs) |
| **8** Burnout & Inactivity | Dashboard (React) | Right sidebar → Recommendations → card with ☕ or “Resume Your Learning Journey” |
| **9** Dashboard | Dashboard (React) | Full dashboard: state + charts + recommendations + form |
| **10** API | Browser | http://localhost:8000/docs (Swagger list of endpoints) |

Put the images in `presentation/screenshots/` as `feature5.png` … `feature10.png` and they’ll show in `slides.html`.
