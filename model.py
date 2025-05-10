import numpy as np
import tensorflow as tf
from keras._tf_keras.keras.models import Sequential
from keras._tf_keras.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Input, Dropout, BatchNormalization
from keras._tf_keras.keras.preprocessing.image import ImageDataGenerator
from keras._tf_keras.keras.optimizers import Adam, RMSprop
from keras._tf_keras.keras.callbacks import ReduceLROnPlateau
import cv2 as cv
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from keras._tf_keras.keras.regularizers import L2
from sklearn.utils.class_weight import compute_class_weight
from keras._tf_keras.keras.models import load_model, Model
x_test =  tf.convert_to_tensor(np.load("Test(x).npy"),dtype=tf.float32)
y_test =  np.load("Test(y).npy")

x_train =  tf.convert_to_tensor(np.load("Train(x).npy"),dtype=tf.float32)
y_train =  np.load("Train(y).npy")
y_train = np.array([int(label) for label in y_train], dtype=np.int32)
y_test = np.array([int(label) for label in y_test], dtype=np.int32)
model=Sequential()
model.add(Input(shape=(200,200,1)))

model.add(Conv2D(128,(3,3),padding='same',activation='relu'))
model.add(MaxPooling2D((2,2))),
model.add(Conv2D(256,(3,3),padding='same',activation='relu'))
model.add(MaxPooling2D((2,2)))
model.add(Conv2D(512,(3,3),padding='same',activation='relu'))
model.add(MaxPooling2D((2,2)))

model.add(Dropout(0.2))
model.add(BatchNormalization())

model.add(Flatten())
model.add(Dense(416,activation='relu', kernel_regularizer=L2(0.1)))
model.add(Dense(208,activation='relu', kernel_regularizer=L2(0.1)))
model.add(Dense(104,activation='relu', kernel_regularizer=L2(0.1)))
model.add(Dense(52,activation='relu', kernel_regularizer=L2(0.1)))
model.add(Dense(len(np.unique(y_train)),activation='softmax')) # Output layer with correct number of classes

model.compile(optimizer=Adam(learning_rate=0.001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=0.0001)

# Fit the model using the augmented data
history = model.fit(x_train, y_train,
                    batch_size=40,
                    epochs=60,
                    validation_split=0.4,
                    shuffle=False,
                    verbose=1,
                    callbacks=[reduce_lr])

 # Load test data



test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=1,batch_size=1)
print(f'Test1 accuracy: {test_accuracy}')
print(f'Test1 loss: {test_loss}')
model.save(f"A{test_accuracy}L{test_loss}.h5")

# Plot training & validation accuracy values
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.grid()
plt.legend(['Train', 'Validation'], loc='upper left')

# Plot training & validation loss values
plt.subplot(1, 2, 2)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.grid()
plt.show()