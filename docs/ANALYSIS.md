# Handwritten Equation Solver - Analysis

## Project Overview
This is a **CNN-based handwritten math equation solver** that:
1. Recognizes individual math symbols and digits (0-9, +, -, ×, ÷)
2. Processes handwritten equation images
3. Solves the recognized equations

## Model Architecture
- **Type**: CNN (Convolutional Neural Network)
- **Input**: 32x32 grayscale images (1 channel)
- **Output**: 14 classes (digits 0-9 + add, sub, mul, div)
- **Architecture**:
  - 3 Conv2D layers (32, 32, 64 filters)
  - MaxPooling after each conv layer
  - 2 Dense layers (120, 84 units)
  - Final Dense layer with 14 outputs (softmax)

## Input & Output

### Inputs:
1. **Training**: Images from `data/data/dataset/` organized by label folders
   - Folders: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, add, sub, mul, div
   - Images: PNG/JPG files of handwritten symbols

2. **Inference** (for Streamlit):
   - Single equation image (handwritten math equation)
   - Example: Image showing "2 + 3 = ?"

### Outputs:
1. **Training Phase**: Trained model (`model.h5`)
2. **Inference Phase**: 
   - Recognized equation string (e.g., "2 + 3")
   - Calculated result (e.g., "5")

## Workflow

### Training Phase:
1. Load images from dataset folders
2. Preprocess: Convert to grayscale → Threshold → Resize to 32x32
3. Label encode: Convert folder names to numeric labels
4. Train CNN model with data augmentation
5. Save model as `model.h5`

### Inference Phase (for Streamlit):
1. **Image Upload**: User uploads equation image
2. **Preprocessing**: Convert to grayscale, threshold, resize
3. **Segmentation**: Split equation image into individual symbols (THIS IS MISSING IN NOTEBOOK!)
4. **Recognition**: Use model to predict each symbol
5. **Post-processing**: Combine symbols into equation string
6. **Evaluation**: Parse and solve the equation
7. **Display**: Show recognized equation and result

## Issues Found in Notebook:

1. **Incomplete Inference Pipeline**: 
   - Notebook shows training but inference code is broken
   - Missing image segmentation step (critical for equations with multiple symbols)

2. **Model File Missing**: 
   - Need to train model first or have pre-trained model

3. **No Equation Solving Logic**: 
   - Notebook doesn't show how to evaluate the equation after recognition

4. **Hardcoded Paths**: 
   - Uses Kaggle-specific paths (`/kaggle/input/`)

## Requirements for Streamlit Deployment:

1. **Pre-trained model** (`model.h5`)
2. **Image preprocessing pipeline**
3. **Symbol segmentation** (contour detection)
4. **Symbol recognition** (model inference)
5. **Equation parsing and solving**
6. **UI**: File uploader, image display, results

## Files Needed:
- `model.h5` (trained model)
- `app.py` (Streamlit app)
- `requirements.txt` (dependencies)
- Inference utilities (image processing, segmentation, solving)

