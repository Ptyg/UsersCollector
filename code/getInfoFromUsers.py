import aminofix as af
import datetime

async def get_info_from_users_after_public_gather(subClient, list_of_users: list):
    users_id_and_nick_to_check_for_duplicate = {}
    users_for_csv = []

    for i in list_of_users:
        if type(i) == af.objects.UserProfileList:
            for nick, user_id, level, blogs_count, comm_count, followers_count, following_count, post_count, created_time \
                    in zip(i.nickname, i.userId, i.level, i.blogsCount, i.commentsCount, i.followersCount, i.followingCount,
                            i.postsCount, i.createdTime):
                if not (user_id in users_id_and_nick_to_check_for_duplicate):
                    users_id_and_nick_to_check_for_duplicate.update({user_id: nick})
                    users_for_csv.append({
                        'Nick': nick,
                        'Id': user_id,
                        'Level': level,
                        'Blogs count': blogs_count,
                        'Comments count': comm_count,
                        'Followers count': followers_count,
                        'Following count': following_count,
                        'Posts count': post_count,
                        'Created time': created_time
                    })
                    print(f'{datetime.datetime.now()} [INFO] {nick} is added')


        elif type(i) == af.objects.UserProfileCountList:
            for nick, user_id, level, blogs_count, comm_count, followers_count, following_count, post_count, created_time \
                    in zip(i.profile.nickname, i.profile.userId, i.profile.level, i.profile.blogsCount, i.profile.commentsCount, 
                            i.profile.followersCount, i.profile.followingCount, i.profile.postsCount, i.profile.createdTime):
                if not (user_id in users_id_and_nick_to_check_for_duplicate):
                    users_id_and_nick_to_check_for_duplicate.update({user_id: nick})
                    users_for_csv.append({
                        'Nick': nick,
                        'Id': user_id,
                        'Level': level,
                        'Blogs count': blogs_count,
                        'Comments count': comm_count,
                        'Followers count': followers_count,
                        'Following count': following_count,
                        'Posts count': post_count,
                        'Created time': created_time
                    })
                    print(f'{datetime.datetime.now()} [INFO] {nick} is added')


        elif type(i) == af.objects.BlogList:
            for nick, user_id, level, blogs_count, comm_count, followers_count, following_count, post_count, created_time \
                    in zip(i.author.nickname, i.author.userId, i.author.level, i.author.blogsCount, i.author.commentsCount, 
                            i.author.followersCount, i.author.followingCount, i.author.postsCount, i.author.createdTime):
                if not (user_id in users_id_and_nick_to_check_for_duplicate):
                    users_id_and_nick_to_check_for_duplicate.update({user_id: nick})
                    users_for_csv.append({
                        'Nick': nick,
                        'Id': user_id,
                        'Level': level,
                        'Blogs count': blogs_count,
                        'Comments count': comm_count,
                        'Followers count': followers_count,
                        'Following count': following_count,
                        'Posts count': post_count,
                        'Created time': created_time
                    })
                    print(f'{datetime.datetime.now()} [INFO] {nick} is added')


        elif type(i) == af.objects.WikiList:
            for nick, user_id, level, blogs_count, comm_count, followers_count, following_count, post_count, created_time \
                    in zip(i.author.nickname, i.author.userId, i.author.level, i.author.blogsCount,
                            i.author.commentsCount, i.author.followersCount, i.author.followingCount,
                            i.author.postsCount, i.author.createdTime):
                if not (user_id in users_id_and_nick_to_check_for_duplicate):
                    users_id_and_nick_to_check_for_duplicate.update({user_id: nick})
                    users_for_csv.append({
                        'Nick': nick,
                        'Id': user_id,
                        'Level': level,
                        'Blogs count': blogs_count,
                        'Comments count': comm_count,
                        'Followers count': followers_count,
                        'Following count': following_count,
                        'Posts count': post_count,
                        'Created time': created_time
                    })
                    print(f'{datetime.datetime.now()} [INFO] {nick} added')
                

        elif type(i) == af.objects.RecentBlogs:
            for nick, user_id, level, blogs_count, comm_count, followers_count, following_count, post_count, created_time \
                    in zip(i.author.nickname, i.author.userId, i.author.level, i.author.blogsCount, i.author.commentsCount, 
                            i.author.followersCount, i.author.followingCount, i.author.postsCount, i.author.createdTime):
                if not (user_id in users_id_and_nick_to_check_for_duplicate):
                    users_id_and_nick_to_check_for_duplicate.update({user_id: nick})
                    users_for_csv.append({
                        'Nick': nick,
                        'Id': user_id,
                        'Level': level,
                        'Blogs count': blogs_count,
                        'Comments count': comm_count,
                        'Followers count': followers_count,
                        'Following count': following_count,
                        'Posts count': post_count,
                        'Created time': created_time
                    })
                    print(f'{datetime.datetime.now()} [INFO] {nick} added')
                

        elif type(i) == af.objects.ThreadList:
            for chatid in i.chatId:
                cur_users = await subClient.get_chat_users(chatid, size=999)
                for nick, user_id, level, blogs_count, comm_count, followers_count, following_count, post_count, created_time \
                        in zip(cur_users.nickname, cur_users.userId, cur_users.level, cur_users.blogsCount,
                                cur_users.commentsCount, cur_users.followersCount, cur_users.followingCount,
                                cur_users.postsCount, cur_users.createdTime):
                    if not (user_id in users_id_and_nick_to_check_for_duplicate):
                        users_id_and_nick_to_check_for_duplicate.update({user_id: nick})
                        users_for_csv.append({
                            'Nick': nick,
                            'Id': user_id,
                            'Level': level,
                            'Blogs count': blogs_count,
                            'Comments count': comm_count,
                            'Followers count': followers_count,
                            'Following count': following_count,
                            'Posts count': post_count,
                            'Created time': created_time
                        })
                        print(f'{datetime.datetime.now()} [INFO] {nick} added')
    
    return users_id_and_nick_to_check_for_duplicate, users_for_csv