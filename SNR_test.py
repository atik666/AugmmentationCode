from IPython import get_ipython  
get_ipython().magic('reset -sf')
import numpy as np
import keras
from keras.preprocessing.image import load_img

fault = ["Norm",
         "IR07", "IR14", "IR21",
         "OR07", "OR14", "OR21",
         "BF07", "BF14", "BF21"]

fault = dict(enumerate(fault))

def load_data(cond = "Train", S = 1, L = 100):
    X_train = []
    y_train = []
    for key,value in fault.items():
            images = []
            for i in range(S,L+1):
                img = load_img(
                    r'D:\Aug\Bearing\{}\SNR\{}\FIG{}.png'.format(value,cond,i),
                           grayscale=False, color_mode="rgb")
                img = keras.preprocessing.image.img_to_array(img)
                img = np.expand_dims(img, axis=0)
                images.append(img)   
                print(cond,value,i,":",key)    
            x = np.vstack(images)  
            X_train.append(x)    
            del x
            y = np.full(L-S+1, key).astype('float32')
            y_train.append(y)
    
    X_train = np.concatenate(X_train)
    X_train /= 255
    y_train = np.concatenate(y_train).ravel()        
    return X_train, y_train

for i in range(-8,11,2):
    print(i)  
    X_test, y_test = load_data(cond = "%s db"%i, S = 1, L = 50)
    np.save(r'D:/Aug/Bearing/SNR_Test/%sX_test.npy'%i, X_test)
    np.save(r'D:/Aug/Bearing/SNR_Test/%sy_test.npy'%i, y_test)


