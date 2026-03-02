# How to Start the Servers

The servers need to be started manually in separate terminal windows. Follow these steps:

## Step 1: Start Backend Server

**Open Terminal/Command Prompt Window 1:**

```bash
cd "C:\Users\divya\OneDrive\Documents\ntu hackathon\backend"
python -m uvicorn api.main:app --reload
```

**You should see:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**Keep this window open!**

---

## Step 2: Start Frontend Server

**Open a NEW Terminal/Command Prompt Window 2:**

```bash
cd "C:\Users\divya\OneDrive\Documents\ntu hackathon\frontend"
npm run dev
```

**You should see:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

**Keep this window open!**

---

## Step 3: Open in Browser

Once both servers are running, open:
- **Dashboard**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

---

## Troubleshooting

### If port 8000 is already in use:
```bash
python -m uvicorn api.main:app --reload --port 8001
```
Then update `frontend/src/services/api.js` to use port 8001.

### If port 3000 is already in use:
Vite will automatically use the next available port (like 3001).

### If you see "Module not found" errors:
- Backend: Run `pip install -r requirements.txt` again
- Frontend: Run `cd frontend && npm install` again

### If backend won't start:
Check for errors in the terminal. Common issues:
- Database file locked: Close any other programs using it
- Import errors: Make sure you're in the `backend` folder when running

### If frontend won't start:
- Make sure Node.js is installed: `node --version`
- Reinstall dependencies: `cd frontend && rm -rf node_modules && npm install`

