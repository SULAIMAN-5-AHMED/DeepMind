import cv2 as cv
import mediapipe as mp
import numpy as np
import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Initialize MediaPipe Hands



def folder_to_data(main_dir):

    file_data = []

    # Walk through the directory structure
    for label in os.listdir(main_dir):
        label_dir = os.path.join(main_dir, label)
        if os.path.isdir(label_dir):
            for file in os.listdir(label_dir):
                if file.endswith('.jpg') or file.endswith('.jpeg'):
                    file_data.append((file, label))

    # Create a DataFrame
    data = pd.DataFrame(file_data, columns=['FileName', 'Label'])
    return data





data = folder_to_data("/Test1")
data = data.sample(frac=1).reset_index(drop=True)


print(len(data))

images = []
labels = []
n=0
passed = 0
ignored = 0
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.35)
for index, row in data.iterrows():
    img_path = row['FileName']
    label = row['Label']
    n+=1
    print(f"Processing image: {label} with item: {n} ")
    img = cv.imread(r"C:\\Users\\sulai\\Desktop\\PYTHON\\AppDev\\Test1\\{}\\{}".format(label,img_path))
    result = hands.process(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    if result.multi_hand_landmarks: # Processing hands
        passed += 1
        for hand_landmarks in result.multi_hand_landmarks:
            # Get bounding box coordinates
            #mp_drawing.draw_landmarks(
                #img,
                #hand_landmarks,
                #mp_hands.HAND_CONNECTIONS,
                #mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                #mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2))
            x_min = max(0, int(min([lm.x for lm in hand_landmarks.landmark]) * img.shape[1]) - 80)
            y_min = max(0, int(min([lm.y for lm in hand_landmarks.landmark]) * img.shape[0]) - 40)
            x_max = min(img.shape[1], int(max([lm.x for lm in hand_landmarks.landmark]) * img.shape[1]) + 70)
            y_max = min(img.shape[0], int(max([lm.y for lm in hand_landmarks.landmark]) * img.shape[0]) + 50)

    else:
        ignored += 1
        print(f"No hand detected in image.with label {label}  and path {img_path}")
        pass
    img = cv.resize(img,(200,200))
    img = cv.cvtColor(img,cv.COLOR_RGB2GRAY)
    cv.imshow('img',img)
    cv.waitKey(15)
    max_pixel_value = 255.0

    img = img.astype("float32")
    img = img/ max_pixel_value
    images.append(np.array(img))
    labels.append(label)


x_train = np.expand_dims(np.array(images), axis=-1)

y_train = labels

np.save("Test(x).npy", images)
np.save("Test(y).npy", y_train)
print(f"Processed {passed} images with hand landmarks and {ignored} images without hand landmarks.")
