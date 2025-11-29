"""
Handwritten Equation Solver - API
"""
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import cv2
import numpy as np
import re
from imutils.contours import sort_contours
import imutils
import base64
from io import BytesIO
from PIL import Image
import tensorflow as tf

tf.get_logger().setLevel('ERROR')

app = FastAPI(title="Equation Solver API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model at startup
print("Loading model...")
model = tf.keras.models.load_model('model.h5', compile=False)
print("Model loaded!")

# Label mapping
CLASSES = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "add", "div", "mul", "sub"]
SYMBOL_MAP = {'add': '+', 'sub': '-', 'mul': '×', 'div': '÷'}


def preprocess_symbol(image):
    if len(image.shape) == 3:
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        img_gray = image.copy()
    
    threshold_img = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    threshold_img = cv2.resize(threshold_img, (32, 32))
    threshold_img = threshold_img / 255.0
    threshold_img = np.expand_dims(threshold_img, axis=-1)
    
    return threshold_img


def segment_equation(image):
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()
    
    binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    
    cnts = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
    if cnts:
        cnts = sort_contours(cnts, method="left-to-right")[0]
    
    symbols = []
    boxes = []
    
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        
        if w < 10 or h < 10:
            continue
        
        padding = 5
        y_start = max(0, y - padding)
        y_end = min(image.shape[0], y + h + padding)
        x_start = max(0, x - padding)
        x_end = min(image.shape[1], x + w + padding)
        
        symbol_img = gray[y_start:y_end, x_start:x_end]
        
        boxes.append({"x": int(x), "y": int(y), "w": int(w), "h": int(h)})
        symbols.append(symbol_img)
    
    return boxes, symbols


def correct_symbol_by_geometry(symbol, box):
    if symbol not in ['+', '-']:
        return symbol
    
    w = box["w"]
    h = box["h"]
    if h == 0:
        return symbol
    
    aspect_ratio = w / h
    
    if aspect_ratio > 1.5:
        return '-'
    elif aspect_ratio < 1.2:
        return '+'
    
    return symbol


def solve_equation(equation_str):
    try:
        eq = equation_str.replace('×', '*').replace('÷', '/').replace(' ', '')
        eq = eq.split('=')[0].replace('?', '')
        
        if not re.match(r'^[\d\+\-\*/\(\)\.\s]+$', eq):
            return None, "Invalid equation format"
        
        result = eval(eq)
        
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        
        return result, None
    except Exception as e:
        return None, str(e)


def process_image(image_array):
    if len(image_array.shape) == 3 and image_array.shape[2] == 3:
        img_cv = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
    else:
        img_cv = image_array
    
    boxes, symbol_images = segment_equation(img_cv)
    
    if not symbol_images:
        return {"error": "No symbols detected in image"}
    
    processed = [preprocess_symbol(s) for s in symbol_images]
    X = np.array(processed)
    
    predictions = model.predict(X, verbose=0)
    predicted_indices = np.argmax(predictions, axis=1)
    
    symbols = []
    for i, idx in enumerate(predicted_indices):
        label = CLASSES[idx]
        symbol = SYMBOL_MAP.get(label, label)
        if i < len(boxes):
            symbol = correct_symbol_by_geometry(symbol, boxes[i])
        symbols.append(symbol)
    
    equation_str = ''.join(symbols)
    result, error = solve_equation(equation_str)
    
    return {
        "equation": equation_str,
        "result": result,
        "symbols_count": len(symbols),
        "boxes": boxes,
        "error": error
    }


@app.get("/")
async def root():
    return {"status": "ok", "message": "Equation Solver API"}


@app.post("/api/predict")
async def predict(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(BytesIO(contents))
        image_array = np.array(image)
        
        result = process_image(image_array)
        return JSONResponse(content={"data": [result]})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/predict")
async def predict_json(data: dict):
    """Handle Gradio-style base64 image input"""
    try:
        if "data" not in data or not data["data"]:
            return JSONResponse(content={"error": "No data provided"}, status_code=400)
        
        image_data = data["data"][0]
        
        # Handle base64 encoded image
        if isinstance(image_data, str) and image_data.startswith("data:"):
            # Remove data URL prefix
            base64_str = image_data.split(",")[1]
            image_bytes = base64.b64decode(base64_str)
            image = Image.open(BytesIO(image_bytes))
            image_array = np.array(image)
        else:
            return JSONResponse(content={"error": "Invalid image format"}, status_code=400)
        
        result = process_image(image_array)
        return JSONResponse(content={"data": [result]})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
