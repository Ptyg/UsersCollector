from tracemalloc import start
import typing
import aminofix as af
import asyncio
import time

from utils.log import Log


TREND_QUIZ_LIST_SIZE, BEST_QUIZ_LIST_SIZE = 999, 999
CHAT_LIST_SIZE, LEADERS_TYPE_LIST_SIZE = 999, 999
RECENT_BLOGS_LIST_SIZE, ONLINE_USERS_LIST_SIZE = 999, 999
RECENT_WIKI_ITEMS_LIST_SIZE, TYPED_ALL_USERS_LIST_SIZE = 999, 999
USER_FOLLOWERS_LIST_SIZE, USER_FOLLOWING_LIST_SIZE = 999, 999
USER_FROM_CHAT = 999
CURRENT_REQUEST_ITER, MAX_REQUEST_CHUNK = 0, 500


class Public:
    __slots__ = ('subClient', )
    

    def __init__(self, subClient: af.asyncfix.SubClient):
        self.subClient = subClient
    

    async def getFromPublic(self) -> list:
        global CURRENT_REQUEST_ITER
        Log.print_info_msg('Collect users from public...')
        Log.print_countdown()
        
        funcs_without_params = (
            self.getTrendingQuiz,
            self.getBestQuiz,
            self.getPublicChatThreads,
            self.getRecentBlogs,
            self.getOnlineUsers,
            self.getRecentWikiItems,
            self.getPrivateChats
        )

        tasks = []
        for curr_func in funcs_without_params:
            curr_task = asyncio.create_task(curr_func())
            tasks.append(curr_task)
            CURRENT_REQUEST_ITER += 1
        
        responses = await asyncio.gather(*tasks, return_exceptions=True) 

        leaderboard_stat_params = ('24', '7', 'rep', 'check', 'quiz')
        for curr_param in leaderboard_stat_params:
            responses.append(await self.getFromLeaderboard(curr_param))
            CURRENT_REQUEST_ITER += 1
        
        public_user_params = ('leaders', 'recent', 'curators')
        for curr_param in public_user_params:
            responses.append(await self.getAllUsers(curr_param))
            CURRENT_REQUEST_ITER += 1

        return responses


    async def getTrendingQuiz(self) -> af.objects.BlogList.BlogList:
        global CURRENT_REQUEST_ITER
        Log.print_info_msg('Get trending quiz')    
        try:
            result = await self.subClient.get_trending_quiz(size=TREND_QUIZ_LIST_SIZE)
            CURRENT_REQUEST_ITER += 1        
        except Exception as e:
            Log.print_error_msg(e)
            raise e

        return result


    async def getBestQuiz(self) -> af.objects.BlogList.BlogList:
        global CURRENT_REQUEST_ITER
        Log.print_info_msg('Collect best qiuz')
        try:
            result = await self.subClient.get_best_quiz(size=BEST_QUIZ_LIST_SIZE) 
            CURRENT_REQUEST_ITER += 1        
        except Exception as e:
            Log.print_error_msg(e)
            raise e

        return result


    async def getPublicChatThreads(self) -> af.objects.ThreadList.ThreadList:
        global CURRENT_REQUEST_ITER
        Log.print_info_msg('Collect public chats')
        try:
            result = await self.subClient.get_public_chat_threads(size=CHAT_LIST_SIZE)
            CURRENT_REQUEST_ITER += 1        
        except Exception as e:
            Log.print_error_msg(e)
            raise e

        return result


    async def getFromLeaderboard(self, type: str) -> af.objects.UserProfileList.UserProfileList:
        global CURRENT_REQUEST_ITER
        Log.print_info_msg(f'Collect leaders: {type}')
        try:
            result = await self.subClient.get_leaderboard_info(type, size=LEADERS_TYPE_LIST_SIZE)
            CURRENT_REQUEST_ITER += 1        
        except Exception as e:
            Log.print_error_msg(e)
            raise e

        return result


    async def getRecentBlogs(self) -> af.objects.RecentBlogs.RecentBlogs:
        global CURRENT_REQUEST_ITER
        Log.print_info_msg('Collecting recent blogs authors')
        try:
            result = await self.subClient.get_recent_blogs(size=RECENT_BLOGS_LIST_SIZE)
            CURRENT_REQUEST_ITER += 1        
        except Exception as e:
            Log.print_error_msg(e)
            raise e
    
        return result


    async def getOnlineUsers(self) -> af.objects.UserProfileCountList.UserProfileCountList:
        global CURRENT_REQUEST_ITER
        Log.print_info_msg('Collecting online users')
        try:
            result = await self.subClient.get_online_users(size=ONLINE_USERS_LIST_SIZE)
            CURRENT_REQUEST_ITER += 1        
        except Exception as e:
            Log.print_error_msg(e)
            raise e

        return result


    async def getRecentWikiItems(self) -> af.objects.WikiList.WikiList:
        global CURRENT_REQUEST_ITER
        Log.print_info_msg('Collecting recent wiki')
        try:
            result = await self.subClient.get_recent_wiki_items(size=RECENT_WIKI_ITEMS_LIST_SIZE)
            CURRENT_REQUEST_ITER += 1                
        except Exception as e:
            Log.print_error_msg(e)
            raise e

        return result


    async def getAllUsers(self, type: str) -> af.objects.UserProfileCountList.UserProfileCountList:
        global CURRENT_REQUEST_ITER
        Log.print_info_msg(f'Collecting users: {type}')
        try:
            result = await self.subClient.get_all_users(type, size=TYPED_ALL_USERS_LIST_SIZE)
            CURRENT_REQUEST_ITER += 1                
        except Exception as e:
            Log.print_info_msg(e)
            raise e

        return result


    async def getUserFollowers(self, id: str) -> af.objects.UserProfileList.UserProfileList:
        global CURRENT_REQUEST_ITER
        Log.print_info_msg(f'Get followers from: {id} ')
        try:
            result = await self.subClient.get_user_followers(id, size=USER_FOLLOWERS_LIST_SIZE)
            CURRENT_REQUEST_ITER += 1                
        except Exception as e:
            Log.print_error_msg(e)
            raise e

        return result


    async def getUserFollowing(self, id: str) -> af.objects.UserProfileList.UserProfileList:
        global CURRENT_REQUEST_ITER
        Log.print_info_msg(f'Get followers from: {id} ')
        try:
            result = await self.subClient.get_user_following(id, size=USER_FOLLOWING_LIST_SIZE)
            CURRENT_REQUEST_ITER += 1                
        except Exception as e:
            Log.print_error_msg(e)
            raise e

        return result


    async def getPrivateChats(self) -> af.objects.ThreadList.ThreadList:
        global CURRENT_REQUEST_ITER
        Log.print_info_msg('Collecting from privates chat')
        try:
            result = await self.subClient.get_chat_threads(size=USER_FROM_CHAT)
            CURRENT_REQUEST_ITER += 1                
        except Exception as e:
            Log.print_error_msg(e)
            raise e

        return result


class Container:
    __slots__ = ('subClient', 'userNickIdx', 'userIdIdx', 'userLevelIdx', 'userBlogsCountIdx', 'userCommentsCountIdx',
                 'userFollowrsCountIdx', 'userFollowngCountIdx', 'userPostsCountIdx', 'userCreatedTimeIdx')
    
    def __init__(self, subClient: af.asyncfix.SubClient = None):
        self.subClient = subClient
        self.userNickIdx, self.userIdIdx = 0, 1 
        self.userLevelIdx, self.userBlogsCountIdx = 2, 3
        self.userCommentsCountIdx, self.userFollowrsCountIdx = 4, 5
        self.userFollowngCountIdx, self.userPostsCountIdx = 6, 7
        self.userCreatedTimeIdx = 8

    
    def __addUserInList(self, current_user: tuple, users_list: list) -> list:
        users_list.append({
            'Id': current_user[self.userIdIdx],
            'Nick': current_user[self.userNickIdx],
            'Level': current_user[self.userLevelIdx],
            'Blogs count': current_user[self.userBlogsCountIdx],
            'Comments count': current_user[self.userCommentsCountIdx],
            'Followers count': current_user[self.userFollowrsCountIdx],
            'Following count': current_user[self.userFollowngCountIdx],
            'Posts count': current_user[self.userPostsCountIdx],
            'Created time': current_user[self.userCreatedTimeIdx]
        })
        return users_list


    async def collectFromUserProfileList(self, data: af.lib.util.objects.UserProfileList,
                                         dict_to_check_duplicates: dict = None) -> typing.Tuple[list, dict]:
        Log.print_info_msg('Extract users from UserProfileList')
        
        users_list = [] 

        for current_user in zip(data.nickname, data.userId, data.level, data.blogsCount,
                                data.commentsCount, data.followersCount, data.followingCount, 
                                data.postsCount, data.createdTime):
            if dict_to_check_duplicates and not (current_user[self.userIdIdx] in dict_to_check_duplicates):            
                dict_to_check_duplicates.update({current_user[self.userIdIdx]: current_user[self.userNickIdx]})
                users_list = self.__addUserInList(current_user, users_list)
            else:
                users_list = self.__addUserInList(current_user, users_list)

        return users_list, dict_to_check_duplicates


    async def collectFromUserProfileCountList(self, data: af.lib.util.objects.UserProfileCountList,
                                              dict_to_check_duplicates: dict = None) -> typing.Tuple[list, dict]:
        Log.print_info_msg('Extract users from UserProfileCountList')
        
        users_list = []

        for current_user in zip(data.profile.nickname, data.profile.userId, data.profile.level, data.profile.blogsCount,
                                data.profile.commentsCount, data.profile.followersCount, data.profile.followingCount,
                                data.profile.postsCount, data.profile.createdTime):
            if dict_to_check_duplicates and not (current_user[self.userIdIdx] in dict_to_check_duplicates):
                dict_to_check_duplicates.update({current_user[self.userIdIdx]: current_user[self.userNickIdx]})
                users_list = self.__addUserInList(current_user, users_list)
            else:
                users_list = self.__addUserInList(current_user, users_list)
    
        return users_list, dict_to_check_duplicates


    async def collectFromRecentBlogs(self, data: af.lib.util.objects.RecentBlogs,
                                     dict_to_check_duplicates: dict = None) -> typing.Tuple[list, dict]:
        Log.print_info_msg('Extract users from RecentBlogs')
        
        users_list = []

        for current_user in zip(data.author.nickname, data.author.userId, data.author.level, data.author.blogsCount,
                                data.author.commentsCount, data.author.followersCount, data.author.followingCount,
                                data.author.postsCount, data.author.createdTime):
            if dict_to_check_duplicates and not (current_user[self.userIdIdx] in dict_to_check_duplicates):            
                dict_to_check_duplicates.update({current_user[self.userIdIdx]: current_user[self.userNickIdx]})
                users_list = self.__addUserInList(current_user, users_list)
            else:
                users_list = self.__addUserInList(current_user, users_list)

        return users_list, dict_to_check_duplicates

    
    async def collectFromBlogList(self, data: af.lib.util.objects.BlogList,
                                  dict_to_check_duplicates: dict = None) -> typing.Tuple[list, dict]:
        Log.print_info_msg('Extract users from BlogList')
        
        users_list = []

        for current_user in zip(data.author.nickname, data.author.userId, data.author.level, data.author.blogsCount,
                                data.author.commentsCount, data.author.followersCount, data.author.followingCount,
                                data.author.postsCount, data.author.createdTime):
            if dict_to_check_duplicates and not (current_user[self.userIdIdx] in dict_to_check_duplicates):            
                dict_to_check_duplicates.update({current_user[self.userIdIdx]: current_user[self.userNickIdx]})
                users_list = self.__addUserInList(current_user, users_list)
            else:
                users_list = self.__addUserInList(current_user, users_list)

        return users_list, dict_to_check_duplicates


    async def collectFromWikiList(self, data: af.lib.util.objects.WikiList,
                                  dict_to_check_duplicates: dict = None) -> typing.Tuple[list, dict]:
        Log.print_info_msg('Extract users from WikiList')
        
        users_list = []

        for current_user in zip(data.author.nickname, data.author.userId, data.author.level, data.author.blogsCount,
                                data.author.commentsCount, data.author.followersCount, data.author.followingCount,
                                data.author.postsCount, data.author.createdTime):
            if dict_to_check_duplicates and not (current_user[self.userIdIdx] in dict_to_check_duplicates):            
                dict_to_check_duplicates.update({current_user[self.userIdIdx]: current_user[self.userNickIdx]})
                users_list = self.__addUserInList(current_user, users_list)
            else:
                users_list = self.__addUserInList(current_user, users_list)
        
        return users_list, dict_to_check_duplicates


    async def collectFromThreadList(self, data: af.lib.util.objects.ThreadList,
                                    dict_to_check_duplicates: dict = None) -> typing.Tuple[list, dict]:
        Log.print_info_msg('Extract users from ThreadList')
        
        global CURRENT_REQUEST_ITER
        responses, tasks = [], []

        for curr_chat_id in data.chatId:
            tasks.append(asyncio.create_task(self.subClient.get_chat_users(curr_chat_id, size=USER_FROM_CHAT)))
            CURRENT_REQUEST_ITER += 1
            
        responses = await asyncio.gather(*tasks, return_exceptions=True) 
        tasks.clear()

        users_list = []
        for curr_user_list in responses:
            for current_user in zip(curr_user_list.nickname, curr_user_list.userId, curr_user_list.level, 
                                    curr_user_list.blogsCount, curr_user_list.commentsCount, 
                                    curr_user_list.followersCount, curr_user_list.followingCount, 
                                    curr_user_list.postsCount, curr_user_list.createdTime):
                if dict_to_check_duplicates and not (current_user[self.userIdIdx] in dict_to_check_duplicates):            
                    dict_to_check_duplicates.update({current_user[self.userIdIdx]: current_user[self.userNickIdx]})
                    users_list = self.__addUserInList(current_user, users_list)
                else:
                    users_list = self.__addUserInList(current_user, users_list)

        return users_list, dict_to_check_duplicates


    async def collectFromResponses(self, responses, dict_to_check_duplicates: dict = None) -> typing.Tuple[list, dict]:
        doings = {
            af.lib.util.objects.UserProfileList: self.collectFromUserProfileList,
            af.lib.util.objects.UserProfileCountList: self.collectFromUserProfileCountList,
            af.lib.util.objects.RecentBlogs: self.collectFromRecentBlogs,
            af.lib.util.objects.BlogList: self.collectFromBlogList,
            af.lib.util.objects.ThreadList: self.collectFromThreadList,
            af.lib.util.objects.WikiList: self.collectFromWikiList,
        }

        users_data, users_check_for_duplicate = [], {}

        if dict_to_check_duplicates:
            users_check_for_duplicate = dict_to_check_duplicates

        for curr_list in responses:
            try:
                users, users_check_for_duplicate = await doings.get(type(curr_list))(curr_list, users_check_for_duplicate)
                users_data.extend(users)
            except KeyboardInterrupt:
                Log.print_warning_msg(f'Ctrl+C is detected. Stopped collecting. Current amount of users - {len(users)}')
                Log.print_countdown()
            except TypeError:
                pass

        return users_data, users_check_for_duplicate


    async def getFollowersAndFollowing(self, users: list,
                                       dict_to_check_duplicates: dict = None) -> typing.Tuple[list, dict]:
        Log.print_info_msg('Get followers & following')
        
        global CURRENT_REQUEST_ITER
        
        tasks, start_idx, curr_list_size = [], 0, len(users)

        while start_idx <= curr_list_size:
            for curr_user_idx in range(start_idx, curr_list_size):
                if CURRENT_REQUEST_ITER <= MAX_REQUEST_CHUNK:
                    tasks.append(asyncio.create_task(self.subClient.get_user_following(users[curr_user_idx].get('Id'), size=USER_FROM_CHAT)))
                    tasks.append(asyncio.create_task(self.subClient.get_user_followers(users[curr_user_idx].get('Id'), size=USER_FROM_CHAT)))
                    CURRENT_REQUEST_ITER += 2
                else:
                    CURRENT_REQUEST_ITER = 0
                    responses = await asyncio.gather(*tasks, return_exceptions=True)
                    newUsers, dict_to_check_duplicates = await self.collectFromResponses(responses, dict_to_check_duplicates)
                    users.extend(newUsers)  
                    tasks.clear()
                
                    Log.print_warning_msg(f'In order to prevent 403 response. Sleep for 5 mins...\nCurrent users amount: {len(users)}')
                    time.sleep(60 * 5)
                    Log.print_countdown()

                    tasks.append(asyncio.create_task(self.subClient.get_user_following(users[curr_user_idx].get('Id'), size=USER_FROM_CHAT)))
                    tasks.append(asyncio.create_task(self.subClient.get_user_followers(users[curr_user_idx].get('Id'), size=USER_FROM_CHAT)))
                    CURRENT_REQUEST_ITER += 2
            start_idx = curr_list_size
            curr_list_size = len(users)
            
        return users, dict_to_check_duplicates



