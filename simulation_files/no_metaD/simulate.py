from sys import argv
from multiprocessing import Process, Queue
import os

# handle input parameters
root = argv[1]
idx_low = int(argv[2])
idx_high = int(argv[3])
ncores = int(argv[4])

def simulate(i):
        os.chdir(f"{root}/{i}")
        os.system("cp ../../data/poisson.py .")
        os.system("python3 poisson.py")
        os.system("echo $PWD")
        os.system("lmp_serial -in run.lmp -screen none -log none")
        # cleanup
        loc = os.getcwd()
        files = ["plumed.dat","run.lmp","log.plumed"]
        for f in files:
            path = os.path.join(loc,f)
            os.remove(path)

run_queue = Queue()
#for i in range(idx_low,idx_high):
#    run_queue.put(i)
#for i in range(ncores):
#    p = Process(target=simulate,args=(run_queue,i))
#    p.start()
for i in range(idx_low,idx_high):
   simulate(i)
