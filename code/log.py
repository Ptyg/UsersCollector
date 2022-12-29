import datetime
import time


class Log:
     __slots__ = ('info_tag', 'warning_tag', 'error_tag', 'countdown_tag')


     def print_info_msg(self, msg: str) -> None:
        print(f'{datetime.datetime.now()} {Log.info_tag} {msg}')


     def print_warning_msg(self, msg: str) -> None:
        print(f'{datetime.datetime.now()} {self.warning_tag} {msg}')


     def print_error_msg(self, exception: Exception = None, msg: str = None) -> None:
        if exception:
            if exception.__doc__ != None and msg:
                print(f'{datetime.datetime.now()} {self.error_tag} \n {exception.__doc__}\n{self.error_tag}: {msg}')
            else: 
                print(f'{datetime.datetime.now()} {self.error_tag}: {msg}')
        else:
            print(f'{datetime.datetime.now()} {self.error_tag}: {msg}')


     def print_countdown(self, start_number: int = 3):
        print(f'{self.countdown_tag} Continue work in...')
        for i in range(start_number, 0, -1):
            print(f'{self.countdown_tag} {i}...')
            time.sleep(1)


     def __init__(self, info_tag: str = '[INFO]', warning_tag: str = '[WARNING]', 
                  error_tag: str = '[ERROR]', countdown_tag: str = '[COUNTDOWN]'):
         self.info_tag = info_tag 
         self.warning_tag = warning_tag 
         self.error_tag = error_tag
         self.countdown_tag = countdown_tag

