# How to Run the Handwritten Equation Solver

## Quick Start

### Step 1: Open Terminal
Open a terminal window on your Mac.

### Step 2: Navigate to Project Directory
```bash
cd /Users/happy/Documents/Code/Handwritten
```

### Step 3: Activate Virtual Environment (Optional)
```bash
source venv/bin/activate
```

Or use the venv Python directly (recommended):
```bash
./venv/bin/streamlit run streamlit_app.py
```

### Step 4: Start Streamlit
Run this command:
```bash
./venv/bin/streamlit run streamlit_app.py
```

### Step 5: Open in Browser
After a few seconds, you should see:
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
```

**Click on the URL or copy-paste `http://localhost:8501` into your browser.**

## Alternative: Use the Script

You can also use the provided script:

```bash
cd /Users/happy/Documents/Code/Handwritten
chmod +x run_streamlit.sh
./run_streamlit.sh
```

## What You'll See

1. **Streamlit Welcome Screen** (first time only)
   - You can skip by pressing Enter

2. **Your App Interface**
   - Title: "📝 Handwritten Equation Solver"
   - Upload button for images
   - Instructions in sidebar

3. **To Test:**
   - Click "Browse files"
   - Select one of the test images:
     - `test_simple_add.png` (tests 2+3)
     - `test_simple_sub.png` (tests 5-2)
     - `test_simple_mul.png` (tests 4×3)
     - `test_simple_div.png` (tests 8÷2)
   - Click "🔮 Solve Equation"
   - See the results!

## Important Notes

### ✅ Keep Terminal Open
- **Don't close the terminal window** while using the app
- The app runs in the terminal - closing it stops the app

### ✅ First Time Loading
- When you upload your first image and click "Solve"
- You'll see "Loading model (first time only)..."
- This is normal - the model loads only when needed
- Subsequent solves will be faster

### ✅ Stopping the App
- Press `Ctrl+C` in the terminal to stop Streamlit
- Or close the terminal window

## Troubleshooting

### Problem: "Connection error" in browser
**Solution:**
1. Check if Streamlit is running in terminal
2. Look for the URL `http://localhost:8501`
3. Make sure terminal window is still open
4. Try refreshing the browser page

### Problem: Streamlit won't start
**Solution:**
1. Make sure you're in the right directory:
   ```bash
   cd /Users/happy/Documents/Code/Handwritten
   ```

2. Check if virtual environment exists:
   ```bash
   ls venv/bin/streamlit
   ```

3. If not, install Streamlit:
   ```bash
   ./venv/bin/pip install streamlit
   ```

### Problem: "Model not found" error
**Solution:**
1. Check if model files exist:
   ```bash
   ls -lh model.h5 label_encoder.pkl
   ```

2. If missing, train the model:
   ```bash
   ./venv/bin/python train_model.py
   ```
   (This takes 15-30 minutes)

### Problem: Port 8501 already in use
**Solution:**
1. Use a different port:
   ```bash
   ./venv/bin/streamlit run streamlit_app.py --server.port 8502
   ```
2. Then open `http://localhost:8502` in browser

## Full Command Reference

### Start Streamlit (Default Port 8501)
```bash
cd /Users/happy/Documents/Code/Handwritten
./venv/bin/streamlit run streamlit_app.py
```

### Start Streamlit (Custom Port)
```bash
cd /Users/happy/Documents/Code/Handwritten
./venv/bin/streamlit run streamlit_app.py --server.port 8502
```

### Start Streamlit (No Browser Auto-Open)
```bash
cd /Users/happy/Documents/Code/Handwritten
./venv/bin/streamlit run streamlit_app.py --server.headless true
```

## Files Needed

Before running, make sure these files exist:
- ✅ `streamlit_app.py` - The main app
- ✅ `inference_utils.py` - Helper functions
- ✅ `model.h5` - Trained model (1.9 MB)
- ✅ `label_encoder.pkl` - Label encoder
- ✅ `requirements.txt` - Dependencies

All these should be in `/Users/happy/Documents/Code/Handwritten/`

## Quick Test

1. Run: `./venv/bin/streamlit run streamlit_app.py`
2. Wait for: `Local URL: http://localhost:8501`
3. Open browser to that URL
4. Upload `test_simple_add.png`
5. Click "🔮 Solve Equation"
6. Should see: Recognized "2+3", Result "5"

**That's it! You're ready to go! 🎉**

