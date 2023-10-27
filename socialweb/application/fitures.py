from application.models import *
from django.shortcuts import HttpResponse, redirect, render


class InterractiveActions:
    def check_value(self, post_id, user_id, category):
        post = BlogModel.objects.get(pk=post_id)
        value = BlogInteractiveModel.objects.filter(post=post).filter(who_likes=user_id)
        if value.exists():
            if value[0].likes == 1:
                value[0].delete()
            else:
                value[0].likes = 1
        else:
            BlogInteractiveModel.objects.create(post=post,
                                                who_likes=user_id,
                                                content_category=category,
                                                likes=1)

    def likes_counter(self, posts):
        try:
            counter = {}
            for post in posts:
                single_post = BlogInteractiveModel.objects.filter(post=post.id).filter(likes=1)
                result = len(single_post)
                counter.update({post.id: result})

            return counter
        except BlogInteractiveModel.DoesNotExist:
            pass


class Search:
    def find_user(self, query):
        name = CustomUser.objects.filter(name=query)
        surname = CustomUser.objects.filter(surname=query)
        if name.exists():
            return name
        elif surname.exists():
            return surname
        else:
            return None

    def video_search(self, query):
        title = Videos.objects.filter(title=query)
        if title.exists():
            return title
        else:
            return None

    def find_friends(self, request, query):
        name = CustomUser.objects.filter(name=query)
        surname = CustomUser.objects.filter(surname=query)
        if name.exists():
            for user in name:
                query_set = FriendsList.objects.filter(friends_list__in=[user.id, request.user.id]).filter(acception='A')
                if query_set.exists():
                    return user.name
                else:
                    return None
        elif surname.exists():
            for user in surname:
                query_set = FriendsList.objects.filter(friends_list__in=[user.id, request.user.id]).filter(acception='A')
                if query_set.exists():
                    return user.surname
                else:
                    return None
        else:
            return None


class FriendList:
    @classmethod
    def friend_invite(self, request, page_id):

        if 'add-friend' in request.GET:
            friend_list_status = FriendsList.objects.filter(friends_list__in=[request.user.id, page_id])

            if friend_list_status.exists():
                if friend_list_status[0].acception != 'A' or friend_list_status.acception != 'S':
                        friend_list_status[0].acception = 'S'
                else:
                    pass
            else:
                create_record = FriendsList.objects.create(acception='S', sender=request.user.id)
                create_record.friends_list.set([request.user.id, page_id])

    @classmethod
    def check_invites(self, request):
        user = CustomUser.objects.get(pk=request.user.id)
        new_friends = FriendsList.objects.filter(friends_list__in=[user.id])
        acceptions = {}
        for new in new_friends:
            if new.acception == 'S' and new.sender != request.user.id:
                acceptions.update({'friend': new})
                return acceptions
            else:
                return None


