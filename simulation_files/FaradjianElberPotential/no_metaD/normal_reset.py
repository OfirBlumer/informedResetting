
import os
import numpy as np
##Resetting time in timesteps
cutoffs=np.array([7025])

##Number of Samples
samples=1000

##Seed used in dynamics
seed=12345

for j in range(len(cutoffs)):
    os.system("python3 prepare_final.py -r "+str(cutoffs[j])+" -seed "+str(seed)+" -N "+str(samples)+" -ncores 1 -dir reset_"+str(cutoffs[j])+" -rcond 'true'")
    os.system("cp poisson.py reset_"+str(cutoffs[j])+"/data")
    os.system("sed -i 's/abcdef/"+str(cutoffs[j])+"/g' reset_"+str(cutoffs[j])+"/data/poisson.py")
    os.chdir("reset_"+str(cutoffs[j])+"/data")
    os.system("echo $PWD")
    os.system("chmod 755 run.sh")
    os.system("./run.sh > out.log &")
    os.chdir("../..")
