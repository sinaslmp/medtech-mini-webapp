# Full-Stack MedTech Mini Web-App

[![Live Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-blue?style=flat-square&logo=github)](https://sinaslmp.github.io/medtech-mini-webapp/)
[![Backend](https://img.shields.io/badge/Backend-Hugging%20Face%20Spaces-yellow?style=flat-square&logo=huggingface)](https://sinaslmp-medtech-phase-backend.hf.space)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Vue](https://img.shields.io/badge/Vue-3-4FC08D?style=flat-square&logo=vue.js&logoColor=white)](https://vuejs.org)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?style=flat-square&logo=docker&logoColor=white)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

A full-stack MedTech mini web-app that simulates arterial and venous image phases — deployed on **GitHub Pages** (frontend) and **Hugging Face Spaces** (backend).

---

## Features

| Phase | Effect |
|---|---|
| **Arterial** | Increases contrast + sharpening (simulates arterial phase enhancement) |
| **Venous** | Applies Gaussian smoothing (simulates venous phase diffusion) |

- Side-by-side comparison of original and processed images
- Supports JPG / PNG uploads
- Fully Dockerized for local development
- CI/CD via GitHub Actions (automatic deploy to GitHub Pages)

---

## Live Demo

| Service | URL |
|---|---|
| Frontend | [sinaslmp.github.io/medtech-mini-webapp](https://sinaslmp.github.io/medtech-mini-webapp/) |
| Backend API | [sinaslmp-medtech-phase-backend.hf.space](https://sinaslmp-medtech-phase-backend.hf.space) |
| API Docs | [/docs](https://sinaslmp-medtech-phase-backend.hf.space/docs) |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Vue 3 + Vite (GitHub Pages) |
| Backend | FastAPI + Pillow (Hugging Face Spaces) |
| Containerization | Docker |
| CI/CD | GitHub Actions |

---

## How to Use

1. Open the [live frontend](https://sinaslmp.github.io/medtech-mini-webapp/)
2. Upload a JPG or PNG image
3. Select a phase: **Arteriosa** (arterial) or **Venosa** (venous)
4. Click **Elabora immagine**
5. View the original and processed images side-by-side

---

## Local Development

### Prerequisites

- Python ≥ 3.10
- Node.js ≥ 18
- Docker (optional)

### Run with Docker

```bash
docker compose up --build
```

Frontend: http://localhost:5173  
Backend API: http://localhost:8000  
API Docs: http://localhost:8000/docs

### Run Manually

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

---

## API Reference

### `POST /process`

Process an uploaded image with the selected phase.

**Request:** `multipart/form-data`

| Field | Type | Values |
|---|---|---|
| `file` | File | JPG or PNG image |
| `phase` | string | `"arterial"` or `"venous"` |

**Response:** PNG image binary (`image/png`)

### `GET /health`

Returns `{"ok": true}` — used for uptime monitoring.

---

## Project Structure

```
medtech-mini-webapp/
├── backend/
│   ├── app.py              # FastAPI routes + image processing
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   └── ...                 # Vue 3 + Vite app
├── .github/workflows/      # GitHub Actions CI/CD
└── README.md
```

---

## License

MIT — free to use and modify.
