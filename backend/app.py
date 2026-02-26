from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse
from PIL import Image, ImageEnhance, ImageFilter
import io
import cv2
import numpy as np

# Initialize FastAPI application
app = FastAPI(title="MedTech Phase Simulator")

# Enable CORS.
# For simplicity, all origins are allowed.
# In production, this should be restricted to the frontend domain (e.g., GitHub Pages URL).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def process_image(img: Image.Image, phase: str) -> Image.Image:
    """
    Apply a simulated medical phase transformation to the input image.

    Parameters:
        img (PIL.Image.Image): Input image.
        phase (str): Selected phase ("arterial" or "venous").

    Returns:
        PIL.Image.Image: Processed image.
    """

    # Ensure image is in RGB format
    img = img.convert("RGB")

    if phase == "arterial":
        # Simulate arterial phase by increasing image contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.6)  # Adjustable contrast factor

        # Optional slight sharpening for a more pronounced effect
        img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=120, threshold=3))
        return img

    if phase == "venous":
        # Simulate venous phase by applying Gaussian smoothing
        return img.filter(ImageFilter.GaussianBlur(radius=2.0))

    # Defensive programming: raise error if phase is invalid
    raise ValueError("Invalid phase")


@app.get("/health")
def health():
    """
    Simple health-check endpoint to verify that the API is running.
    """
    return {"ok": True}


@app.post("/process")
async def process(file: UploadFile = File(...), phase: str = Form(...)):
    """
    Receive an uploaded image and a selected phase.
    Perform image processing on the backend and return the processed image as PNG.
    """

    try:
        # Normalize and validate phase input
        phase = (phase or "").strip().lower()
        if phase not in ("arterial", "venous"):
            return JSONResponse(
                {"success": False, "error": "phase must be arterial or venous"},
                status_code=400,
            )

        # Read uploaded file content
        content = await file.read()
        if not content:
            return JSONResponse(
                {"success": False, "error": "empty file"},
                status_code=400,
            )

        # Load image from bytes
        img = Image.open(io.BytesIO(content))

        # Process image according to selected phase
        processed_img = process_image(img, phase)

        # Convert processed image to PNG and return as binary response
        buffer = io.BytesIO()
        processed_img.save(buffer, format="PNG")

        return Response(
            content=buffer.getvalue(),
            media_type="image/png"
        )

    except Exception as e:
        # Return error details for debugging purposes
        return JSONResponse(
            {"success": False, "error": str(e)},
            status_code=400,
        )

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    """
    Detects whether the image contains a liver-like region using a simple heuristic:
    grayscale -> blur -> threshold -> largest contour -> bounding box.
    No deep learning is used (as requested).
    """
    try:
        content = await file.read()
        if not content:
            return JSONResponse({"success": False, "error": "empty file"}, status_code=400)

        # Decode bytes -> OpenCV image (BGR)
        nparr = np.frombuffer(content, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            return JSONResponse({"success": False, "error": "invalid image"}, status_code=400)

        h, w = img.shape[:2]

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Simple threshold (Otsu) to separate bright/dark regions
        # Detection logic: we assume the largest contour after thresholding
        # may represent an organ region; if it's large enough, we mark detected=True.
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        detected = False
        confidence = 0.0
        bounding_box = None

        if contours:
            largest = max(contours, key=cv2.contourArea)
            area = float(cv2.contourArea(largest))

            # Heuristic threshold: at least ~5% of the image area
            area_ratio = area / float(w * h)
            if area_ratio >= 0.05:
                x, y, bw, bh = cv2.boundingRect(largest)
                detected = True

                # Confidence as a bounded function of area ratio (simple, stable)
                confidence = min(max(area_ratio, 0.0), 1.0)

                bounding_box = {
                    "x": int(x),
                    "y": int(y),
                    "width": int(bw),
                    "height": int(bh),
                }

        return {
            "detected": detected,
            "confidence": round(float(confidence), 2),
            "bounding_box": bounding_box,
        }

    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=400)