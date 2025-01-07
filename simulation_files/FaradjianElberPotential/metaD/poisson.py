import numpy as np
import os
import warnings
os.system("rm random")

for i in range(0,25000):
    random = int(np.random.exponential(abcdef))
    if (random!=0.0):
        with open("random", "a") as newFile:
            newFile.write(str(random)+'\n')
            newFile.close()
