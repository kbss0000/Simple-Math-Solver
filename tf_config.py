"""
TensorFlow configuration module - must be imported FIRST before any TensorFlow imports
"""
import os
import sys

# Set TensorFlow environment variables BEFORE any imports
os.environ['TF_NUM_INTEROP_THREADS'] = '1'
os.environ['TF_NUM_INTRAOP_THREADS'] = '1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

# Disable TensorFlow optimizations that might cause threading issues
os.environ['TF_DISABLE_SEGMENT_REDUCTION_OP'] = '1'
os.environ['TF_DISABLE_MKL'] = '1'

# Force single-threaded execution
if sys.platform == 'darwin':  # macOS
    os.environ['OMP_NUM_THREADS'] = '1'
    os.environ['MKL_NUM_THREADS'] = '1'

print("✅ TensorFlow environment configured for single-threaded execution")

