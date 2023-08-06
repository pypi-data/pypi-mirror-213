"""
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
"""
__version__ = "0.5"
