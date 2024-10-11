#!/usr/bin/env python

import os
import sys
from random import randint
import time
import subprocess
from concurrent.futures import ThreadPoolExecutor as Pool

run_list = range(0, 419)
run_depth = 2

version = str(randint(0, 10**9))
if len(sys.argv) == 2:
    version = sys.argv[1]
print("Updating to version", version)

parallel = 6

os.system('mkdir -p store/version/')
os.system('mkdir -p store/tmp/')

def outdated(i):
    fn = f'store/version/{i}.txt'
    os.system(f'touch {fn}')
    with open(fn, 'r') as f:
        t = f.read()
    return t != version

def update(i):
    fn = f'store/version/{i}.txt'
    with open(fn, 'w') as f:
        f.write(version)

run_list = [i for i in run_list if outdated(i)]

done = 0
n = len(run_list)

def timed_run(command, stdout_file, stderr_file):
    start_time = time.time()
    with open(stdout_file, 'w') as out, open(stderr_file, 'w') as err:
        result = subprocess.run(command, stdout=out, stderr=err)
    end_time = time.time()
    execution_time = end_time - start_time
    return result.returncode, execution_time

def run(i):
    global done
    returncode, exec_time = timed_run(['./run', str(i), str(run_depth)], 
                                      f'store/tmp/{i}_out.txt', 
                                      f'store/tmp/{i}_err.txt')
    if returncode:
        print(f"{i} Crashed")
        return i
    os.system(f'cp store/tmp/{i}_out.txt store/{i}_out.txt')
    update(i)
    done += 1
    print(f"{done} / {n}     \r", end="")
    sys.stdout.flush()
    print(f"Task {i} completed in {exec_time:.2f} seconds")
    return i

subprocess.run(['make', '-j'])
scores = []
with Pool(max_workers=parallel) as executor:
    for i in executor.map(run, run_list):
        pass
print("Done!       ")
