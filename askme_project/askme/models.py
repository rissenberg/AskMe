from django.db import models
from django.contrib.auth.models import User

# Create your models here.
QUESTIONS = [
    {
        'id': i,
        'title': f'Question Title {i + 1}',
        'text': f'Text of question {i + 1}',
    } for i in range(12)
]


ANSWERS = [
    {
        'id': i,
        'title': f'Answer Title {i + 1}',
        'text': f'Text of answer {i + 1}, a bit longer',
    } for i in range(4)
]


class PostManager(models.Manager):
    def get_newest(self):
        return self.order_by('last_update')

    def get_tag(self, name):
        return self.filter('tag=name')

    def get_hot(self, name):
        return



class Post(models.Model):
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=2047)
    last_update = models.DateTimeField(auto_now=True)
    status_id = models.ForeignKey('Status', auto_created=True, on_delete=models.CASCADE)
    tags_id = models.ManyToManyField('Tag', blank=True)
    author = models.ForeignKey('User',  on_delete=models.CASCADE)

    object = PostManager()
    def __str__(self):
        return self.title


class AnswerManager(models.Manager):
    def get_newest(self):
        return self.order_by('last_update')

    def get_hot(self, name):
        return


class Answer(models.Model):
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=2047)
    last_update = models.DateTimeField(auto_now=True)
    correct = models.BooleanField(null=True)
    post_id = models.ForeignKey('Post', on_delete=models.CASCADE)
    status_id = models.ForeignKey('Status', auto_created=True, on_delete=models.CASCADE)
    author = models.ForeignKey('User',  on_delete=models.CASCADE)

    object = AnswerManager()
    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Status(models.Model):
    views = models.IntegerField(max_length=32)
    likes = models.IntegerField(max_length=32)


class User(models.Model):
    profile = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    avatar = models.ImageField(blank=True)
