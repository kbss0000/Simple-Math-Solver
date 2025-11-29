# Fix: Connection Error When Clicking "Solve Equation"

## Problem
When you click "🔮 Solve Equation", Streamlit crashes with:
- "Connection error"
- `mutex lock failed: Invalid argument`

This is a **known TensorFlow issue on macOS** - the model loading triggers a threading crash.

## Solutions

### Solution 1: Run with Environment Variables (Recommended)

Open a **new terminal** and run:

```bash
cd /Users/happy/Documents/Code/Handwritten

export TF_NUM_INTEROP_THREADS=1
export TF_NUM_INTRAOP_THREADS=1
export TF_CPP_MIN_LOG_LEVEL=2

./venv/bin/streamlit run streamlit_app.py
```

**Keep this terminal window open** while using the app.

### Solution 2: Use the Safe Runner Script

```bash
cd /Users/happy/Documents/Code/Handwritten
./run_streamlit_safe.sh
```

### Solution 3: Alternative - Use TensorFlow 2.13 or Earlier

The mutex issue is worse in TensorFlow 2.15+. Try downgrading:

```bash
cd /Users/happy/Documents/Code/Handwritten
./venv/bin/pip install "tensorflow<2.14"
./venv/bin/streamlit run streamlit_app.py
```

### Solution 4: Use Python 3.10 or 3.11

TensorFlow on macOS works better with Python 3.10-3.11 than 3.12+:

```bash
# If you have Python 3.10 or 3.11 installed:
python3.10 -m venv venv310
source venv310/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

### Solution 5: Run Model in Separate Process (Advanced)

If nothing else works, we might need to load the model in a separate process and communicate via API. This is more complex but avoids the threading issue entirely.

## Why This Happens

- **TensorFlow threading bug on macOS**: The model loading triggers a mutex lock error
- **Streamlit's threading model**: Conflicts with TensorFlow's threading
- **macOS-specific issue**: This doesn't happen on Linux/Windows

## Workaround for Now

If you need to test the model immediately:

1. **Don't use the web interface** - Use a simple Python script instead:

```bash
cd /Users/happy/Documents/Code/Handwritten
./venv/bin/python -c "
from inference_utils import recognize_equation
from tensorflow.keras.models import load_model
import joblib
import cv2

# Load model (outside Streamlit)
model = load_model('model.h5', compile=False)
encoder = joblib.load('label_encoder.pkl')

# Test with an image
img = cv2.imread('test_simple_add.png')
result, error = recognize_equation(model, encoder, img)
print('Equation:', result['equation'])
print('Result:', result['result'])
"
```

## Check Current Status

To see if Streamlit is currently running:

```bash
ps aux | grep streamlit
lsof -ti:8501
```

To restart:

```bash
cd /Users/happy/Documents/Code/Handwritten
pkill -9 -f streamlit
export TF_NUM_INTEROP_THREADS=1 TF_NUM_INTRAOP_THREADS=1
./venv/bin/streamlit run streamlit_app.py
```

## Expected Behavior

- ✅ Streamlit starts successfully
- ✅ You can upload an image
- ❌ **When you click "Solve Equation"**, Streamlit crashes
- This is because model loading triggers the TensorFlow mutex error

The fix is to run Streamlit with the environment variables set, which should prevent the crash.

## Next Steps

1. Try Solution 1 (run with export commands)
2. If that doesn't work, try Solution 3 (downgrade TensorFlow)
3. If still failing, consider Solution 5 (separate process)

Let me know which solution works for you!

