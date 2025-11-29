#!/usr/bin/env python
"""
Isolated prediction worker - runs in separate process to avoid TensorFlow mutex crashes
"""
import sys
import os
import json
import numpy as np

# Set environment variables BEFORE importing TensorFlow
os.environ['TF_NUM_INTEROP_THREADS'] = '1'
os.environ['TF_NUM_INTRAOP_THREADS'] = '1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'

def predict_symbols(model_path, data_file):
    """Load model and make predictions in isolated process"""
    try:
        # Import TensorFlow INSIDE the function after env vars are set
        import tensorflow as tf
        
        # Configure TensorFlow IMMEDIATELY after import
        try:
            tf.config.threading.set_inter_op_parallelism_threads(1)
            tf.config.threading.set_intra_op_parallelism_threads(1)
            tf.config.optimizer.set_experimental_options({'disable_meta_optimizer': True})
            # Disable all threading optimizations
            tf.config.threading.set_inter_op_parallelism_threads(1)
            tf.config.threading.set_intra_op_parallelism_threads(1)
        except Exception as config_error:
            # Even if config fails, try to continue
            pass
        
        # Load model - this is where crashes usually happen
        try:
            model = tf.keras.models.load_model(model_path, compile=False)
        except Exception as load_error:
            return {'error': f"Failed to load model: {str(load_error)}"}
        
        # Load data
        try:
            X_data = np.load(data_file)
        except Exception as load_error:
            return {'error': f"Failed to load data: {str(load_error)}"}
        
        # Predict one at a time to avoid threading issues
        predictions_list = []
        for i in range(len(X_data)):
            try:
                single_input = np.expand_dims(X_data[i], axis=0)
                # Use direct tensor instead of predict() method
                single_tensor = tf.constant(single_input, dtype=tf.float32)
                
                # Use model.__call__ with training=False
                pred = model(single_tensor, training=False)
                
                # Convert to numpy safely
                if hasattr(pred, 'numpy'):
                    pred_np = pred.numpy()
                else:
                    pred_np = np.array(pred)
                
                predictions_list.append(pred_np[0])
            except Exception as pred_error:
                return {'error': f"Prediction failed at symbol {i}: {str(pred_error)}"}
        
        predictions = np.array(predictions_list)
        predicted_labels = np.argmax(predictions, axis=1)
        
        return predicted_labels.tolist()
    except Exception as e:
        import traceback
        return {'error': f"{str(e)}\n{traceback.format_exc()}"}

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(json.dumps({'error': 'Missing arguments: model_path data_file'}))
        sys.exit(1)
    
    model_path = sys.argv[1]
    data_file = sys.argv[2]
    
    try:
        result = predict_symbols(model_path, data_file)
        print(json.dumps(result))
        sys.exit(0)
    except Exception as e:
        print(json.dumps({'error': str(e)}))
        sys.exit(1)
