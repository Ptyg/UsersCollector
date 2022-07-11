import datetime
import time


class Log:
    info_tag = '[INFO]'
    warning_tag = '[WARNING]'
    error_tag = '[ERROR]'
    countdown_tag = '[COUNTDOWN]'

    @staticmethod
    def print_info_msg(msg: str) -> None:
        print(f'{datetime.datetime.now()} {Log.info_tag} {msg}')
    
    @staticmethod
    def print_warning_msg(msg: str) -> None:
        print(f'{datetime.datetime.now()} {Log.warning_tag} {msg}')

    @staticmethod
    def print_error_msg(exception: Exception = None, msg: str = None) -> None:
        if exception:
            if exception.__doc__ != None and msg:
                print(f'{datetime.datetime.now()} {Log.error_tag} \n {exception.__doc__}\n{Log.error_tag}: {msg}')
            elif msg: 
                print(f'{datetime.datetime.now()} {Log.error_tag}: {msg}')
        else:
            print(f'{datetime.datetime.now()} {Log.error_tag}: {msg}')

    @staticmethod
    def print_countdown(start_number: int = 3):
        print(f'{Log.countdown_tag} Continue work in...')
        for i in range(start_number, 0, -1):
            print(f'{Log.countdown_tag} {i}...')
            time.sleep(1)
