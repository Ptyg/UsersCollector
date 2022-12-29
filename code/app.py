import time
import os
import aminofix as af
import pyfiglet as pf

from utils.input import Input
from utils.log import Log
from utils.utils import login, chooseCom, Save
from collecting import Public, Container

class App:
    @staticmethod
    def __clearScreen() -> None:
        os.system('cls' if os.name == 'nt' else 'clear')


    @staticmethod
    def __startCli() -> str:    
        App.__clearScreen()        
        print(pf.figlet_format("Users collector"))
        
        print('1. Collect users')
        print('2. FAQ')
        print('E. Exit')
        return Input.input('Choice')


    @staticmethod
    async def __printFaq() -> None:
        App.__clearScreen()
        print(pf.figlet_format("FAQ"))
        print('> Does the script steals my login data?\n\tNo, you can check the code\n')
        print('> How long does it takes to collect users?\n\tIt depends on the amount'\
                ' of users in community\n\tThe most long part - when collect followers & following'\
                '\n\tfrom each user and then followers & following from\n\tprev followers'\
                ' & following and then... You got it\n')
        print('> Does it collect ALL users from community?\n\tThere`s no guarantee for all'\
                ', BUT quite a lot\n')
        print('> How the results will be saved?\n\tIn csv \ json \ MySql \ MongoDb, you can choose\n')
        print('> If i press Ctrl+c during collecting, what will happen?\n\tWell, nothing - collected users will be saved.')
        Input.input('Press any key to continue...')
        return


    @staticmethod
    async def __collectUsers() -> None:
        savingTypeChoice = {
            'c': Save.saveCsv,
            'j': Save.saveJson,
            's': Save.saveSql,
            'm': Save.saveMongo
        }

        App.__clearScreen()
        print(pf.figlet_format("Start"))

        while True:
            savingType = Input.input('File format for result: csv(c) / json(j) / mysql(s) / mongo(m)').lower()
            if savingType == 'c' or savingType == 'j' or savingType == 's' or savingType == 'm':
                break

        email = Input.input('Email')
        password = Input.input_hidden('Password')
        
        try:
            client = await login(email, password)
            subClient = await chooseCom(client)
            responses = await Public(subClient).getFromPublic()
            users, dict_with_unique_users = await Container(subClient).collectFromResponses(responses)
                    
            Log.print_info_msg('Users info from public is collected')
            Log.print_info_msg(f'Current amount of users: { str(len(users)) }')
            Log.print_info_msg('Collecting each user`s followers and following...')
            Log.print_countdown()

            users, _ = await Container(subClient).getFollowersAndFollowing(users, dict_with_unique_users)
        except KeyboardInterrupt:
            pass
        except Exception as e:
            Log.print_error_msg(exception=e)
            Input.input('Press any key to continue...')
            return
            
        commName = await subClient.get_community_info(subClient.comId)
        savingTypeChoice.get(savingType)(commName.name, users)
        

    @staticmethod
    async def run() -> None:
        choice_list = {
            '1': App.__collectUsers,
            '2': App.__printFaq,
            'E': exit,
        }
        while True:
            try:
                choice = App.__startCli().upper()
                await choice_list.get(choice)()
            except TypeError:
                pass

        return






