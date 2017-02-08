import time
import sys
import os
import glob
import shutil
import logging
from ConfigParser import SafeConfigParser
from watchdog.observers import Observer  
from watchdog.events import PatternMatchingEventHandler  
from Device42pgm import Device_d42


logger = logging.getLogger('Debugging logs')
logger.setLevel(logging.INFO)
fh = logging.FileHandler(strftime("log_for_watchfile_%m_%d_%Y.log"))
logger = logging.getLogger('Debugging logs')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(strftime("log_for_watchfile_%m_%d_%Y.log"))
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)



#Opening config parameters file to read
#filepath = sys.argv[1]
filepath = "../Device42_project/read_path_destination.cfg"
config = SafeConfigParser()
if not os.path.exists(filepath):
    logger.info("Cannot read destination file path")
    sys.exit(1)
else:
    pass
    

class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.xlsx"]

    def read_config(self):
        logger.info("starting to log in watchfile....")
        try:
            config.read(filepath)
            self.success_filepath = config.get('path', 'success_file_path')
            self.failure_filepath = config.get('path', 'failure_file_path')
        except IOError,e:
            logger.error(e, exc_info=True)

    def process(self, event):
        """
        event.event_type 
            'modified' | 'created' | 'moved' | 'deleted'
        """
        # the file will be processed there
#        print event.src_path, event.event_type
#        return event.src_path
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
            else:
                self.file_to_failure(user_file)
        return True            

    def file_to_success(self,user_file):
        try:
            user_file_noEXT, EXT = os.path.splitext(user_file)
            os.rename(user_file_noEXT, user_file_noEXT+'_'+time.strftime("%Y%m%d%H%M%S")+EXT)
            logger.info("Succesfully rename the file")
        except IOError:
            logger.error("Error in renaming file.")
            
        src = os.path.join(args,user_file)
        des = self.success_filepath
        if not os.path.exists(des):
            os.makedirs(des)
        shutil.move(src, des)
        return True

    def file_to_failure(self,user_file):
        try:
            user_file_noEXT, EXT = os.path.splitext(user_file)
            os.rename(user_file_noEXT, user_file_noEXT+'_'+time.strftime("%Y%m%d%H%M%S")+EXT)
            logger.info("Succesfully rename the file")
        except IOError:
            logger.error("Error in renaming file.")
            
        src = os.path.join(args,user_file)
        des = self.failure_filepath
        if not os.path.exists(des):
            os.makedirs(des)
        shutil.move(src, des)
        return True
        
        
if __name__ == '__main__':
    #args = sys.argv[1:]
    args = "./User_files"
    observer = Observer()
    #observer.schedule(MyHandler(), path=args[0] if args else '.')
    observer.schedule(MyHandler(), path=args)

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
            observer.stop()        
    observer.join()
