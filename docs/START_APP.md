# How to Start the Streamlit App

## Quick Start

Run this command in your terminal:

```bash
cd /Users/happy/Documents/Code/Handwritten
./venv/bin/streamlit run streamlit_app.py
```

Or use the provided script:

```bash
cd /Users/happy/Documents/Code/Handwritten
./run_streamlit.sh
```

## What to Expect

1. Streamlit will start and show output like:
   ```
   You can now view your Streamlit app in your browser.
   Local URL: http://localhost:8501
   ```

2. Open your browser and go to: **http://localhost:8501**

3. Upload a handwritten equation image and click "Solve Equation"!

## Troubleshooting

If you see "Connection error":
- Make sure Streamlit is running in your terminal
- Check if port 8501 is already in use
- Try restarting: Press `Ctrl+C` to stop, then run the command again

## Files Ready

- ✅ Model: `model.h5` (1.9 MB)
- ✅ Label Encoder: `label_encoder.pkl`
- ✅ Streamlit App: `streamlit_app.py`
- ✅ All dependencies installed

Your app is ready to use!

