
import os
import numpy as np
##Position in which the condition passes through the x coordinate
conditions_distancex=np.array(["3"])

##Position in which the line of the condition passes through y coordinate
conditions_distancey=np.array(["0.0"])

##Angle of the condition centered at the above position in x, y
conditions_angle=np.array(["0"])

##Resetting time in timesteps
cutoffs=np.array([1])

##Number of Samples
samples=1000

##Seed used in dynamics
seed=12345
for i in range(len(conditions_distancex)):
    for k in range(len(conditions_angle)):
        for j in range(len(cutoffs)):
            os.system("python3 prepare_final.py -r "+str(cutoffs[j])+"  -seed "+str(seed)+" -N "+str(samples)+" -ncores 1 -dir reset_"+str(cutoffs[j])+"_x"+str(conditions_distancex[i])+"_y"+str(conditions_distancey[i])+"_angle"+str(conditions_angle[k])+" -rcond '"+str(conditions_distancex[i])+" "+str(conditions_angle[k])+" "+str(conditions_distancey[i])+"'")
            os.system("cp poisson.py reset_"+str(cutoffs[j])+"_x"+str(conditions_distancex[i])+"_y"+str(conditions_distancey[i])+"_angle"+str(conditions_angle[k])+"/data")
            os.system("sed -i 's/abcdef/"+str(cutoffs[j])+"/g' reset_"+str(cutoffs[j])+"_x"+str(conditions_distancex[i])+"_y"+str(conditions_distancey[i])+"_angle"+str(conditions_angle[k])+"/data/poisson.py")
            os.chdir("reset_"+str(cutoffs[j])+"_x"+str(conditions_distancex[i])+"_y"+str(conditions_distancey[i])+"_angle"+str(conditions_angle[k])+"/data")
            os.system("echo $PWD")
            os.system("chmod 755 run.sh")
            os.system("./run.sh > out.log &")
            os.chdir("../..")
