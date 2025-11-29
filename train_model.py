"""
Training script for Handwritten Equation Solver
Extracted and fixed from the notebook
"""
import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Input, Conv2D, Activation, MaxPool2D, Flatten, Dense, Dropout
from tensorflow.keras.initializers import glorot_uniform
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.regularizers import l2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

print("="*60)
print("Training Handwritten Math Symbol Recognition Model")
print("="*60)

# Configuration
DATADIR = 'data/data/dataset'
RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)
tf.random.set_seed(RANDOM_STATE)

# Load data
print("\n1. Loading images...")
x = []
y = []

if not os.path.exists(DATADIR):
    raise FileNotFoundError(f"Dataset directory not found: {DATADIR}")

for folder in sorted(os.listdir(DATADIR)):
    path = os.path.join(DATADIR, folder)
    if not os.path.isdir(path):
        continue
    
    print(f"  Loading {folder}...", end=" ")
    count = 0
    for image_file in os.listdir(path):
        if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(path, image_file)
            img = cv2.imread(img_path)
            if img is not None:
                x.append(img)
                y.append(folder)
                count += 1
    print(f"{count} images")

print(f"\n✓ Loaded {len(x)} images")
print(f"✓ Classes: {sorted(set(y))}")

# Preprocess images
print("\n2. Preprocessing images...")
X = []
for i, img in enumerate(x):
    if (i + 1) % 500 == 0:
        print(f"  Processing {i+1}/{len(x)}...")
    
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    threshold_image = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)[1]
    threshold_image = cv2.resize(threshold_image, (32, 32))
    X.append(threshold_image)

print(f"✓ Preprocessed {len(X)} images")

# Encode labels
print("\n3. Encoding labels...")
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)
num_classes = len(label_encoder.classes_)
print(f"✓ {num_classes} classes: {label_encoder.classes_}")

# Convert to numpy arrays
X = np.array(X)
y_encoded = np.array(y_encoded)

# Normalize and reshape
X = np.expand_dims(X, axis=-1)
X = X / 255.0
Y = to_categorical(y_encoded, num_classes=num_classes)

print(f"✓ Final shape: X={X.shape}, Y={Y.shape}")

# Train-test split
print("\n4. Splitting data...")
X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.2, random_state=RANDOM_STATE, stratify=y_encoded
)
print(f"✓ Train: {X_train.shape[0]} samples")
print(f"✓ Test: {X_test.shape[0]} samples")

# Build model
print("\n5. Building model...")
def math_symbol_and_digits_recognition(input_shape=(32, 32, 1), num_classes=14):
    regularizer = l2(0.01)
    model = Sequential()
    model.add(Input(shape=input_shape))
    model.add(Conv2D(32, (3, 3), strides=(1, 1), padding='same', 
                     kernel_initializer=glorot_uniform(seed=0), 
                     name='conv1', activity_regularizer=regularizer))
    model.add(Activation(activation='relu', name='act1'))
    model.add(MaxPool2D((2, 2), strides=(2, 2)))
    model.add(Conv2D(32, (3, 3), strides=(1, 1), padding='same', 
                     kernel_initializer=glorot_uniform(seed=0), 
                     name='conv2', activity_regularizer=regularizer))
    model.add(Activation(activation='relu', name='act2'))
    model.add(MaxPool2D((2, 2), strides=(2, 2)))
    model.add(Conv2D(64, (3, 3), strides=(1, 1), padding='same', 
                     kernel_initializer=glorot_uniform(seed=0), 
                     name='conv3', activity_regularizer=regularizer))
    model.add(Activation(activation='relu', name='act3'))
    model.add(MaxPool2D((2, 2), strides=(2, 2)))
    model.add(Flatten())
    model.add(Dropout(0.5))
    model.add(Dense(120, activation='relu', kernel_initializer=glorot_uniform(seed=0), name='fc1'))
    model.add(Dense(84, activation='relu', kernel_initializer=glorot_uniform(seed=0), name='fc2'))
    model.add(Dense(num_classes, activation='softmax', kernel_initializer=glorot_uniform(seed=0), name='fc3'))
    
    optimizer = Adam()
    model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
    return model

model = math_symbol_and_digits_recognition(input_shape=(32, 32, 1), num_classes=num_classes)
model.summary()

# Data augmentation
print("\n6. Setting up data augmentation...")
aug = ImageDataGenerator(
    zoom_range=0.1,
    width_shift_range=0.05,
    height_shift_range=0.05
)

# Train model
print("\n7. Training model (this will take a while)...")
print("   Training for 50 epochs (reduced for faster completion)...")

history = model.fit(
    aug.flow(X_train, Y_train, batch_size=128),
    batch_size=128,
    epochs=50,  # Reduced from 100 for faster completion
    validation_data=(X_test, Y_test),
    verbose=1
)

# Evaluate
print("\n8. Evaluating model...")
test_loss, test_acc = model.evaluate(X_test, Y_test, verbose=0)
print(f"✓ Test Accuracy: {test_acc*100:.2f}%")

# Save model and label encoder
print("\n9. Saving model and label encoder...")
model.save('model.h5')
print("✓ Model saved as model.h5")

import joblib
joblib.dump(label_encoder, 'label_encoder.pkl')
print("✓ Label encoder saved as label_encoder.pkl")

print("\n" + "="*60)
print("Training completed successfully!")
print("="*60)

