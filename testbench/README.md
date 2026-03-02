# Testbench

This folder contains materials for judges to set up and test the project.

## Contents

| File | Description |
|------|-------------|
| **SETUP_AND_RUN.md** | **Step-by-step setup and run guide** — use this to install dependencies, start backend and frontend, load sample data, and verify the application. |
| **README.md** | This file — overview of the testbench. |
| **verify_backend.ps1** | Windows PowerShell script to check if the backend API is reachable (optional). |
| **verify_backend.sh** | Bash script to check if the backend API is reachable on Linux/macOS (optional). |
| **API_ENDPOINTS.txt** | Reference list of main API endpoints and sample request bodies. |

## Quick start for judges

1. Open **[SETUP_AND_RUN.md](SETUP_AND_RUN.md)** and follow the steps in order.
2. Use the checklist at the end to confirm the project runs correctly.
3. Optionally run `verify_backend.ps1` (Windows) or `verify_backend.sh` (Linux/macOS) after starting the backend to confirm the API responds.

## Requirements

- Python 3.8+, Node.js 16+, two terminals (one for backend, one for frontend).
- All commands in SETUP_AND_RUN.md assume you are in the **project root** (the folder that contains `backend/` and `frontend/`).
