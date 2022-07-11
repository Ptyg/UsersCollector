import datetime
import asyncio
from log import Log


async def getTrendingQuiz(subClient, who):
    '''
    
    Collect trending quiz

    Params:
        subClient - comumunity client class object to execute function
        who - unusefull param, because of dict implementation in main (what_collect: dict)
              Not a bug, but it`s need to be here for correct work in `for loop` in main
              Look for `COLLECT FROM DICTIONARY` section in main   

    Success:
        returns trending quiz
        
    Fail: 
        returns exeption

    '''
    Log.print_info_msg('Get trending quiz')    
    try:
        myList = await subClient.get_trending_quiz(size=999)
    except Exception as e:
        Log.print_error_msg(e)
        return e

    return myList


async def getBestQuiz(subClient, who):
    '''
    
    Collect best quiz

    Params:
        subClient - comumunity client class object to execute function
        who - unusefull param, because of dict implementation in main (what_collect: dict)
              Not a bug, but it`s need to be here for correct work in `for loop` in main
              Look for `COLLECT FROM DICTIONARY` section in main   

    Success:
        returns best quiz
        
    Fail: 
        returns exeption

    '''
    Log.print_info_msg('Collect best qiuz')
    try:
        myList = await subClient.get_best_quiz(size=999) 
    except Exception as e:
        Log.print_error_msg(e)
        return e

    return myList


async def getPublicChatThreads(subClient, who):
    '''
    
    Collect public chats

    Params:
        subClient - comumunity client class object to execute function
        who - unusefull param, because of dict implementation in main (what_collect: dict)
              Not a bug, but it`s need to be here for correct work in `for loop` in main
              Look for `COLLECT FROM DICTIONARY` section in main   

    Success:
        returns public chats threads
        
    Fail: 
        returns exeption
    
    '''
    Log.print_info_msg('Collect public chats')
    try:
        myLists = await subClient.get_public_chat_threads(size=999)
    except Exception as e:
        Log.print_error_msg(e)
        return e

    return myLists


async def addingLeaderboard(subClient, myType):
    '''
    
    Collect leaders 

    Params:
        subClient - comumunity client class object to execute function
        myType - type of leaders in leaderboard to collect

    Success:
        returns leaders from leaderboard
        
    Fail: 
        returns exeption
    
    '''
    Log.print_info_msg(f'Collect leaders: {myType}')
    try:
        myList = await subClient.get_leaderboard_info(myType, size=999)  # .userId
    except Exception as e:
        Log.print_error_msg(e)
        return e

    return myList


async def getRecentBlogs(subClient, who):
    '''
    
    Collect recent blogs

    Params:
        subClient - comumunity client class object to execute function
        who - unusefull param, because of dict implementation in main (what_collect: dict)
              Not a bug, but it`s need to be here for correct work in `for loop` in main
              Look for `COLLECT FROM DICTIONARY` section in main   

    Success:
        returns recent blogs
        
    Fail: 
        returns exeption
    
    '''
    Log.print_info_msg('Collecting recent blogs authors')
    try:
        result = await subClient.get_recent_blogs(size=999)  # .author.userId
    except Exception as e:
        Log.print_error_msg(e)
        return e
    
    return result


async def getOnlineUsers(subClient, who):
    '''
    
    Collect online users

    Params:
        subClient - comumunity client class object to execute function
        who - unusefull param, because of dict implementation in main (what_collect: dict)
              Not a bug, but it`s need to be here for correct work in `for loop` in main
              Look for `COLLECT FROM DICTIONARY` section in main   

    Success:
        returns online users
        
    Fail: 
        returns exeption
    
    '''
    Log.print_info_msg('Collecting online users')
    try:
        result = await subClient.get_online_users(size=999)  # .profile.userId
    except Exception as e:
        Log.print_error_msg(e)
        return e

    return result


async def getRecentWikiItems(subClient, who):
    '''
    
    Collect recent wiki

    Params:
        subClient - comumunity client class object to execute function
        who - unusefull param, because of dict implementation in main (what_collect: dict)
              Not a bug, but it`s need to be here for correct work in `for loop` in main
              Look for `COLLECT FROM DICTIONARY` section in main   

    Success:
        returns recent wiki
        
    Fail: 
        returns exeption
    
    '''
    Log.print_info_msg('Collecting recent wiki')
    try:
        result = await subClient.get_recent_wiki_items(size=999)  # author.userId  author.nickname
    except Exception as e:
        Log.print_error_msg(e)
        return e

    return result


async def getAllUsers(subClient, myType: str):
    '''
    
    Collect all users

    Params:
        subClient - comumunity client class object to execute function
        myType - type of users in community   

    Success:
        returns list of users
        
    Fail: 
        returns exeption
    
    '''
    Log.print_info_msg('Collecting users')
    try:
        result = await subClient.get_all_users(myType, size=999)  # .profile.userId
    except Exception as e:
        Log.print_info_msg(e)
        return e

    return result


async def getUserFollowers(subClient, id: str, who: str = None):
    '''
    
    Collect user`s followers

    Params:
        subClient - comumunity client class object to execute function
        who - user`s nick
        id - users`s id

    Success:
        returns users
        
    Fail: 
        returns exeption
    
    '''
    Log.print_info_msg(f'{who}`s followers')
    try:
        result = await subClient.get_user_followers(id, size=999)
    except Exception as e:
        Log.print_error_msg(e)
        return e

    return result


async def getUserFollowing(subClient, id: str, who: str = None):
    '''
    
    Collect user`s following

    Params:
        subClient - comumunity client class object to execute function
        who - user`s nick
        id - users`s id

    Success:
        returns users
        
    Fail: 
        returns exeption
    
    '''
    Log.print_info_msg(f'{who}`s following')
    try:
        result = await subClient.get_user_following(id, size=999)
    except Exception as e:
        Log.print_error_msg(e)
        return e

    return result


async def getPrivateChats(subClient, who):
    '''
    
    Collect account chats

    Params:
        subClient - comumunity client class object to execute function
        who - unusefull param, because of dict implementation in main (what_collect: dict)
              Not a bug, but it`s need to be here for correct work in `for loop` in main
              Look for `COLLECT FROM DICTIONARY` section in main   

    Success:
        returns private chats
        
    Fail: 
        returns exeption
    '''

    Log.print_info_msg('Collecting from privates chat')
    try:
        result = await subClient.get_chat_threads(size=999)
    except Exception as e:
        Log.print_error_msg(e)
        return e

    return result

        
async def getFollowersAndFollowingFromUsersDict(subClient, listOfUserInCsvStructure: list, originDict: dict, start: str = None):
    '''
    Get followers and followee from users in dict

    Params:
        listOfUserInCsvStructure - list of users in custom csv structure
            Example:
                csv = [{
                    'Name': Test,
                    'Age': 12,
                    ...
                },
                ...]
        originDict - dict with userId and nick of users to check for duplicates
        start - start key in originDict

    Returns:
        flags if all possible followers and followee is collected. If not - returns flag and id to start from 
    '''
    
    dictToIterate = originDict

    if start != None:
        # not the most efficient way to make a dictionary copy with a filter, but it works
        # if needs to be faster - good idea to look this 'if' scope
        ok = False
        originDictSlice = {}
        for id, nick in originDictSlice.items():
            if id == start:
                ok = True
            if ok:
                originDictSlice.update({id: nick})
        dictToIterate = originDictSlice 
    
    tasks = []
    CHUNK = 500
    curr_chunk_size = 1
    newFollowersAndFollowing = {}

    for id, nick in dictToIterate.items():
        curr_task1 = asyncio.create_task(getUserFollowers(subClient, id, nick))
        curr_task2 = asyncio.create_task(getUserFollowing(subClient, id, nick))

        tasks.append(curr_task2)
        tasks.append(curr_task1)
        curr_chunk_size += 2

        if curr_chunk_size >= CHUNK:
            responses = await asyncio.gather(*tasks, return_exceptions=True)

            for i in responses:
                for user_nick, user_id, level, blogs_count, comm_count, followers_count, following_count, post_count, created_time in zip(i.nickname, i.userId, i.level, i.blogsCount, i.commentsCount, i.followersCount, i.followingCount, i.postsCount, i.createdTime):
                    if (user_id not in originDict) and (user_id not in newFollowersAndFollowing):
                        newFollowersAndFollowing.update({user_id: user_nick})
                        listOfUserInCsvStructure.append({
                            'Nick': user_nick,
                            'Id': user_id,
                            'Level': level,
                            'Blogs count': blogs_count,
                            'Comments count': comm_count,
                            'Followers count': followers_count,
                            'Following count': following_count,
                            'Posts count': post_count,
                            'Created time': created_time
                        })
                        Log.print_info_msg(user_nick + ' is added')
            
            tasks.clear()
            curr_chunk_size = 1

            Log.print_warning_msg('In order to prevent temporary ip ban - sleeping for 5 minutes')
            Log.print_info_msg('Current number of users - ' + str(len(listOfUserInCsvStructure)))
            await asyncio.sleep(5 * 60)
            
            Log.print_countdown()
    
    originDictLen = len(originDict)
    originDict.update(newFollowersAndFollowing)
    originDictLenNew = len(originDict)

    if (originDictLen < originDictLenNew):
        return False, list(newFollowersAndFollowing.keys())[0]
    return True, None





