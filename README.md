# Full-Stack MedTech Mini Web-App

This project is a minimal full-stack medical imaging simulator built with Vue (frontend) and FastAPI (backend).

It includes:

- **Arterial phase simulation** (contrast enhancement)
- **Venous phase simulation** (Gaussian smoothing)
- **AI-powered organ detection (liver region heuristic)**

---

# Branches

## main
Original phase simulator (as initially submitted).

- Frontend: https://sinaslmp.github.io/medtech-mini-webapp/
- Backend: https://sinaslmp-medtech-phase-backend.hf.space

---

## feature/organ-detection
Extended version including AI-powered organ detection.

- Frontend: https://sinaslmp.github.io/medtech-mini-webapp-organ-detection/
- Backend: https://sinaslmp-medtech-phase-backend-organ-detection.hf.space

---

# New Endpoint: POST /analyze

This endpoint performs simple liver-region detection using classical computer vision (no deep learning).

### Detection Logic

1. Convert image to grayscale  
2. Apply Gaussian blur  
3. Apply Otsu thresholding  
4. Extract largest contour  
5. If contour area exceeds a heuristic threshold, classify as detected  

### Example Response

```json
{
  "detected": true,
  "confidence": 0.87,
  "bounding_box": {
    "x": 120,
    "y": 95,
    "width": 310,
    "height": 280
  }
}
```

---

## How to Use (Feature Branch)

### Organ Detection

1. Upload a JPG or PNG medical image.
2. Click **Analyze**.
3. The backend will process the image using classical computer vision.
4. A JSON result will appear below the image including:
   - `detected` (true/false)
   - `confidence` score
   - `bounding_box` coordinates (if detected)

---

### Phase Simulation (Original Feature)

1. Upload a JPG or PNG image.
2. Select a phase:
   - **Arterial** → increases contrast
   - **Venous** → applies Gaussian smoothing
3. Click **Elabora immagine**.
4. View the original and processed images side-by-side.

---