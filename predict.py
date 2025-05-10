from flask import Flask, request, jsonify
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import os
import mediapipe as mp

# Load ASL Model
MODEL_PATH = '/home/user/myapp/python_model/A78L1.h5'
model = load_model(MODEL_PATH)

# Class labels (update based on your training labels)
CLASS_LABELS = {
    0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J',
    10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S',
    19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z'
}

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    min_detection_confidence=0.5
)

app = Flask(__name__)

def detect_hand(image):
    """
    Detects the hand in the image and returns the cropped + resized ROI.
    Returns None if no hand detected.
    """
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    if not results.multi_hand_landmarks:
        return None  # No hand detected

    h, w, _ = image.shape
    landmarks = results.multi_hand_landmarks[0]

    # Get bounding box around the hand
    x_coords = [landmark.x * w for landmark in landmarks.landmark]
    y_coords = [landmark.y * h for landmark in landmarks.landmark]

    x_min, x_max = int(min(x_coords)), int(max(x_coords))
    y_min, y_max = int(min(y_coords)), int(max(y_coords))

    # Add padding to the bounding box
    padding = 20
    x_min = max(0, x_min - padding)
    y_min = max(0, y_min - padding)
    x_max = min(w, x_max + padding)
    y_max = min(h, y_max + padding)

    # Crop and resize the hand region
    hand_img = image[y_min:y_max, x_min:x_max]
    hand_img = cv2.resize(hand_img, (200, 200))  # Resize to match model input size

    return hand_img


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    image_path = data.get('image_path')

    if not image_path or not os.path.exists(image_path):
        return jsonify({'error': 'Image path invalid or missing'}), 400

    try:
        # Read image
        img = cv2.imread(image_path)
        if img is None:
            return jsonify({'error': 'Failed to read image'}), 400

        # Detect and crop hand
        hand_img = detect_hand(img)
        if hand_img is None:
            return jsonify({'error': 'No hand detected in the image'}), 400

        # Preprocess for model
        hand_img_gray = cv2.cvtColor(hand_img, cv2.COLOR_BGR2GRAY)
        hand_img_normalized = hand_img_gray / 255.0
        hand_img_input = np.expand_dims(hand_img_normalized, axis=-1)  # Add channel
        hand_img_input = np.expand_dims(hand_img_input, axis=0)       # Add batch dim

        # Predict
        pred = model.predict(hand_img_input)
        predicted_label = CLASS_LABELS.get(np.argmax(pred, axis=1)[0], "Unknown")

        return jsonify({'label': predicted_label})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
