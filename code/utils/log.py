from datetime import datetime
import time

from colorama import Fore, Style, init
init(autoreset=True)

class Log:
     @staticmethod
     def print_info_msg(msg: str, info_tag: str = '[INFO]') -> None:
        print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} {Fore.GREEN}{Style.BRIGHT}{info_tag}{Style.RESET_ALL} {msg}')


     @staticmethod
     def print_warning_msg(msg: str, warning_tag: str = '[WARNING]') -> None:
        print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} {Fore.YELLOW}{Style.BRIGHT}{warning_tag}{Style.RESET_ALL} {msg}')


     @staticmethod
     def print_error_msg(msg: str = 'Error occurred', error_tag: str = '[ERROR]',
                         exception: Exception = None) -> None:
        if exception.__doc__ != None:
            print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' '\
                  + Fore.RED + Style.BRIGHT + error_tag + Style.RESET_ALL + '\n'\
                  + exception.__doc__ + '\n' + msg)
            return

        print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' '\
                + Fore.RED + Style.BRIGHT + error_tag + Style.RESET_ALL + '\n'\
                + msg)
        

     @staticmethod
     def print_countdown(start_number: int = 3, countdown_tag: str = '[COUNTDOWN]'):
        print(f'{Fore.MAGENTA}{Style.BRIGHT}{countdown_tag}{Style.RESET_ALL} Continue work in...')
        for i in range(start_number, 0, -1):
            print(f'{Fore.MAGENTA}{Style.BRIGHT}{countdown_tag}{Style.RESET_ALL} {i}...')
            time.sleep(1)



