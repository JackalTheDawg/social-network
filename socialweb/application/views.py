from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from application.auth import auth
from application.fitures import *
from django.contrib.auth.decorators import login_required
from application.chat.chat import *


# Create your views here.
def page(request):
    """index page with authorization and registration
    if session is not None, function will redirect user on his page
    """
    profile = auth.AuthenticateUser()

    user_id = profile.check_session(request)

    if user_id is not None:
        return redirect(f'/id={user_id}')
    else:
        pass

    form = Sign_in_form(request.POST or None)
    registration_form = Registration_form(request.POST or None)
    message = None

    if request.method == "POST":
        if 'sign-in-btn' in request.POST:
            if form.is_valid():
                user_id = profile.sign_in(request, form.cleaned_data)
                if user_id is not None:
                    return redirect(f'/id={user_id}')
                else:
                    print('Wrong login or password, please try again')

        if 'registration-btn' in request.POST:
            if registration_form.is_valid():
                user_id = profile.sign_up(request, registration_form)
                if user_id is not None:
                    return redirect(f'/id={user_id}')
                else:
                    print('This email or number already used! Forgot password?')


    context = {'sign_in': form, 'registration': registration_form, 'message': message}
    return render(request,'index.html', context)


@login_required
def profile_page(request, page_id):
    """function of rendering page with blog, likes,video, comments and photos"""

    users_page = CustomUser.objects.get(pk=page_id)
    visitor = CustomUser.objects.get(pk=request.user.id)
    posts = BlogModel.objects.filter(post_location_id=page_id)
    photos_from_gallery = PhotoGallery.objects.filter(page=page_id).order_by('-id')[:5]
    videos_form_gallery = Videos.objects.filter(page=page_id).order_by('-id')[:3]


    comments = BlogCommentsModel.objects.filter(location_id=page_id)

    category = 'post'

    act = InterractiveActions()
    likes = act.likes_counter(posts)

    form = PageBlogForm(request.POST, request.FILES)
    comment_form = CommentsForm(request.POST, request.FILES)
    add_photo_form = AddPhoto(request.POST, request.FILES)
    profile_picture = Change_picture(request.POST, request.FILES)

    invites = FriendList.check_invites(request)

    if request.method == "POST":
        if 'blog' in request.POST:
            if form.is_valid():
                form.instance.post_author = visitor
                form.instance.post_location_id = page_id
                form.save()

        if 'like' in request.POST:
            act.check_value(post_id=request.POST['like'], user_id=visitor, category=category)

        if 'comment' in request.POST:
            if comment_form.is_valid():
                comment_form.instance.author = visitor
                comment_form.instance.location_id = page_id
                comment_form.instance.post = BlogModel.objects.get(pk=request.POST['comment'])
                comment_form.save()

        if 'add-photo' in request.POST:
            if add_photo_form.is_valid():
                add_photo_form.instance.page = users_page
                add_photo_form.save()

        if 'send-message' in request.POST:
            chat = Chat.start_chat(request.user.id, page_id)
            return redirect(f'/chat={chat}')

        if 'change-picture' in request.POST:
            if profile_picture.is_valid():
                users_page.profile_picture = profile_picture.instance.profile_picture
                users_page.save()

    context = {'blog_form': form,
               'comment_form': comment_form,
               'page': users_page,
               'posts': posts,
               'comments': comments,
               'photos': photos_from_gallery,
               'add_photo': add_photo_form,
               'videos': videos_form_gallery,
               'likes': likes,
               'change_pic': profile_picture
               }

    if 'q' in request.GET:
        query = request.GET.get('q', None)
        splited_query = query.split('=')[1]
        photo = PhotoGallery.objects.get(pk=splited_query)
        context.update({'picture': photo})

    if 'v' in request.GET:
        query = request.GET.get('v', None)
        splited_query = query.split('=')[1]
        video = Videos.objects.get(pk=splited_query)
        context.update({'video_render': video})

    if 'pic' in request.GET:
        query = request.GET.get('pic', None)
        print(f'query: {query}')
        splited_query = query.split('=')[-1]
        print(splited_query)
        prof_pic = CustomUser.objects.get(email=splited_query)
        context.update({'picture': prof_pic})

    if 'add-friend' in request.GET:
        FriendList.friend_invite(request, page_id)


    if invites is not None:
        context.update({'invites': invites})

    return render(request, 'profile_page.html', context)

@login_required
def photo_gallery(request, page_id):
    """Function of renderign photo-gallery of profile"""
    photos = PhotoGallery.objects.filter(page=page_id).order_by('-id')
    context = {'photos': photos}
    """Secondary use
    That`s should be a function"""
    if 'q' in request.GET:
        query = request.GET.get('q', None)
        splited_query = query.split('=')[1]
        photo = PhotoGallery.objects.get(pk=splited_query)
        context.update({'picture': photo})
    return render(request, 'photo-gallery.html', context)

@login_required
def video_gallery(request, page_id):
    """Function of renderign video-gallery of profile"""
    search = Search()
    form = AddVideo(request.POST, request.FILES)
    author = CustomUser.objects.get(pk=page_id)
    videos = Videos.objects.filter(page=page_id).order_by('-id')
    if request.method == "POST":
        if form.is_valid():
            form.instance.page = author
            form.save()
        else:
            print(form.errors.as_data())

    """????"""
    search_query = request.GET.get('q', None)
    if search_query is not None:
        results = search.video_search(search_query)
        return render(request, 'video-gallery.html', {'results': results})


    context = {'form': form, 'videos':videos}



    """Secondary use"""
    if 'v' in request.GET:
        query = request.GET.get('v', None)
        splited_query = query.split('=')[1]
        video = Videos.objects.get(pk=splited_query)
        context.update({'video_render': video})

    return render(request, 'video-gallery.html', context)

@login_required
def friends_list(request):
    """Functrion that`s rendering friends list with search in it and friends invites"""

    search = Search()

    users = CustomUser.objects.all()
    friends = FriendsList.objects.filter(friends_list__in=[request.user.id]).filter(acception='A')
    invites = FriendsList.objects.filter(friends_list__in=[request.user.id]).filter(acception='S')

    friends_data = []
    invites_data = []

    for friend in friends:
        friend_obj = friend.friends_list.all().exclude(pk=request.user.id)[0]
        friend_info = CustomUser.objects.get(pk=friend_obj.id)
        friends_data.append(friend_info)

    """Secondary use"""
    for invite in invites:
        invite_obj = invite.friends_list.all().exclude(pk=request.user.id)[0]
        invite_info = CustomUser.objects.get(pk=invite_obj.id)
        invites_data.append(invite_info)


    search_query = request.GET.get('q', None)
    if search_query is not None:
        results = search.find_friends(request, search_query)
        return render(request, 'friends_list.html', {'results': results})

    context = {'users': users, 'friends': friends_data, 'invites': invites_data}


    if 'accept' in request.GET:
        user = request.GET.get('accept', None)
        user_id = CustomUser.objects.get(pk=user)
        change_status = FriendsList.objects.filter(friends_list__in=[request.user.id, user_id])[0].id
        FriendsList.objects.filter(pk=change_status).update(acception='A')

    if 'refuse' in request.GET:
        user = request.GET.get('refuse', None)
        user_id = CustomUser.objects.get(email=user).pk
        FriendsList.objects.get(friends_list__in=[request.user.id, user_id]).delete()

    return render(request, 'friends_list.html', context)

@login_required
def search_page(request):
    """rendering page with searching in all users"""

    search = Search()
    users = CustomUser.objects.all().exclude(pk=request.user.id)
    search_query = request.GET.get('q', None)
    if search_query is not None:
        results = search.find_user(search_query)
        return render(request, 'search.html', {'results': results})

    return render(request, 'search.html', {'users': users})


@login_required
def chat_list(request, page_id):
    chats = ChatModel.objects.filter(members__in=[request.user.id])
    members = []
    for chat in chats:
        member = chat.members.all().exclude(pk=request.user.id)[0]
        members.append(member)
    return render(request, 'chat_list.html', {'chats': chats, 'members': members})

@login_required
def chat_page(request, chat_id):
    chat = Chat()
    messages = chat.get_messages(chat_id)
    form = MessageForm(request.POST)

    return render(request, 'chat.html', {'form': form, 'messages': messages, 'chat': chat_id})

@login_required
def favorites(request):

    users_likes = BlogInteractiveModel.objects.filter(who_likes=request.user.id)

    return render(request, 'favorites.html', {'likes': users_likes})

@login_required
def page_settings(request):
    users_data = CustomUser.objects.get(pk=request.user.id)
    form = Change_profiles_info(request.POST or None, instance=users_data)
    if request.method == "POST":
        if form.is_valid():
            data = form.cleaned_data
            for key in data:
                if data[key] != '':
                    setattr(users_data, key, data[key])
                    users_data.save()


    return render(request, 'page_settings.html', {'form': form})


@login_required
def news(request):

    return render(request, 'news.html')