import argparse
from whisper_spln.parserTasks import clearLogs, getLogs, getQueue, runWhisper


def main():
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
    parser.add_argument('-q', '--queue', action=QueueAction,
                        help='Show the audio conversion queue')
    parser.add_argument('-l', '--logs', action=LogsAction,
                        help='Show the execution logs')
    parser.add_argument('-cl', '--clearLogs', action=ClearLogsAction,
                        help='Clear logs')
    # Parse the command-line arguments
    args = parser.parse_args()
    # Access the values of the arguments
    input_file = args.input_file
    dest_folder = args.dest
    inputLang = args.inputLang
    outputLang = args.outputLang

    runWhisper(input_file, dest_folder, inputLang, outputLang)


class QueueAction(argparse.Action):
    def __init__(self, option_strings, dest, **kwargs):
        return super().__init__(option_strings, dest, nargs=0, default=argparse.SUPPRESS, **kwargs)

    def __call__(self, parser, namespace, values, option_string, **kwargs):
        getQueue()
        parser.exit()


class LogsAction(argparse.Action):
    def __init__(self, option_strings, dest, **kwargs):
        return super().__init__(option_strings, dest, nargs=0, default=argparse.SUPPRESS, **kwargs)

    def __call__(self, parser, namespace, values, option_string, **kwargs):
        getLogs()
        parser.exit()


class ClearLogsAction(argparse.Action):
    def __init__(self, option_strings, dest, **kwargs):
        return super().__init__(option_strings, dest, nargs=0, default=argparse.SUPPRESS, **kwargs)

    def __call__(self, parser, namespace, values, option_string, **kwargs):
        clearLogs()
        parser.exit()


if __name__ == '__main__':
    main()
