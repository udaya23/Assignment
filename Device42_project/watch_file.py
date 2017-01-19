import time
import sys
import os
import shutil
from watchdog.observers import Observer  
from watchdog.events import PatternMatchingEventHandler  
from Device42pgm import Device_d42

threads = []

class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.xlsx"]

    def process(self, event):
        """
        event.event_type 
            'modified' | 'created' | 'moved' | 'deleted'
        """
        # the file will be processed there
        #print event.src_path, event.event_type
        head, tail = os.path.split(event.src_path)
        return tail

    def on_created(self, event):
        user_file = self.process(event)
        c = Device_d42()
        data = c.read_from_xlsx(user_file)
        if not data:
            self.file_to_failure(user_file)
        else:
            status = c.post_multipledata(user_file)
            if status:
                self.file_to_success(user_file)
        return True            

    def file_to_success(self,user_file):
        src = os.path.join(args,user_file)
        des = "./Success_files"
        if not os.path.exists(des):
            os.makedirs(des)
        shutil.move(src, des)
        return True

    def file_to_failure(self,user_file):
        src = os.path.join(args,user_file)
        des = "./Failure_files"
        if not os.path.exists(des):
            os.makedirs(des)
        shutil.move(src, des)
        return True
        
if __name__ == '__main__':
#    args = sys.argv[1:]
    args = "./User_files"
    observer = Observer()
#    observer.schedule(MyHandler(), path=args[0] if args else '.')
    observer.schedule(MyHandler(), path=args)

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
            observer.stop()
        
    observer.join()
