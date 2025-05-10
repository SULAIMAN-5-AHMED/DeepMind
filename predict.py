from flask import Flask, request, jsonify
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import os

# Load the trained ASL model
MODEL_PATH = 'asl_model.h5'
model = load_model("/home/user/myapp/python_model/A78L1.h5")

# Define class labels (must match your training labels)
CLASS_LABELS = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J',
10:'K',11:'L',12:'M',13:'N'14:'O',15:'P',16:'Q',17:'R',18:'S',
19:'T',20:'U',21:'V',22:'W',23:'X',24:'Y',25:'Z'}
app = Flask(_name_)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    image_path = data.get('image_path')

    if not image_path or not os.path.exists(image_path):
        return jsonify({'error': 'Image path invalid or missing'}), 400

    # Preprocess image
    try:
        img = cv2.imread(image_path)
        img = cv2.resize(img, (200, 200))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = img / 255.0
        img = np.expand_dims(img, axis=-1)  # Add channel
        img = np.expand_dims(img, axis=0)   # Add batch dim

        # Predict
        pred = model.predict(img)
        predicted_label = CLASS_LABELS.get(np.argmax(pred, axis=1)[0])

        return jsonify({'label': predicted_label})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=5000)