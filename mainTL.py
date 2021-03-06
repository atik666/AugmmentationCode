from IPython import get_ipython  
get_ipython().magic('reset -sf')
import numpy as np
import keras
from keras.preprocessing.image import load_img
import tensorflow as tf
import tensorflow_hub as hub
from tensorflow.keras.callbacks import EarlyStopping,ModelCheckpoint
from matplotlib import pyplot as plt

fault = {
         0: ["r1",'r2','r3','r1r3','r1r2','r2r3','r1r2r3'],
         1: ["l1",'l2','l3','l1l3','l1l2','l2l3','l1l2l3'],
         2: ["t1",'t2','t3','t1t3','t1t2','t2t3','t1t2t3']
         }

def load_data(cond = "Train", S = 1, L = 200):
    X_train = []
    y_train = []
    for key,value in fault.items():
        for j in value:
            images = []
            for i in range(S,L+1):
                img = load_img(
                    r'D:\Aug\Data\{}\{}\FIG{}.png'.format(j,cond,i),
                           grayscale=False, color_mode="rgb")
                img = keras.preprocessing.image.img_to_array(img)
                img = np.expand_dims(img, axis=0)
                images.append(img)   
                print(cond, j,i, ":", key)    
            x = np.vstack(images)  
            X_train.append(x)    
            del x
            y = np.full(L-S+1, key).astype('float32')
            y_train.append(y)
    
    X_train = np.concatenate(X_train)
    X_train /= 255
    y_train = np.concatenate(y_train).ravel()        
    return X_train, y_train
    
X_train, y_train = load_data(cond = "Train", S = 1, L = 200)
X_val, y_val = load_data(cond = "Val", S = 201, L = 300)
X_test, y_test = load_data(cond = "Test", S = 301, L = 400)

IMAGE_SHAPE = (224, 224)
      
feature_extractor_model = "https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/4"

pretrained_model_without_top_layer = hub.KerasLayer(
    feature_extractor_model, input_shape=(224, 224, 3), trainable=False)
       
num_class = 3

model = tf.keras.Sequential([
  pretrained_model_without_top_layer,
  tf.keras.layers.Dense(num_class)
])

model.summary()          
         
model.compile(
  optimizer="adam",
  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
  metrics=['accuracy'])
      
early_stopping = EarlyStopping(monitor='val_loss',patience=5)
modelCheckpoint = ModelCheckpoint('diagCNN_model.hdf5',save_best_only = True)
     
# Train your model using the early stopping callback
h_callback = model.fit(X_train, y_train, batch_size = 32,
           epochs = 50, validation_data = (X_val, y_val),
           callbacks = [early_stopping,modelCheckpoint])

# load weights
model.load_weights("diagCNN_model.hdf5")

loss, acc= model.evaluate(X_test, y_test)
print('Test Accuracy: %f' % (acc*100))

def plot_loss(loss,val_loss):
  plt.figure()
  plt.plot(loss)
  plt.plot(val_loss)
  plt.title('Model loss')
  plt.ylabel('Loss')
  plt.xlabel('Epoch')
  plt.legend(['Train', 'Validation'], loc='upper right')
  plt.show()
  
def plot_accuracy(acc,val_acc):
  # Plot training & validation accuracy values
  plt.figure()
  plt.plot(acc)
  plt.plot(val_acc)
  plt.title('Model accuracy')
  plt.ylabel('Accuracy')
  plt.xlabel('Epoch')
  plt.legend(['Train', 'Validation'], loc='lower right')
  plt.show()
  
# Plot train vs test loss during training
plot_loss(h_callback.history['loss'], h_callback.history['val_loss'])

# Plot train vs test accuracy during training
plot_accuracy(h_callback.history['accuracy'], h_callback.history['val_accuracy'])

from sklearn.metrics import confusion_matrix
y_pred = model.predict(X_test)
y_pred = np.argmax(y_pred, axis=1)
conf = confusion_matrix(y_test, y_pred)
print(conf)
print('acc : ', np.trace(conf)/np.sum(conf)*100)
