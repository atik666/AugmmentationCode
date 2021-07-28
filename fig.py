import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

sig = pd.read_csv('allSig.csv', header=None)
sig = sig.to_numpy()

x = np.arange(1,1001).astype('float64')

for i in range(np.size(sig, 1)): 
    plt.subplot(5, 1, i+1)
    plt.plot(x, sig[:,i])
    #plt.show()
    plt.xlabel("Samples")

