#import shutil
import sched
import os
import time
from datetime import datetime,timedelta

scheduler = sched.scheduler(time.time,time.sleep)
path = "../Device42_project/User_new_files"

ext = (".xlsx")
isdir = os.path.isdir(path)
if isdir:
    old = set(os.listdir(path))
    print old
else:
    print "It is not a directory"


def watch_dog():   
    if os.path.isdir(path):
        new = set(os.listdir(path))
        for name in new - old:
            if name.endswith(ext):
                print "The new file added is {0}".format(name)
    else:
        pass

def do_task():   
    print time.ctime()
    scheduler.enter(10, 1, watch_dog, ())
#    scheduler.enter(10, 1, watch_dog, ())
    scheduler.run()

do_task()

        
