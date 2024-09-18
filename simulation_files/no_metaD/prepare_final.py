import numpy as np
import os
import argparse

parser = argparse.ArgumentParser()
# simulation-related parameters
parser.add_argument("-seed",type=int)
parser.add_argument("-r",type=float)		# resetting rate in ns^-1
parser.add_argument("-rcond",type=str)		# condition for resetting (if rcond==true then reset)
# job-related parameters
parser.add_argument("-N",type=int)		# number of trajectories
parser.add_argument("-ncores",type=int)		# maximal number of subprocesses (should be less than or equal to ppn)
parser.add_argument("-dir",type=str)		# directory inside which the simulations will run
parser.add_argument("-new",action="store_true")	# if present, use the versions of LAMMPS and PLUMED which were compiled for the hirshb-new queue. for any other queue, do not specify
args = parser.parse_args()
arg_d = vars(args)
for arg in arg_d:
    if arg_d[arg] is None:
        raise Exception(f"Parameter '{arg}' not set")

# set variables and create directories
if args.r == 0:
    stride = 1000000000		# default arbitrary number of steps for simulations without resetting
    rcond = "false"
else:
    stride = int(args.r)	# convert ns to fs
    rcond = args.rcond
root = os.getcwd()
rng = np.random.default_rng(args.seed)
os.mkdir(f"{root}/{args.dir}")
os.mkdir(f"{root}/{args.dir}/data")
os.mkdir(f"{root}/{args.dir}/sims")

# import formats
with open(root+"/formats/run.lmp",'r') as f:
    lmp_format = f.read()
with open(root+"/formats/plumed.dat",'r') as f:
    plmd_format = f.read()
#
# INSERT ANY OTHER FILES REQUIRED FOR LAMMPS TO RUN A TRAJECTORY
#
with open(root+"/formats/run.sh",'r') as f:
    run_script = f.read()

# change LAMMPS folder if needed. TO BE CHANGED BY THE USER TO MATCH THEIR NAMING CONVENTIONS
if args.new:
    run_script = run_script.replace("lammps-23Jun2022","lammps-23Jun2022_new").replace("load.sh","load_new.sh")		

# create input and node scripts
for i in range(args.N):
    path = f"{root}/{args.dir}/sims/{i}"
    os.mkdir(path)
    lmp_script = lmp_format.replace("{p_SEED}",str(rng.integers(0,100000)))
    lmp_script = lmp_script.replace("{p_STRIDE}",str(stride))
    if rcond == "true":
        cond = "1.0"
        lmp_script = lmp_script.replace("{p_RCOND}",('variable check equal 1.0 \nfix cond all halt ${test} v_check == 1.0 error continue'))
        lmp_script = lmp_script.replace("v_check < 0.0 error",('v_check == 1.0 error'))
    elif rcond == "false":
        cond = "0.0"
        lmp_script = lmp_script.replace("{p_RCOND}",(' '))
        lmp_script = lmp_script.replace("fix cond all halt ${test} v_check < 0.0 error continue",(' '))
    else:
        cond = rcond.split()
        lmp_script = lmp_script.replace("{p_RCOND}",('variable checkb equal '+str(cond[0])+'\n variable ang equal '+str(cond[1])+'*3.14159265358979/180.0\n variable checka equal '+str(cond[2])+'\n variable cv_neg equal (tan(${ang})*(-100-${checka})+${checkb})\n variable cv_pos equal (tan(${ang})*(100-${checka})+${checkb})\n variable check equal ((-100-${checka}-(100-${checka}))*(x[1]-${cv_pos})-(${cv_neg}-${cv_pos})*(y[1]-(100-${checka})))\n fix cond all halt ${test} v_check < 0.0 error continue').replace(" x "," ").replace(" y "," "))
    with open(path+"/run.lmp",'w') as f:
        f.write(lmp_script)
    with open(path+"/plumed.dat",'w') as f:
        f.write(plmd_format)
    #
    # INSERT ANY OTHER FILES REQUIRED FOR LAMMPS TO RUN A TRAJECTORY
    #

# write run script to be sent as a job
run_script += f"python3 {root}/simulate.py {root}/{args.dir}/sims 0 {args.N} {args.ncores}"
with open(f"{root}/{args.dir}/data/run.sh",'w') as f:
    f.write(run_script)
# write a rerun script in case something goes wrong
rerun = f"cd {root}\npython3 prepare.py -N {args.N} -ncores {args.ncores} -dir {args.dir}{' -new' if args.new else ''} -r {args.r} -seed {args.seed} -rcond \"{args.rcond}\""
with open(f"{root}/{args.dir}/data/rerun.sh",'w') as f:
    f.write(rerun)
