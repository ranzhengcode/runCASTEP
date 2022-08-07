#!/usr/bin/env python
'''
    Author: Ran Zheng
    
    Source of demofiles: http://www.castep.org/Tutorials/BasicsAndBonding
'''

import psutil as psl
import time as t
import os

def checkProcessIsExist(processName):
    '''
    Check if the process processName exists.
    '''
    flag = False
    for pid in psl.pids():
        # Check if process name contains the given processName.
        if psl.Process(pid).name().lower() == processName.lower():
            flag = True
            break
    return flag

def getFiles(suffix,dir=os.getcwd()):
    '''
    Get the file name of the specified folder *dir* and its subfolders in the specified format.
    '''
    rename = []
    # Iterate through the specified folder and its subfolders.
    for root,directory,files in os.walk(dir,topdown=True):
        for filename in files:
            # Split filename and suffix.
            fname,suf = os.path.splitext(filename)
            # Check if suf name contains the given suffix.
            if suf.lower() == suffix.lower():
                rename.append(os.path.join(root,fname))
    return(rename)

# 
suffix = '.cell'

fname  = getFiles(suffix)

# Number of CPU cores, you can customize **ncore** according to your CPU cores.
ncore  = 4
processName = 'castep.mpi'

taskId = 1
if len(fname) > 0:
    for name in fname:
        cmd = 'mpirun -np '+ str(ncore)+' castep.mpi ' + name
        print('Task No.: '+ str(taskId)+';  Task Name: '+name)
        if taskId == 1:
            # Execute castep.mpi command
            os.system(cmd)
        else:
            while True:
                if checkProcessIsExist(processName):
                    # Pause 1.5 seconds to avoid frequent judgments
                    t.sleep(1.5)
                    continue
                else:
                    # Execute CASTEP
                    os.system(cmd)
                    break
        print()
        taskId += 1
    print('Task completed!')
else:
    print("No files in " + suffix + " format exist in the specified folder and its subfolders")

