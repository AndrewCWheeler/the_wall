from django.shortcuts import render, redirect
from register_login_app.models import User
from messages_app.models import Messages
from messages_app.models import Comments
from datetime import datetime
from datetime import timedelta

def wall(request):
    session_user = User.objects.get(id=request.session['userid'])
    all_users = User.objects.all()
    # all_messages = Messages.objects.all()
    all_messages = Messages.objects.all().order_by('-created_at')
    all_comments = Comments.objects.all().order_by('-created_at')
    context = {
        'session_user' : session_user,
        'all_messages' : all_messages,
        'all_users' : all_users,
        'all_comments' : all_comments
    }
    return render(request, 'wall.html', context)

def process_message(request):
    Messages.objects.create(
        message = request.POST['message'],
        user = User.objects.get(id=request.session['userid'])
    )
    return redirect('/messages/wall')

def logout(request):
    del request.session['userid']
    return redirect('/home/login')

def process_comment(request):
    Comments.objects.create(
        comment = request.POST['comment'],
        user = User.objects.get(id=request.session['userid']),
        message = Messages.objects.get(id=request.POST['message_id'])
    )
    return redirect('/messages/wall')

def destroy(request, message_id):
    user = User.objects.get(id=request.session['userid'])
    message = Messages.objects.get(id=message_id)
    tz_info = message.created_at.tzinfo
    print(tz_info)
    print(message.created_at)
    print(datetime.now(tz_info))
    if user.id == message.user.id:
        difference = datetime.now(tz_info) - message.created_at
        if difference < timedelta(minutes=30):
            print(difference)
            print(type(difference))
            message.delete()
            return redirect('/messages/wall')
    return redirect('/messages/wall')