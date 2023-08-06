from threading import Thread, Event
import socket
import pickle
from time import time

from whisper_spln.lockedQueue import lockedQueue

def timetoMinutesHour(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    s = round(s, 2)
    m = round(m, 0)
    h = round(h, 0)
    if h:
        return f'{h} hours, {m} minutes and {s} seconds'
    elif m:
        return f'{m} minutes and {s} seconds'
    else:
        return f'{s} seconds'

PORT = 9999
ASK_QUEUE_STATUS = "ASK_QUEUE_STATUS"


class Listener(Thread):
    def __init__(self, shared_queue: lockedQueue, event_shutdown: Event):
        Thread.__init__(self)
        self.shared_queue = shared_queue
        self.event_shutdown = event_shutdown

    def run(self):
        self.listen()

    def listen(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', PORT)
        server_socket.bind(server_address)
        server_socket.listen(1)
        server_socket.settimeout(10)
        while not self.event_shutdown.is_set():
            try:
                client_socket, client_address = server_socket.accept()
                print('Connected by', client_address)
                request = client_socket.recv(4096)

                received_dict = pickle.loads(request)
                response = self.handle_request(received_dict)
                client_socket.sendall(response.encode())
                client_socket.close()
            except socket.timeout:
                pass

        # Close the connection
        server_socket.close()

    def handle_request(self, request):
        if request['type'] == ASK_QUEUE_STATUS:
            queue_list, meanTime, isRunning = self.shared_queue.all_items()
            str_queue = 'Queue\nFile Name | File Size | Estimated Time'
            
            if isRunning:
                item = queue_list[0]
                queue_list = queue_list[1:]
                str_queue += f'\n{item["filename"]} | {item["size"]} b | {timetoMinutesHour(item["size"] * meanTime)} (running)'
                
            for item in queue_list:
                str_queue += f'\n{item["filename"]} | {item["size"]} b | {timetoMinutesHour(item["size"] * meanTime)}'
            
            return str_queue
        else:
            queue, meanTime, isRunning, actualSize, actualTime = self.shared_queue.put(request)
            prediction = self.predictTime(queue, meanTime, isRunning, actualSize, actualTime)
            return f'Your file will be ready in {timetoMinutesHour(prediction)}! Location : {request["dest_folder"]}'
        
    def predictTime(self, queue, meanTime, isRunning, actualSize, actualTime):
        prediction = 0
        for item in queue:
            prediction += item["size"] * meanTime

        if isRunning:
            timeDifference = actualSize * meanTime - (time() - actualTime)
            if timeDifference > 0:
                prediction += timeDifference

        return prediction
