# Setup Guide: Python 3.11 for TensorFlow

## Quick Setup

### Step 1: Install Python 3.11

**If you have Homebrew:**
```bash
brew install python@3.11
```

**If you don't have Homebrew:**
1. Download Python 3.11 from: https://www.python.org/downloads/release/python-3119/
2. Install the macOS installer
3. Make sure to check "Add Python to PATH" during installation

### Step 2: Create New Virtual Environment

```bash
cd /Users/happy/Documents/Code/Handwritten

# Use Python 3.11
python3.11 -m venv venv311

# Or if python3.11 is not in PATH:
# /usr/local/bin/python3.11 -m venv venv311
```

### Step 3: Activate New Environment

```bash
source venv311/bin/activate

# Verify Python version
python --version  # Should show Python 3.11.x
```

### Step 4: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 5: Run Streamlit

```bash
streamlit run streamlit_app.py
```

**Or with environment variables:**

```bash
export TF_NUM_INTEROP_THREADS=1
export TF_NUM_INTRAOP_THREADS=1
streamlit run streamlit_app.py
```

## Alternative: Use pyenv (if installed)

```bash
# Install Python 3.11
pyenv install 3.11.9

# Set local version
cd /Users/happy/Documents/Code/Handwritten
pyenv local 3.11.9

# Create venv
python -m venv venv311
source venv311/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Verify It Works

After setting up Python 3.11:

```bash
python --version  # Should be 3.11.x
python -c "import tensorflow; print(tensorflow.__version__)"  # Should work
streamlit run streamlit_app.py  # Should start without mutex errors
```

## Troubleshooting

### "python3.11: command not found"

Try:
```bash
/usr/local/bin/python3.11 -m venv venv311
# or
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11 -m venv venv311
```

### Still getting mutex error

Make sure:
1. You're using Python 3.11 (check: `python --version`)
2. You've activated the new venv: `source venv311/bin/activate`
3. You set environment variables before running Streamlit

