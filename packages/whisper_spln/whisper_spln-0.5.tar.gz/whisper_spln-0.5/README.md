# Whisper

Whisper SPLN is a remote service that allows a user to transcrive audio files to text using whisper from openai.
The user can make various requests to the server, such as transcribing a file, getting the status of the queue, and getting the logs of the application.
It is also possible to translate the transcrived text to a language chosen by the user.

Possible Commands:
Transcribe: transcribes an audio file to text.
Variables:
input_file (obrigatory): path for the audio file to transcrive.
dest (-d, --dest, optional): defines the path for the output file.
inputLang (-il, --inputLang, optional): defines the language of the input file if not defined, the whisper assumes the language.
outputLang (-ol, --outputLang, optional): defines the language of the output text, if not defined the output language is the one used in the audio file.

    queue (-q, --queue, optional): shows the audio conversion queue.
    logs (-l, --logs, optional): shows the execution logs.
    clearLogs (-cl, --clearLogs, optional): clear the execution logs.

# Example
    whisper_spln input_file
    whisper_spln input_file -d output_file -il input_language -ol output_language

# Source Code

To work whisper will do 1 of 2 things:

- whisper will first create 2 threads, one for the listener and one for the worker.
- If the 2 threads are already running, whisper will send the request to the queue.

Files:

- listener.py -> listener class that listens for requests and sends them to the queue.
- lockedQueue.py -> locked queue class that stores the requests whit locks to secure the access from both threads.
- worker.py -> worker class that gets the requests from the queue and executes them.
- main.py -> argparse of the service, it has different classes to handle different arguments
- parserTasks.py -> functions that handle different arguments of the argparse
- startThreads.py -> tries to access or initializes the threads that will run Whisper
