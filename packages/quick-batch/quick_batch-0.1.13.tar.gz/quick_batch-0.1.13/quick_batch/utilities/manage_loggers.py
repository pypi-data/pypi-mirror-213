import functools
import sys
import datetime
import re


class LogExceptions:
    def __init__(self):
        # self.file_path = file_path
        pass

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            try:
                result = func(*args, **kwargs)           
            except Exception as e:
                # with open(self.file_path, 'a') as file:
                #     file.write(f"FAILURE: {func_name} failed: {e}\n")
                #     traceback.print_exc(file=file)
                print(f"FAILURE: {func_name} failed: {e}")
            else:
                # with open(self.file_path, 'a') as file:
                #     file.write(f"SUCCESS: {func_name} succeeded\n")
                print(f"SUCCESS: {func_name} succeeded")
                return result
        return wrapper


def decorate_methods(decorator):
    def decorate(obj):
        if isinstance(obj, type):
            # Decorate class methods
            for name, method in vars(obj).items():
                if callable(method):
                    setattr(obj, name, decorator(method))
            return obj
        else:
            # Decorate standalone functions
            return decorator(obj)
    return decorate


class Logger(object):
    def __init__(self, log_file):
        self.terminal = sys.stdout
        self.log_file = log_file
        self.log = None
        self.previous_message = ""

    def open_log(self):
        self.log = open(self.log_file, "a")

    def write(self, message):
        timestamp = datetime.datetime.now().replace(microsecond=0)  # Ignore milliseconds
        message_lines = message.splitlines()
        
        if self.previous_message.endswith("\n"):
            message_with_timestamp = "\n".join(f"{timestamp} - {line}" for line in message_lines)
        else:
            message_with_timestamp = "\n".join(f"\n{timestamp} - {line}" for line in message_lines)
            
        self.previous_message = message_with_timestamp
        self.terminal.write(message_with_timestamp)
        self.terminal.flush()  # Flush the terminal output
        if self.log is not None:
            self.log.write(message_with_timestamp)
            self.log.flush()  # Flush the log file output



    def flush(self):
        pass

    def close_log(self):
        if self.log is not None:
            self.log.close()
            self.log = None  # Set log attribute to None to prevent further writing
