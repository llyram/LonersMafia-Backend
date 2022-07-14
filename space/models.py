from django.db import models
from django.conf import settings
from django.utils import timezone
from utils.customfields import ContentTypeRestrictedFileField
# Create your models here.


class Space(models.Model):
    """
        Each user can create their own space and start a chat. Looner is a char space for looners
    """
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    name = models.CharField(max_length=30, null=False, unique=True)
    verbose_name = models.CharField(max_length=40, null=True) # this is a verbose name

    icon = ContentTypeRestrictedFileField(upload_to='space-icons/', content_types=['image/png', 'image/jpeg', 'image/gif'], 
                                            max_upload_size=5242880, null=True)
    about = models.CharField(max_length=350, null=True)
    tag_line = models.CharField(max_length=60, null=True)

    created_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:

        verbose_name = 'space'
        verbose_name_plural = 'spaces'

    def __str__(self) -> str:
        return self.name


class Rule(models.Model):

    """
        The user who create the space can enfoce certain rules
    """

    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    rule = models.CharField(max_length=250)

    class Meta:

        verbose_name = 'space rule'
        verbose_name_plural = 'space rules'

    def __str__(self) -> str:
        return self.rule


class Moderator(models.Model):

    """
        Moderators are previlaged users that can delete other's messages and ban users from a space
    """

    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.name} is a mod of {self.space.name}'


class Message(models.Model):

    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    message = models.TextField(max_length=2500, null=True)
    media = ContentTypeRestrictedFileField(upload_to='chat-media/', content_types=['image/png', 'image/jpeg', 'image/gif', 'image/svg'], 
                                            max_upload_size=10485760, null=True)  # 20 mb max
    
    datetime = models.DateTimeField(default=timezone.now) #auto_now_add=True

    class Meta:

        verbose_name = 'message'
        verbose_name_plural = 'messages'
    
    def __str__(self):
        return self.message[:50]


class Reaction(models.Model):

    """
        reaction to certain message
    """

    class ReactionTypes(models.IntegerChoices):

        HEART = 0, 'heart'
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)

    reaction = models.PositiveSmallIntegerField(choices=ReactionTypes.choices)  

    def __str__(self):
        return f'{self.user.name} reacted with {self.reaction}'


class BanUserFromSpace(models.Model):

    """
        This bans user from participating in a space
    """

    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)