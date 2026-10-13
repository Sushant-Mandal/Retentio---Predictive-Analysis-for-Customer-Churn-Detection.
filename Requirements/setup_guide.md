# How to Start the Retentio Project

This guide explains how to set up and run both the frontend and backend of the Retentio project.

## Prerequisites
- Node.js (v18+ recommended)
- `pnpm` (Node package manager)
- Python 3.9+

---

## 1. Starting the Frontend (Vite + React)

The frontend is located in the `retentio` directory.

1. Open a terminal and navigate to the `retentio` folder:
   ```bash
   cd retentio
   ```
2. Install the dependencies using `pnpm`:
   ```bash
   pnpm install
   ```
3. Start the development server:
   ```bash
   pnpm run dev
   ```
4. Once the server starts, it will provide a local URL (e.g., `http://localhost:5173`). Open this URL in your browser to view the website.

---

## 2. Starting the Backend (FastAPI + Python)

The backend is located in the `backend` directory.

1. Open a new terminal and navigate to the `backend` folder:
   ```bash
   cd backend
   ```
2. (Optional but recommended) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up the environment variables:
   - Copy `.env.example` to `.env`
   - Fill in the required environment variables (like MongoDB URI).
5. Start the backend development server using Uvicorn:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
6. The backend API will be available at `http://localhost:8000`. You can view the API documentation at `http://localhost:8000/docs`.

---

## Seeing the Website

Make sure both the **frontend** and **backend** servers are running simultaneously in separate terminal windows.

Once both are running, go to the frontend URL (usually `http://localhost:5173`) in your web browser to interact with the Retentio application.
