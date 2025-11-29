# ⚠️ CRITICAL: How to Run Without Crashes

## The Problem

When you click "Solve Equation", TensorFlow tries to load the model and crashes Streamlit due to a **mutex lock error on macOS**. This happens even with background processes.

## ✅ The Solution: Run Manually with Environment Variables

**You MUST run Streamlit manually in a terminal with environment variables set BEFORE starting.**

### Step 1: Stop Any Running Streamlit

```bash
pkill -9 -f streamlit
```

### Step 2: Open a NEW Terminal Window

**Don't run it in background** - you need to see what's happening.

### Step 3: Run This Exact Command

```bash
cd /Users/happy/Documents/Code/Handwritten

export TF_NUM_INTEROP_THREADS=1
export TF_NUM_INTRAOP_THREADS=1
export TF_CPP_MIN_LOG_LEVEL=2

./venv/bin/streamlit run streamlit_app.py
```

### Step 4: Keep Terminal Open

**Keep this terminal window open** while using the app. Don't close it!

### Step 5: Test the App

1. Wait for: `Local URL: http://localhost:8501`
2. Open that URL in your browser
3. Upload an image
4. Click "🔮 Solve Equation"
5. The model should load without crashing

## Alternative: Use the Script

I've created a script that does this automatically:

```bash
cd /Users/happy/Documents/Code/Handwritten
./run_streamlit.sh
```

## Why This Works

Setting `TF_NUM_INTEROP_THREADS=1` and `TF_NUM_INTRAOP_THREADS=1` **before** Python starts tells TensorFlow to use single-threaded mode, which avoids the mutex lock error on macOS.

**If you set these AFTER Python/Streamlit starts, they won't take effect!**

## What Happens if You Don't Do This

- ✅ Streamlit starts fine
- ✅ You can upload images
- ❌ **When you click "Solve Equation"**, Streamlit crashes with connection error
- This is because TensorFlow tries to load the model with multi-threading and triggers the mutex error

## Verify It's Working

After running with env vars:

1. Streamlit should start without errors
2. You can access `http://localhost:8501`
3. Upload an image
4. Click "Solve Equation"
5. You should see "Loading model (first time only)..."
6. Model loads successfully
7. Results appear

If it still crashes, check the terminal output for error messages and share them with me.

## Quick Copy-Paste

Just copy and paste this entire block:

```bash
cd /Users/happy/Documents/Code/Handwritten
export TF_NUM_INTEROP_THREADS=1
export TF_NUM_INTRAOP_THREADS=1
export TF_CPP_MIN_LOG_LEVEL=2
./venv/bin/streamlit run streamlit_app.py
```

**That's it!** This should fix the connection error.

