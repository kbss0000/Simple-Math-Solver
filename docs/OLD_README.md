# Handwritten Equation Solver - Streamlit App

A CNN-based handwritten math equation solver that recognizes and solves equations from images.

## Project Overview

This project uses a Convolutional Neural Network (CNN) to:
1. **Recognize** handwritten math symbols (digits 0-9, +, -, ×, ÷)
2. **Segment** equation images into individual symbols
3. **Solve** the recognized equations

## Model Architecture

- **Input**: 32×32 grayscale images
- **Output**: 14 classes (digits 0-9 + add, sub, mul, div)
- **Architecture**: 
  - 3 Conv2D layers (32, 32, 64 filters)
  - MaxPooling layers
  - 2 Dense layers (120, 84 units)
  - Output layer with softmax activation

## Input & Output

### Input:
- **Training**: Images from `data/data/dataset/` organized by label folders
- **Inference**: Single handwritten equation image (PNG/JPG)

### Output:
- **Training**: Trained model (`model.h5`) + Label encoder (`label_encoder.pkl`)
- **Inference**: 
  - Recognized equation string (e.g., "2+3")
  - Calculated result (e.g., "5")

## Files Structure

```
Handwritten/
├── streamlit_app.py          # Main Streamlit application
├── inference_utils.py         # Utilities for recognition and solving
├── train_model.py             # Model training script
├── requirements.txt           # Dependencies
├── model.h5                   # Trained model (generated after training)
├── label_encoder.pkl          # Label encoder (generated after training)
├── data/
│   └── data/
│       └── dataset/          # Training dataset
│           ├── 0/
│           ├── 1/
│           ├── ...
│           ├── add/
│           ├── sub/
│           ├── mul/
│           └── div/
└── README.md
```

## Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

Or activate your virtual environment:
```bash
source venv/bin/activate  # On macOS/Linux
pip install -r requirements.txt
```

2. **Train the model** (if `model.h5` doesn't exist):
```bash
python train_model.py
```
*Note: Training takes time (100 epochs). You can stop early with Ctrl+C if needed.*

## Running the App

### Local Development

```bash
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`

### Usage

1. **Upload Image**: Click "Browse files" and select a handwritten equation image
2. **Solve**: Click "🔮 Solve Equation"
3. **View Results**: 
   - Recognized equation string
   - Calculated solution
   - Symbol detection visualization

## Training the Model

If you need to train or retrain the model:

```bash
python train_model.py
```

This will:
- Load images from `data/data/dataset/`
- Preprocess images (grayscale, threshold, resize)
- Train CNN for 100 epochs
- Save `model.h5` and `label_encoder.pkl`

**Training Time**: Approximately 15-30 minutes depending on your system

## Model Performance

Expected performance after training:
- **Training Accuracy**: ~95%+
- **Test Accuracy**: ~90%+

## Deployment

### Streamlit Cloud

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repository
4. Set main file: `streamlit_app.py`
5. Ensure `model.h5` and `label_encoder.pkl` are in repository
6. Deploy!

### Requirements for Deployment

- ✅ Model file (`model.h5`) - must be committed to repo
- ✅ Label encoder (`label_encoder.pkl`) - must be committed to repo
- ✅ All dependencies in `requirements.txt`
- ✅ Dataset NOT needed (only model files)

## Testing

Run the quick test:
```bash
python quick_test.py
```

This checks:
- Model file existence
- Dataset structure
- Dependencies

## Known Issues & Fixes

### Issue: Model not found
**Solution**: Train the model first: `python train_model.py`

### Issue: Import errors
**Solution**: Install dependencies: `pip install -r requirements.txt`

### Issue: Poor recognition accuracy
**Solutions**:
- Ensure clear, well-spaced handwriting
- Use images with good contrast
- Retrain model with more epochs if needed

## Limitations

- Currently supports: digits 0-9, +, -, ×, ÷
- Works best with clear, spaced handwriting
- Complex equations may need better segmentation
- No parentheses support yet

## Future Enhancements

- Support for parentheses
- Support for more operations (power, sqrt, etc.)
- Better segmentation for complex layouts
- Batch processing of multiple equations

## License

Educational purposes only.

