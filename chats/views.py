import os
from main.models import UserProfile
from django.contrib.auth.decorators import permission_required, login_required
from django.db.models import Q, F
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone

from website import settings
from .models import Message, Group, GroupMembers, GroupMessages, Chat, ChatParticipant
from django.contrib.auth.models import User
import pytz


@login_required(login_url="/login")
@permission_required("chats.add_message", raise_exception=True)
def chats(request):
    if request.method == 'POST':
        groupName = request.POST.get('group-name')

        Group.objects.create(group_name=groupName, created_by=request.user)
        groups = Group.objects.all().filter(group_name=groupName)[0]
        GroupMembers.objects.create(group=groups, members=request.user, is_admin=True, added_by=request.user.id)


    return render(request, 'chats.html')



def calls(request):
    if request.method == 'POST':
        reci = request.POST.get('seen')
        Message.objects.filter(Q(sender=reci)&Q(recipient_id=request.user.id)).update(status="seen")




    users = User.objects.all().values(
        p_pu = F("userprofile__profile_picture"),
        user_name = F("username"),
        user_id = F("id"),
        users = F("userprofile__is_user")
    ).union(
        Group.objects.filter(groupmembers__members=request.user).values(
            p_pu = F("groupprofile__group_picture"),
            groupname = F("group_name"),
            group_id = F("id"),
            users = F("groupprofile__is_user")
        ))

    return render(request, 'calls.html', {"users": users})

def chat(request, reciid, userid, name, is_user):
    recipient = User.objects.get(id=reciid)
    get = Message.objects.filter(id=name)
    chat = Chat.objects.filter(participants=recipient).filter(participants=request.user)
    #chat_get = Chat.objects.get(participants=recipient).get(participants=request.user)
    present = GroupMessages.objects.filter(group_id=reciid)


    if not chat.exists():
        nc = Chat.objects.create()
        ChatParticipant.objects.create(user=request.user, chat=nc)
        ChatParticipant.objects.create(user=recipient, chat=nc)

    selected = Message.objects.filter(chat=chat[0]).order_by('sent_at')
    if reciid and userid:
        Message.objects.filter(Q(sender=recipient) & Q(chat=chat[0])).update(status="seen")

    else:
        pass

    user_timezone = pytz.timezone('CET')
    if is_user == 1:
        reci = User.objects.all().filter(id=reciid)[0]
    else:
        reci = Group.objects.all().filter(id=reciid)[0]

    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        group_id = request.POST.get("del-b")
        cr = ChatParticipant.objects.filter(Q(chat=chat[0]) & Q(user=recipient))
        if form_type == 'form4':
            reply = request.POST.get("reply")
            copy = request.POST.get("copy")
            delete = request.POST.get("delete")

            if reply:
                get = Message.objects.filter(id=reply)
            elif copy:
                get = Message.objects.filter(id=copy)
                pass
            elif delete:
                Message.objects.filter(id=delete).delete()
        elif form_type == 'form2':
            msg = request.POST.get('r-message')
            img = request.FILES.get('imgs')
            message = Message()
            if is_user == 1:

                if cr[0].is_blocked == False:
                    message.message = msg
                    message.chat = chat[0]
                    message.sender = request.user
                    message.status = "Delivered"
                    message.sent_at = timezone.now().astimezone(pytz.timezone('CET'))
                    message.image = img
                    trying = str(message.image)
                    if trying[-3:] in ['mp4', 'webm', 'avi', 'mov', 'mkv'] or trying[-4:] in ['mp4', 'webm', 'avi', 'mov', 'mkv']:
                        message.is_video = True
                    message.image_url = f"{message.image.name}"
                    if get:
                        message.reply = get[0]

                    message.save()
                    return redirect(f'/chat/{reciid}/{userid}/0/{is_user}')

            else:
                gms = GroupMessages()
                groups = Group.objects.get(id=reciid)
                gms.group = groups
                gms.message = msg
                gms.sent_by = request.user
                gms.status = "Delivered"
                gms.sent_at = timezone.now().astimezone(user_timezone)
                gms.image = img
                g_trying = str(gms.image)
                if g_trying[-3:] in ['mp4', 'webm', 'avi', 'mov', 'mkv'] or g_trying[-4:] in ['mp4', 'webm', 'avi', 'mov', 'mkv']:
                    gms.is_video = True

                gms.save()
                return redirect(f'/chat/{reciid}/{userid}/0/{is_user}')
        elif form_type == 'form1':
            group = Group.objects.get(id=group_id)
            if group:
                try:
                    group_member = GroupMembers.objects.get(group=group, members=request.user)

                    if group_member.is_admin:
                        group.delete()
                except GroupMembers.DoesNotExist:
                    pass
            else:
                pass
        elif form_type == 'form3':
            cr.update(is_blocked=True)


    if is_user == 0:
        gm = GroupMembers.objects.filter(group=reci)
    else:
        gm = []
    return render(request, 'chat.html', {'message': selected, 'groupmessages': present,'reci': reci, 'reply': get , 'r': reciid,'i_u': is_user,'gm': gm})

def default(request):
    return render(request, "def.html")

def member(request,groupId):
    users = User.objects.all()

    if request.method == "POST":
        user = request.POST.getlist("member-id")
        group = Group.objects.all().filter(id=groupId)[0]
        cu = GroupMembers.objects.all().filter(Q(members=request.user)&Q(group_id=groupId))[0]
        if cu.is_admin:
            for sUser in user:

                gm = GroupMembers.objects.all().filter(Q(members_id=sUser)&Q(group_id=groupId))
                if not gm:
                    userId = User.objects.all().filter(id=sUser)[0]
                    GroupMembers.objects.create(group=group,members=userId,is_admin=False,added_by=request.user.id)
                else:
                    pass
        else:
            pass

    return render(request, "group-admins.html", {"users": users,"id": groupId})
def r_member(request,groupId):

    gm = GroupMembers.objects.filter(group_id=groupId)
    if request.method == 'POST':
        ft = request.POST.get("form_type")
        if ft == "form1":
            n = request.POST.get("rm")
            u = GroupMembers.objects.get(Q(members_id=n)&Q(group_id=groupId))
            u.delete()
        elif ft == "form2":
            n = request.POST.get("rm")

            GroupMembers.objects.filter(Q(members_id=n) & Q(group_id=groupId)).update(is_admin=True)

    return render(request, 'group-members.html', {"gm":gm, "id": groupId})
def serve_media(request, path):
    media_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(media_path):
        with open(media_path, 'rb') as f:
            return HttpResponse(f.read(), content_type='image/jpeg')
    return HttpResponse('Image not found',status=404)

def media(request,mediaId):
    mFactor = Message.objects.filter(id=mediaId)
    if mFactor:
        m = Message.objects.get(id=mediaId)
    else:
        m = GroupMessages.objects.get(id=mediaId)
    return render(request, 'media.html',{'mFactor': m})

def entertainment(request):
    
    return render(request, "emoji.html")
    # Create your views here.
