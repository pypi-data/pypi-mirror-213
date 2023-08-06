import inspect
from datetime import datetime

from .log import log

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

    def getInfo(self):
        self.targetName = self.func.__name__

        self.target.signature = inspect.signature(self.func)
        self.targetArgs = list(self.target.signature.parameters.keys())

        self.target.as_string = self.func.__doc__

        self.target.is_method = inspect.ismethod(self.func)

        self.target.is_generator = inspect.isgeneratorfunction(self.func)

        self.target.source_code = inspect.getsource(self.func)

        self.target.source_location = inspect.getsourcelines(self.func)

        self.targetFilename = self.target.source_location[0]
        self.targetLineNumber = self.target.source_location[1]

        self.targetModule = inspect.getmodule(self.func).__name__

        targetInfo = {
            "name": self.targetName,
            "arguments": self.targetArgs,
            "file_name": self.targetFilename,
            "line_number": self.targetLineNumber,
            "module": self.targetModule
        }

        return targetInfo

    def meter(self, args: list = None, loops: int = 1):
        self.logStream.skipLine()

        self.logStream.add(f'Meter: Loading args... {args}')

        self.count = 0

        if args is not None:
            for argPack in args:
                result = self.run(argPack, loops)
        else:
            result = self.run(None, loops)

        return result


    def run(self, argPack, loops):
        for i in range(loops):

            self.count += 1
            self.loopCount += 1

            startTime = datetime.now()

            self.logStream.skipLine()
            self.logStream.add(f'Meter Execution Count: {self.count}')
            self.logStream.add(f"Meter Execution Starts at: {startTime}")
            self.logStream.add(f"Meter Execution Args: {argPack}")

            try:
                if argPack is None:
                    executionResult = str(self.func())
                elif not isinstance(argPack, str):
                    executionResult = str(self.func(*argPack))
                elif isinstance(argPack, str):
                    executionResult = str(self.func(argPack))
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

            return executionResult