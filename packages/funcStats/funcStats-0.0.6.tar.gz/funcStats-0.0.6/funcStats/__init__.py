import inspect
from datetime import datetime

from funcStats.log import log

def info():
    return None


class monitor:

    def __init__(self, target: any = None, console: bool = True, toFile: str = None):

        # arguments loading
        self.func = target
        self.console = console
        self.toFile = toFile
        self.count = 0

        # default definitions to overwrite
        self.target = info
        self.loopCount = 1

        # more complex stuff
        #self.thread = Thread(target=target, args=args)

        if self.func is None:
            raise Exception("Monitor needs a method to watch, please use the 'target' argument or the first positional "
                            "argument to set it.")
        else:
            try:

                self.mode = ''

                if console:
                    self.mode += 'console'
                if toFile is not None:
                    self.mode += 'toFile'

                self.targetInfo = self.getInfo()

                self.logStream = log(self.toFile, victim=self.targetName, header='[FuncStats Report]', mode=self.mode)

                self.logStream.add(f"Target Info: {self.targetInfo}")

            except TypeError:
                raise Exception("Impossible to monitor. Not a function or method provided.")


    def start(self):
        self.thread.start()
        self.thread.join()

    def getInfo(self):
        # Get the function's name
        self.targetName = self.func.__name__

        # Get the function's arguments
        self.target.signature = inspect.signature(self.func)
        self.targetArgs = list(self.target.signature.parameters.keys())

        # Get the function's docstring
        self.target.as_string = self.func.__doc__

        # Check if the function is a method
        self.target.is_method = inspect.ismethod(self.func)

        # Check if the function is a generator
        self.target.is_generator = inspect.isgeneratorfunction(self.func)

        # Get the function's source code
        self.target.source_code = inspect.getsource(self.func)

        # Get the file name and line number where the function is defined
        self.target.source_location = inspect.getsourcelines(self.func)

        self.targetFilename = self.target.source_location[0]
        self.targetLineNumber = self.target.source_location[1]

        # Get the function's module name
        self.targetModule = inspect.getmodule(self.func).__name__

        # Create a dictionary to store the information
        targetInfo = {
            "name": self.targetName,
            "arguments": self.targetArgs,
            "file_name": self.targetFilename,
            "line_number": self.targetLineNumber,
            "module": self.targetModule
        }

        return targetInfo

    def meter(self, args: list, loops: int = 1):
        self.logStream.skipLine()

        self.logStream.add(f'Meter: Loading args... {args}')

        self.count = 0

        for argPack in args:

            for i in range(loops):

                self.count += 1
                self.loopCount += 1

                startTime = datetime.now()

                self.logStream.skipLine()
                self.logStream.add(f'Meter Execution Count: {self.count}')
                self.logStream.add(f"Meter Execution Starts at: {startTime}")
                self.logStream.add(f"Meter Execution Args: {argPack}")

                try:
                    executionResult = str(self.func(*argPack))
                except Exception as e:
                    executionResult = e

                self.logStream.add(f"Meter Execution Returns: {str(executionResult)}...")

                endTime = datetime.now()

                duration = endTime - startTime

                hours = duration.seconds // 3600
                minutes = (duration.seconds % 3600) // 60
                seconds = duration.seconds % 60
                milliseconds = duration.microseconds // 1000

                self.logStream.add(f"Meter Execution Takes: {hours}h {minutes}m {seconds}s {milliseconds}ms")
                self.logStream.skipLine()
