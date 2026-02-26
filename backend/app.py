from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse
from PIL import Image, ImageEnhance, ImageFilter
import io

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