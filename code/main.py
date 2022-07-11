import csv
import asyncio
import requests
import datetime
import time
import aminofix as af

import collecting
import chooseCommunity as cc
from log import Log
import getInfoFromUsers as gifu


def get_device_id():
    '''
    Get device id

    Params:
        None

    Success: 
        returns device id

    Fail: 
        raise exeption
    '''
    Log.print_info_msg('Get device id')

    try:
        id = requests.get("https://ka-generator.herokuapp.com/device").text
    except requests.exceptions.Timeout as e:
        raise e
    except requests.exceptions.TooManyRedirects as e:
        raise e
    except requests.exceptions.RequestException as e:
        raise e

    return id


async def login(email: str, password: str):
    '''
    Log in into account

    Params:
        email - email to enter
        password - password for email to enter

    Success
        return client of app

    Fail:
        return None and to exit

    All exception are handled there. So just returns `None` like a sign exception was there
    '''
    try:
        Log.print_info_msg('Attempt to log in in with random device id')
        dev_id = get_device_id()
        client = af.asyncfix.Client(deviceId=dev_id)
        
        await client.login(email, password)
        Log.print_info_msg('Logged in')
        
        return client
    except af.exceptions.InvalidDevice:
        Log.print_error_msg(msg='Random device id not worked. Attempt to log in without it...')
        client = af.asyncfix.Client()
    except af.exceptions.AccountLimitReached:
        Log.print_error_msg(msg='To much attemts. Plese try again in 5 minutes')
        return None
    except requests.exceptions.Timeout as e:
        Log.print_error_msg(msg='The request timed out')
        return None
    except requests.exceptions.TooManyRedirects as e:
        Log.print_error_msg(msg='To many redirects')
        return None
    except requests.exceptions.RequestException as e:
        Log.print_error_msg(msg='There was an ambiguous exception that occurred while handling your request')
        return None


    try:
        await client.login(email, password)
        Log.print_info_msg('Logged in')
        return client
    except (af.exceptions.InvalidEmail, af.exceptions.InvalidPassword):
        Log.print_error_msg(af.exceptions.InvalidEmail, 'Invalid input data. Check your email and password. Exit...')
        return None
    except af.exceptions.AccountLimitReached:
        Log.print_error_msg(msg='To much attemts. Plese try again in 5 minutes')
        return None
    except Exception as e:
        Log.print_error_msg(e, 'Exception occured. Exit...')
        return None


async def save_in_csv(fileName: str, users: list) -> None:
    fieldnames_csv = ['Nick', 'Id', 'Level', 'Blogs count', 'Comments count', 'Followers count', 
                      'Following count', 'Posts count', 'Created time']
    
    with open(fileName, 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames_csv)
        writer.writeheader()
        writer.writerows(users)


async def main():
    
    what_collect = {
    #    list of things where users can be collected from community. Free to add more functions
    #    in some functions extra param must be specified:
    #    example:
    #        subClient.get_leaderboard_info(extra) - in this function leader type must be written.
    #                                                Or leader by reputation (rep), or the most active by day (24)

        '24': collecting.addingLeaderboard,
        '7': collecting.addingLeaderboard,
        'rep': collecting.addingLeaderboard,
        'check': collecting.addingLeaderboard,
        'quiz': collecting.addingLeaderboard,
        'leaders': collecting.getAllUsers,
        'recent': collecting.getAllUsers,
        'curators': collecting.getAllUsers,
        'online': collecting.getOnlineUsers,
        'blogs': collecting.getRecentBlogs,
        'publicChats': collecting.getPublicChatThreads,
        'best_quiz': collecting.getBestQuiz,
        'trending_quiz': collecting.getTrendingQuiz,
        'wikis': collecting.getRecentWikiItems,
        'private_chats': collecting.getPrivateChats
    }

    ########################## login ##########################################################

    email = input('[INPUT] Email: ')
    password = input('[INPUT] Password: ')
    
    client = await login(email, password)
    if client == None:
        return

    subClient, comId = await cc.chooseCom(client)

    ########################## COLLECT FROM DICTIONARY 'what_collect' #########################
    
    Log.print_info_msg('Start collecting users from public in...')
    Log.print_countdown()
    
    tasks = []
    for key, func in what_collect.items():
        curr_task = asyncio.create_task(func(subClient, key))
        tasks.append(curr_task)

    responses = await asyncio.gather(*tasks, return_exceptions=True)    
    
    Log.print_info_msg('Users from public is collected. Start gather info in...')
    Log.print_countdown()

    users_id_and_nick_to_check_for_duplicate, users_for_csv = await gifu.get_info_from_users_after_public_gather(subClient, responses)
    
    tasks.clear()
    Log.print_info_msg('Users from public is collected')
    Log.print_info_msg('Current amount of users - ' + str(len(users_for_csv)))
    Log.print_info_msg('Want to save current data or continue gather followers & following of each user?')
    choice = input('[INPUT] Choice (S(safe) \ C(continue)): ') 

    communityInfo = await subClient.get_community_info(comId)
    fileName = communityInfo.name + '_'+ time.strftime("%Y.%m.%d") + '.csv'
    if choice == 'S' or choice == 'safe' or choice == 'Safe' or choice == 's':
        Log.print_info_msg('Filename is - ' + fileName)
        Log.print_info_msg('Saving data...')
        await save_in_csv(fileName, users_for_csv)
        Log.print_info_msg('Data is saved...')
        return

    Log.print_info_msg('Sleep for 5 minutes before get followers and following')
    await asyncio.sleep(60 * 5)

    Log.print_info_msg('Start collecting users` followers and following users in...')
    Log.print_countdown()

     
    is_collected = False
    lastKey = None

    while not is_collected:
        is_collected, lastKey = await collecting.getFollowersAndFollowingFromUsersDict(subClient, users_for_csv, users_id_and_nick_to_check_for_duplicate, lastKey)

    Log.print_info_msg('User is collected')
    Log.print_info_msg('Filename is - ' + fileName)
    Log.print_info_msg('Saving data...')
    await save_in_csv(fileName, users_for_csv)
    Log.print_info_msg('Data is saved...')



    try:
        await client.logout()
        Log.print_info_msg('Logged out')
        print(f'{datetime.datetime.now()} [SCRIPT WORK IS DONE]')
        print(f'{datetime.datetime.now()} [CONTACTS] Github - https://github.com/Ptyg, Discord - Gtyp#2934')
    except Exception as e:
        Log.print_error_msg(msg='Oh, exception occured, nvm, you can just kill the process. All job is done')
        print(f'{datetime.datetime.now()} [SCRIPT WORK IS DONE]')
        print(f'{datetime.datetime.now()} [CONTACTS] Github - https://github.com/Ptyg, Discord - Gtyp#2934')
        await asyncio.sleep(5 * 60)
        await client.logout()


if __name__ == '__main__':
    asyncio.run(main())