from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField
#import collections

class Expertise(models.Model):
    expertise = models.CharField(max_length=32, blank=True)
"""
    majority_types = (
        ('MATH', 'math'),
        ('COMPUTER_SCIENCE', 'computer_science'),
        ('ENGLISH', 'english')
    )
    majorities = (choices=majority_types)
"""




class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    expertises = models.ManyToManyField(Expertise)

    class Meta:
        verbose_name = 'User Profile'

    def __str__(self):
        return "{}".format(self.user.__str__())

class Hashtag(models.Model):
    hashtag = models.CharField(max_length=32)


class QuestionForm(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_form')

    title = models.CharField('Title', max_length=128)

    content = models.CharField('Content', max_length=10000, blank=True)

    create_date = models.DateTimeField('Create modified')
    
    mod_date = models.DateTimeField('Last modified', auto_now=True)

    reply_number = models.IntegerField('Reply Number', default=0)
    
    hashtags = models.ManyToManyField(Hashtag)

    class Meta:
        verbose_name = 'Question Form'

    def __str__(self):
        return "{}".format(self.__str__())

