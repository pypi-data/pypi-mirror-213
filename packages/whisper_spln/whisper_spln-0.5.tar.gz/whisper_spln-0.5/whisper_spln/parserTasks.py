from whisper_spln.listener import ASK_QUEUE_STATUS, PORT, timetoMinutesHour
import socket
import pickle
import subprocess
import sys
import os


def runWhisper(input_file, dest_folder, inputLang, outputLang):
    dict = {
        "filename": input_file,
        "output_lang": outputLang,
        "dest_folder": dest_folder,
        "input_lang": inputLang,
        "type": ''
    }
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', PORT)
        client_socket.connect(server_address)

        send_request = pickle.dumps(dict)
        client_socket.sendall(send_request)
        response = client_socket.recv(1024)
        print(response.decode())
        client_socket.close()
    except ConnectionRefusedError:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        error_log_path = os.path.join(script_dir, 'conf/error.log')
        output_log_path = os.path.join(script_dir, 'conf/output.log')
        config_file_path = os.path.join(script_dir, 'conf/exec_time')
        prediction = predictTime(config_file_path, input_file)
        print(
            f'Your file will be ready in {timetoMinutesHour(prediction)}! Location: {dest_folder}')
        subprocess.Popen(
            ["python3", "whisper_spln/startThreads.py"] + sys.argv[1:], stdout=open(output_log_path, "a"), stderr=open(error_log_path, "a"))


def predictTime(file_time, input_file):
    with open(file_time, 'r') as file:
        lines = [line.rstrip() for line in file]

    meanTime = 0
    if len(lines) == 2:
        meanTime = float(lines[0])

    size = os.stat(input_file).st_size
    return size * meanTime


def getQueue():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', PORT)

        dict = {'type': ASK_QUEUE_STATUS}
        send_request = pickle.dumps(dict)
        client_socket.connect(server_address)
        client_socket.sendall(send_request)
        response = client_socket.recv(1024)

        print(response.decode())
        client_socket.close()
    except ConnectionRefusedError:
        print("No server found, no jobs in queue")


def getLogs():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    error_log_path = os.path.join(script_dir, 'conf/error.log')
    output_log_path = os.path.join(script_dir, 'conf/output.log')

    with open(error_log_path, 'r') as file:
        error_text = file.read()
    with open(output_log_path, 'r') as file:
        output_text = file.read()

    print('App Logs\n\nOUTPUT:')
    print(output_text)
    print('\nERROR:')
    print(error_text)


def clearLogs():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    error_log_path = os.path.join(script_dir, 'conf/error.log')
    output_log_path = os.path.join(script_dir, 'conf/output.log')

    with open(error_log_path, 'w') as file:
        file.close()
    with open(output_log_path, 'w') as file:
        file.close()

    print('The application logs were cleared!')
