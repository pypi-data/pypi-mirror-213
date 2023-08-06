
from threading import Event
from whisper_spln.worker import Worker
from whisper_spln.lockedQueue import lockedQueue
from whisper_spln.listener import Listener
import sys
import argparse


def start_threads():
    parser = argparse.ArgumentParser(
        prog='AudioToText',
        description='Converts an audio file to text file.',
        epilog='Made for SPLN 2022/2023'
    )

    # Add arguments
    parser.add_argument('input_file', type=str,
                        help='Path to the file with the audio')
    parser.add_argument('-d', '--dest', type=str, default='result.txt',
                        help='Path for the output file')
    parser.add_argument('-il', '--inputLang', type=str,
                        help='Language of the input file')
    parser.add_argument('-ol', '--outputLang', type=str,
                        help='Language of the output text')

    args = parser.parse_args()
    # Access the values of the arguments
    input_file = args.input_file
    dest_folder = args.dest
    inputLang = args.inputLang
    outputLang = args.outputLang

    dict = {
        "filename": input_file,
        "output_lang": outputLang,
        "dest_folder": dest_folder,
        "input_lang": inputLang
    }
    event_shutdown = Event()
    shared_queue = lockedQueue()
    shared_queue.put(dict)
    listener = Listener(shared_queue, event_shutdown)
    worker = Worker(shared_queue, event_shutdown)

    listener.start()
    worker.start()


start_threads()
