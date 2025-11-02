"""
Streamlit App for Handwritten Equation Solver
"""

# Import TensorFlow configuration FIRST - before any other imports
try:
    import tf_config  # Sets environment variables before TensorFlow imports
except ImportError:
    # Fallback: set env vars manually
    import os

    os.environ["TF_NUM_INTEROP_THREADS"] = "1"
    os.environ["TF_NUM_INTRAOP_THREADS"] = "1"
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"

import os

import streamlit as st
import cv2
import numpy as np
from PIL import Image
from pathlib import Path
from sklearn.preprocessing import LabelEncoder

# DON'T import TensorFlow here - import only when needed
import pickle

# Import utilities
try:
    from inference_utils import recognize_equation, segment_equation, preprocess_symbol
except ImportError:
    st.error("Please ensure inference_utils.py is in the same directory")
    st.stop()

# Page config
st.set_page_config(
    page_title="Handwritten Equation Solver", page_icon="📝", layout="wide"
)

# Custom CSS
st.markdown(
    """
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .result-box {
        padding: 1.5rem;
        border-radius: 10px;
        background: #f0f2f6;
        margin: 1rem 0;
    }
    </style>
""",
    unsafe_allow_html=True,
)


@st.cache_resource
def load_model_and_encoder():
    """Load trained model and label encoder - TensorFlow imported here only"""
    try:
        # Import TensorFlow only when this function is called
        # Try both import styles for different TensorFlow versions
        try:
            from tensorflow.keras.models import load_model
            import tensorflow as tf
        except ImportError:
            try:
                from keras.models import load_model
                import tensorflow as tf
            except ImportError:
                import tensorflow as tf
                load_model = tf.keras.models.load_model
        
        # Configure TensorFlow BEFORE any operations
        # This is critical for avoiding mutex issues
        try:
            tf.config.threading.set_inter_op_parallelism_threads(1)
            tf.config.threading.set_intra_op_parallelism_threads(1)
        except:
            pass  # Ignore if already set or not available
        
        # Disable eager execution warnings
        try:
            tf.get_logger().setLevel('ERROR')
        except:
            pass
        
        # Disable TensorFlow warnings
        import warnings
        import os
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
        warnings.filterwarnings('ignore')
        
    except ImportError as e:
        return None, None, f"TensorFlow not installed: {str(e)}"
    except Exception as e:
        return None, None, f"Error importing TensorFlow: {str(e)}"

    model_path = Path("model.h5")
    encoder_path = Path("label_encoder.pkl")

    if not model_path.exists():
        return (
            None,
            None,
            "Model file (model.h5) not found. Please train the model first.",
        )

    # if not encoder_path.exists():
    #     return None, None, "Label encoder file (label_encoder.pkl) not found."

    try:
        # Load encoder first (safer, no TensorFlow needed)
        classes = [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "add",
            "div",
            "mul",
            "sub",
        ]
        label_encoder = LabelEncoder()
        label_encoder.fit(classes)

        # Now load model with all safeguards
        # Use compile=False to avoid issues
        model = load_model(str(model_path), compile=False)

        # Don't compile - not needed for inference
        # The model should work fine without recompiling

        return model, label_encoder, None
    except SystemExit:
        # Don't let SystemExit propagate
        raise
    except Exception as e:
        import traceback

        error_msg = f"Error loading model: {str(e)}\n{traceback.format_exc()}"
        return None, None, error_msg


# Initialize model variables (loaded lazily)
model = None
label_encoder = None
model_error = None

# Main title
st.markdown(
    '<h1 class="main-header">📝 Handwritten Equation Solver</h1>',
    unsafe_allow_html=True,
)
st.markdown("---")


# Load model only when needed
def get_model():
    """Lazy load model on first use"""
    global model, label_encoder, model_error
    if model is None and model_error is None:
        model, label_encoder, model_error = load_model_and_encoder()
    return model, label_encoder, model_error


# Don't load model at startup - load only when needed
# Check if files exist first
model_path = Path("model.h5")
encoder_path = Path("label_encoder.pkl")

if not model_path.exists() or not encoder_path.exists():
    st.error("⚠️ Model files not found")
    st.info("""
    **To train the model:**
    1. Ensure dataset is in `data/data/dataset/`
    2. Run: `python train_model.py`
    3. Wait for training to complete (will take time)
    4. Refresh this page
    """)
    st.stop()

# Sidebar
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    **How it works:**
    1. Upload a handwritten equation image
    2. Model segments the image into symbols
    3. Recognizes each symbol (digits 0-9, +, -, ×, ÷)
    4. Solves the equation

    **Supported operations:**
    - Addition (+)
    - Subtraction (-)
    - Multiplication (×)
    - Division (÷)

    **Note:** Upload clear, well-spaced handwritten equations
    """)

# Main content
st.header("📤 Upload Equation Image")

uploaded_file = st.file_uploader(
    "Choose an image file",
    type=["png", "jpg", "jpeg"],
    help="Upload a handwritten math equation image",
)

if uploaded_file is not None:
    # Display uploaded image
    image = Image.open(uploaded_file)
    img_array = np.array(image)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📷 Uploaded Image")
        st.image(image, caption="Your equation", use_container_width=True)

    # Process image
    if st.button("🔮 Solve Equation", type="primary", use_container_width=True):
        with st.spinner("Processing equation..."):
            try:
                # Model loading is done in subprocess - just check if files exist
                model_path = Path("model.h5")
                if not model_path.exists():
                    st.error("⚠️ Model file (model.h5) not found")
                    st.info("Please train the model first or ensure model.h5 exists")
                    st.stop()
                
                # Initialize dummy model/encoder for API compatibility
                # They're not actually used - subprocess handles everything
                if model is None:
                    model = "dummy"  # Placeholder
                if label_encoder is None:
                    from sklearn.preprocessing import LabelEncoder
                    classes = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "add", "div", "mul", "sub"]
                    label_encoder = LabelEncoder()
                    label_encoder.fit(classes)

                # Convert PIL to OpenCV format
                if len(img_array.shape) == 3:
                    img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
                else:
                    img_cv = img_array.copy()

                # recognize_equation uses subprocess - never loads TensorFlow in main process
                result, error = recognize_equation(model, label_encoder, img_cv)

                if error:
                    st.error(f"Error: {error}")
                elif result:
                    with col2:
                        st.subheader("✅ Recognition Results")

                        # Display recognized equation
                        st.markdown('<div class="result-box">', unsafe_allow_html=True)
                        st.markdown(f"**Recognized Equation:**")
                        st.code(result["equation"], language=None)

                        if result["result"] is not None:
                            st.markdown(f"**Solution:**")
                            st.success(f"**{result['result']}**")

                        if result["error"]:
                            st.warning(f"Warning: {result['error']}")

                        st.info(f"Detected {result['symbols']} symbols")
                        st.markdown("</div>", unsafe_allow_html=True)

                        # Show segmentation visualization
                        if result["boxes"]:
                            st.subheader("🔍 Symbol Detection")
                            # Create visualization
                            vis_img = img_cv.copy()
                            if len(vis_img.shape) == 2:
                                vis_img = cv2.cvtColor(vis_img, cv2.COLOR_GRAY2BGR)

                            for i, (x, y, w, h) in enumerate(result["boxes"]):
                                cv2.rectangle(
                                    vis_img, (x, y), (x + w, y + h), (0, 255, 0), 2
                                )
                                cv2.putText(
                                    vis_img,
                                    str(i + 1),
                                    (x, y - 5),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.5,
                                    (0, 255, 0),
                                    1,
                                )

                            vis_img_rgb = cv2.cvtColor(vis_img, cv2.COLOR_BGR2RGB)
                            st.image(
                                vis_img_rgb,
                                caption="Detected symbols",
                                use_container_width=True,
                            )

            except Exception as e:
                st.error(f"Error processing image: {str(e)}")
                st.exception(e)

else:
    # Instructions
    st.info("👆 Upload an image file to get started!")

    # Example
    st.subheader("💡 Example")
    st.markdown("""
    **Try uploading an image with:**
    - Clear handwritten digits (0-9)
    - Math operators (+, -, ×, ÷)
    - Well-spaced symbols
    - Example equation: "2 + 3 = ?"
    """)

# Footer
st.markdown("---")
st.markdown(
    """
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>Handwritten Equation Solver using CNN</p>
</div>
""",
    unsafe_allow_html=True,
)
