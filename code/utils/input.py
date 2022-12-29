import getpass
from colorama import Fore, Style, init
init(autoreset=True)

class Input:
    @staticmethod
    def input(msg: str, input_tag: str = '[INPUT]') -> str:
        return input(f'{Fore.BLUE}{Style.BRIGHT}{input_tag}{Style.RESET_ALL} {msg}: ')

    @staticmethod
    def input_hidden(msg: str, input_tag: str = '[INPUT]') -> str:
        return getpass.getpass(f'{Fore.BLUE}{Style.BRIGHT}{input_tag}{Style.RESET_ALL} {msg}: ')
