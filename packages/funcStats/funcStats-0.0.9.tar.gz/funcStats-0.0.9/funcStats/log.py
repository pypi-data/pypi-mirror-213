import os
from datetime import datetime

class log:

    def __init__(self, filepath, victim, mode: str, header: str = "[Info]"):
        self.mode = mode
        self.header = header
        self.filepath = filepath
        self.targetName = f"[{victim}]"

        if filepath is not None:
            self.logStream = open(os.path.join(os.path.dirname(os.path.abspath(self.filepath)), f'{self.filepath} - {datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log'),
                                'w')

    def skipLine(self):
        if 'toFile' in self.mode:
            self.logStream.seek(0, 2)
            self.logStream.write('\n')
            self.logStream.truncate()

        if 'console' in self.mode:
            print('')

    def write(self, text):
        self.currentContent = f"{self.header} {datetime.now()} - {self.targetName} - {str(text)}"

        if 'toFile' in self.mode:
            os.makedirs(os.path.dirname(os.path.abspath(self.filepath)), exist_ok=True)
            self.logStream.write(f'{self.currentContent}\n')
            self.logStream.truncate()

        if 'console' in self.mode:
            print(self.currentContent)

    def add(self, text):
        self.write(text)
