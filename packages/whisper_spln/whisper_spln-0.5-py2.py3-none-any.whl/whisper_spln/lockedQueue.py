from threading import Lock
from time import time
import os


class lockedQueue():

    def __init__(self):
        self.lock = Lock()
        self.queue = []
        self.isRunning = False
        self.actualName = ''
        self.actualTime = 0
        self.actualSize = 0
        self.meanTime = 0
        self.numConversions = 0
        self.loadTime()
    
    def loadTime(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_file_path = os.path.join(script_dir, 'conf/exec_time')
        
        with open(config_file_path, 'r') as file:
            lines = [line.rstrip() for line in file]
        
        if len(lines) == 2:
            self.meanTime = float(lines[0])
            self.numConversions = float(lines[1])
    
    def saveTime(self):
        self.lock.acquire()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_file_path = os.path.join(script_dir, 'conf/exec_time')
        
        with open(config_file_path, 'w') as file:
            file.write(f"{self.meanTime}\n")
            file.write(f"{self.numConversions}\n")
            
        self.lock.release()

    def put(self, item):
        self.lock.acquire()
        item["size"] = os.stat(item["filename"]).st_size
        self.queue.append(item)
        self.lock.release()

        return self.queue, self.meanTime, self.isRunning, self.actualSize, self.actualTime

    def get(self):
        self.lock.acquire()
        self.actualSize = self.queue[0]["size"]
        self.actualTime = time()
        self.actualName = self.queue[0]["filename"]
        self.isRunning = True
        item = self.queue.pop(0)
        self.lock.release()
        return item

    def empty(self):
        self.lock.acquire()
        empty = len(self.queue) == 0
        self.lock.release()
        return empty

    def all_items(self):
        self.lock.acquire()
        items = self.queue.copy()
        
        if self.isRunning:
            running = {}
            running['size'] = self.actualSize
            running['filename'] = self.actualName
            items.insert(0, running)
            
        isRunning = self.isRunning
        time = self.meanTime
        self.lock.release()
        return items, time, isRunning

    def calculteNewMean(self):
        self.lock.acquire()

        meanTime = (time() - self.actualTime) / self.actualSize

        self.meanTime = (self.meanTime * self.numConversions +
                         meanTime) / (self.numConversions + 1)
        self.numConversions += 1
        self.isRunning = False

        self.lock.release()

    def stopRunning(self):
        self.lock.acquire()
        self.isRunning = False
        self.lock.release()
