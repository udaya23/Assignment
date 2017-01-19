import time
import sys
import os
import thread
import threading
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
#        print tail
 
        # print now only for degug

#    def on_modified(self, event):
#        self.process(event)

    def on_created(self, event):
        user_file = self.process(event)
        c = Device_d42()
        c.post_multipledata(user_file)


if __name__ == '__main__':
#    args = sys.argv[1:]
    args = "./User_files"
    observer = Observer()
#    observer.schedule(MyHandler(), path=args[0] if args else '.')
    observer.schedule(MyHandler(), path=args)
#    threads.append(observer)


    observer.start()
#    print threads

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
            observer.stop()
        
    observer.join()
