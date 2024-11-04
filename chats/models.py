from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class Chat(models.Model):
    participants = models.ManyToManyField(User, through='ChatParticipant')




class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, default=0)
    message = models.TextField()
    sent_at = models.DateTimeField()
    status = models.CharField()
    image = models.ImageField(upload_to='dm_media/', blank=True, null=True)
    image_url = models.URLField(blank=True)
    is_video = models.BooleanField(default=False)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')



    """def save(self, *args, **kwargs):
        if self.image:
            file_extension = self.image.name.split('.')[-1].lower()
            if file_extension in ['mp4', 'webm', 'avi', 'mov', 'mkv']:
                self.is_video = True
                super().save(*args, **kwargs)"""


class ChatParticipant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    last_message = models.ForeignKey(Message, on_delete=models.SET_NULL, null=True, blank=True)
    is_blocked = models.BooleanField(default=False)



class Group(models.Model):

    group_name = models.CharField(max_length=30)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class groupprofile(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    group_picture = models.ImageField(upload_to="dm_media", null=True, blank=True)
    is_user = models.BooleanField(default=False)

class GroupMembers(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    members = models.ForeignKey(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(False)
    added_at = models.DateTimeField(auto_now_add=True)
    added_by = models.IntegerField()

    def __str__(self):
        return self.members

class GroupMessages(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    message = models.TextField(max_length=5000)
    sent_by = models.ForeignKey(User, on_delete=models.CASCADE)
    sent_at = models.DateTimeField()
    status = models.CharField()
    image = models.ImageField(upload_to='dm_media/', blank=True, null=True)
    image_url = models.URLField(blank=True)
    is_video = models.BooleanField(default=False)

    def __str__(self):
        return self.message

class Recent(models.Model):
    sender = models.IntegerField()
    recipient_id = models.IntegerField()
    user_id = models.IntegerField()
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
# Create your models here.
