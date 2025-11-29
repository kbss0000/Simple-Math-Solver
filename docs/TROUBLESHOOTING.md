# Troubleshooting Guide

## If Streamlit Won't Start

The error `mutex lock failed: Invalid argument` is a known TensorFlow issue on macOS. Here's how to fix it:

### Option 1: Use a Different Port

Try running on a different port:

```bash
cd /Users/happy/Documents/Code/Handwritten
./venv/bin/streamlit run streamlit_app.py --server.port 8502
```

### Option 2: Run in Terminal Manually

Instead of background processes, run it directly in your terminal:

```bash
cd /Users/happy/Documents/Code/Handwritten
source venv/bin/activate
streamlit run streamlit_app.py
```

**Keep the terminal window open** - don't close it while using the app.

### Option 3: Use Threading Fix

The model now loads lazily (only when you upload an image), which should help. But if you still see errors:

1. Make sure you're using Python 3.8-3.11 (not 3.12+)
2. Try reinstalling TensorFlow: `pip install --upgrade tensorflow`
3. Use TensorFlow 2.13 or earlier instead of 2.15+

### Option 4: Check Your Environment

```bash
cd /Users/happy/Documents/Code/Handwritten
./venv/bin/python --version  # Should be 3.8-3.11
./venv/bin/pip list | grep tensorflow  # Check version
```

## Model Loading Issues

If the model won't load:

1. Check files exist:
   ```bash
   ls -lh model.h5 label_encoder.pkl
   ```

2. Test model loading:
   ```bash
   ./venv/bin/python -c "from tensorflow.keras.models import load_model; m = load_model('model.h5'); print('OK')"
   ```

## Still Not Working?

The app uses lazy loading now - the model only loads when you upload an image. This should avoid startup issues.

Try:
1. Open http://localhost:8501 in your browser
2. Upload an image
3. The model will load when you click "Solve Equation"

