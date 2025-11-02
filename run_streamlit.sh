#!/bin/bash
# Run Streamlit with proper TensorFlow environment variables
# Uses Python 3.11 (compatible with TensorFlow on macOS)

cd "$(dirname "$0")"

# Set TensorFlow environment variables BEFORE starting Streamlit
# This is critical to avoid the mutex error
export TF_NUM_INTEROP_THREADS=1
export TF_NUM_INTRAOP_THREADS=1
export TF_CPP_MIN_LOG_LEVEL=2

# Use Python 3.11 virtual environment
if [ -d "venv311" ]; then
    echo "✅ Using Python 3.11 environment (venv311)"
    source venv311/bin/activate
else
    echo "⚠️ Python 3.11 environment not found, using default venv"
    source venv/bin/activate
fi

echo ""
echo "Starting Streamlit with TensorFlow threading configured..."
echo "Python version: $(python --version)"
echo "Environment variables set:"
echo "  TF_NUM_INTEROP_THREADS=1"
echo "  TF_NUM_INTRAOP_THREADS=1"
echo ""
echo "Keep this terminal open while using the app!"
echo ""

# Run Streamlit with XSRF protection disabled for local development
streamlit run streamlit_app.py --server.enableXsrfProtection false
