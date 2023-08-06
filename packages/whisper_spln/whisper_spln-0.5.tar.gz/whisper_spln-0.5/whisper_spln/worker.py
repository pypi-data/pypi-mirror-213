from threading import Event, Thread
from time import sleep
import whisper
from googletrans import Translator
from whisper_spln.lockedQueue import lockedQueue


class Worker(Thread):

    def __init__(self, shared_queue: lockedQueue, event_shutdown: Event):
        Thread.__init__(self)
        self.shared_queue = shared_queue
        self.event_shutdown = event_shutdown
        self.shutdown = False
        self.model = whisper.load_model("base")
        self.translator = Translator()

    def run(self):
        print("Worker started")
        while not self.shutdown:
            self.process_queue()
            sleep(20)  # Sleep for 20 seconds to wait for more work
            self.process_queue()
        self.shared_queue.saveTime()
        self.event_shutdown.set()
        print("Worker stopped")

    def translate(self, text, dest):
        return self.translator.translate(text, dest=dest).text

    def process_queue(self):
        self.shutdown = True if self.shared_queue.empty() else False

        while not self.shared_queue.empty():
            dict = self.shared_queue.get()
            dest_folder = dict["dest_folder"]
            filename = dict["filename"]
            inputLang = dict["input_lang"]
            outputLang = dict["output_lang"]
            print("Handling ------>", filename)
            try:
                if inputLang != None:
                    result = self.model.transcribe(
                        filename, fp16=False, language=inputLang)["text"]
                else:
                    result = self.model.transcribe(
                        filename, fp16=False)["text"]
                if outputLang != None:
                    result = self.translate(result, outputLang)
                self.shared_queue.calculteNewMean()
                result = result.replace(". ", ".\n")

            except Exception as e:
                result = f"Error: {e}"
                self.shared_queue.stopRunning()
            open(dest_folder, "a").write(f"{result}\n")
