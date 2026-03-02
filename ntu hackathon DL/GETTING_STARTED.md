# Getting Started - Step by Step Guide

Follow these steps to run the Learning Analytics system on your computer.

## Prerequisites Check

Before starting, make sure you have:
- ✅ **Python 3.8 or higher** installed
  - Check: Open terminal/command prompt and type `python --version`
  - If not installed: Download from [python.org](https://www.python.org/downloads/)
  
- ✅ **Node.js 16 or higher** installed
  - Check: Open terminal/command prompt and type `node --version`
  - If not installed: Download from [nodejs.org](https://nodejs.org/)

- ✅ **pip** (Python package manager)
  - Usually comes with Python, check with `pip --version`

---

## Step 1: Install Backend Dependencies

1. **Open a terminal/command prompt** in the project folder

2. **Install Python packages:**
   ```bash
   pip install -r requirements.txt
   ```
   
   This will install all required Python libraries (FastAPI, pandas, scikit-learn, etc.)
   
   ⚠️ **Note**: If you get permission errors, try:
   - Windows: `python -m pip install -r requirements.txt`
   - Mac/Linux: `pip3 install -r requirements.txt` or `sudo pip install -r requirements.txt`

---

## Step 2: Start the Backend Server

1. **Navigate to the backend folder:**
   ```bash
   cd backend
   ```

2. **Start the API server:**
   ```bash
   python -m uvicorn api.main:app --reload
   ```
   
   You should see output like:
   ```
   INFO:     Uvicorn running on http://127.0.0.1:8000
   INFO:     Application startup complete.
   ```

3. **Keep this terminal window open!** The server needs to keep running.

4. **Verify it's working:**
   - Open your web browser
   - Go to: http://localhost:8000/docs
   - You should see the API documentation page

---

## Step 3: (Optional) Generate Sample Data

In a **new terminal window** (keep the backend server running):

1. **Navigate to backend folder:**
   ```bash
   cd backend
   ```

2. **Run the sample data script:**
   ```bash
   python utils/sample_data.py
   ```
   
   This creates a sample student with 50 learning interactions for testing.

---

## Step 4: Install Frontend Dependencies

1. **Open a new terminal window** (keep backend running)

2. **Navigate to the frontend folder:**
   ```bash
   cd frontend
   ```

3. **Install Node.js packages:**
   ```bash
   npm install
   ```
   
   This may take a few minutes. It downloads React and other frontend libraries.

---

## Step 5: Start the Frontend Dashboard

1. **Still in the frontend folder**, start the development server:
   ```bash
   npm run dev
   ```
   
   You should see output like:
   ```
   VITE v5.x.x  ready in xxx ms
   ➜  Local:   http://localhost:3000/
   ```

2. **Open your browser** and go to: http://localhost:3000

3. **You should see the Learning Analytics Dashboard!** 🎉

---

## Step 6: Using the System

### Create Your First Student

1. Click the **"+ New Student"** button
2. Enter a name (e.g., "John Doe")
3. Enter an email (e.g., "john@example.com")
4. Click **"Create Student"**

### Record Learning Activities

1. Scroll down to the **"Record Learning Activity"** section
2. Fill in the form:
   - **Activity Type**: Choose from Study, Quiz, Assignment, Video, or Reading
   - **Topic**: Enter a subject (e.g., "Mathematics", "Physics")
   - **Duration**: How many minutes you spent
   - **Score**: (Optional) For quizzes/assignments, enter 0.0 to 1.0
   - **Difficulty**: Easy, Medium, or Hard
   - **Engagement**: Use the slider (0-100%)
3. Click **"Record Activity"**

### View Your Learning Analytics

- **Learning State Card**: See your proficiency, engagement, and learning velocity
- **Analytics Charts**: View score trends, topic distribution, and study time
- **Recommendations Panel**: Get AI-powered personalized recommendations

### Explore Recommendations

1. Look at the **Recommendations Panel** on the right side
2. Click the **"+"** button on any recommendation to expand it
3. Read the **reasoning** and **supporting data**
4. Follow the **action items**
5. Mark recommendations as **Viewed** or **Completed** when done

---

## Quick Reference: Running Commands

### Terminal 1 - Backend Server
```bash
cd backend
python -m uvicorn api.main:app --reload
```
**Keep this running!**

### Terminal 2 - Frontend Dashboard
```bash
cd frontend
npm run dev
```
**Keep this running!**

### Terminal 3 - (Optional) Sample Data
```bash
cd backend
python utils/sample_data.py
```

---

## Troubleshooting

### Backend Won't Start

**Problem**: `ModuleNotFoundError` or import errors
- **Solution**: Make sure you installed dependencies: `pip install -r requirements.txt`
- **Solution**: Make sure you're in the `backend` folder when running the command

**Problem**: Port 8000 already in use
- **Solution**: Change the port: `python -m uvicorn api.main:app --reload --port 8001`
- **Solution**: Or close the program using port 8000

**Problem**: Database errors
- **Solution**: The database is created automatically. Delete `learning_analytics.db` if corrupted and restart

### Frontend Won't Start

**Problem**: `npm: command not found`
- **Solution**: Install Node.js from [nodejs.org](https://nodejs.org/)

**Problem**: `Module not found` errors
- **Solution**: Run `npm install` again in the frontend folder

**Problem**: Can't connect to API
- **Solution**: Make sure the backend server is running on port 8000
- **Solution**: Check that you see the API docs at http://localhost:8000/docs

**Problem**: CORS errors
- **Solution**: The backend is configured for localhost:3000. Make sure frontend runs on port 3000

### Dashboard Shows No Data

**Problem**: No students or recommendations showing
- **Solution**: Create a student first using "+ New Student"
- **Solution**: Record some learning activities
- **Solution**: Or run the sample data script: `python backend/utils/sample_data.py`

---

## What's Next?

1. **Explore the API**: Visit http://localhost:8000/docs to see all available endpoints
2. **Record More Activities**: The more data you add, the better the recommendations
3. **Try Different Scenarios**:
   - Record activities with low scores → See practice recommendations
   - Stop recording for a few days → See inactivity recommendations
   - Record high scores consistently → See acceleration recommendations
4. **Check Learning State**: Watch how your metrics change over time

---

## Need Help?

- Check the **README.md** for feature descriptions
- Check **SOLUTION_OVERVIEW.md** for architecture details
- Review the API documentation at http://localhost:8000/docs
- Check browser console (F12) for frontend errors
- Check terminal output for backend errors

---

## Summary Checklist

- [ ] Installed Python dependencies (`pip install -r requirements.txt`)
- [ ] Started backend server (`cd backend && python -m uvicorn api.main:app --reload`)
- [ ] Verified backend at http://localhost:8000/docs
- [ ] Installed frontend dependencies (`cd frontend && npm install`)
- [ ] Started frontend server (`npm run dev`)
- [ ] Opened dashboard at http://localhost:3000
- [ ] Created a student profile
- [ ] Recorded some learning activities
- [ ] Viewed recommendations and analytics

**You're all set! Happy learning! 🎓**

