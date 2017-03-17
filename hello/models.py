from django.db import models
from hello.utils.clean import clean_tweet

# Create your models here.
# to remove
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)


class QuestionManager(models.Manager):
    def clean_all(self):
        questions = Question.objects.all()
        for q in questions:
            q.txt_clean, q.is_clean = clean_tweet(q.txt, remove_hashtags=True)
            q.save()
        return True
    pass



class Question(models.Model):
    objects = QuestionManager()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    txt = models.TextField(null=False, blank=False)
    txt_clean = models.TextField(null=True, blank=True)
    created_by_name = models.CharField(max_length=30, null=True, blank=True)
    created_by_email = models.EmailField(null=True, blank=True)
    src = models.CharField(max_length=30, null=True, blank=True) #doctoctoc or website or twiiter_scrap
    tweet_infos = models.TextField(null=True, blank=True)
    is_clean = models.BooleanField(default=False)

    def __str__(self):
        return self.txt

class AnswerManager(models.Manager):
    def clean_all(self):
        answers = Answer.objects.all()
        for a in answers:
            a.txt_clean, a.is_clean = clean_tweet(a.txt, remove_hashtags=True)
            a.save()
        return True
    pass


class Answer(models.Model):
    objects = AnswerManager()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    txt = models.TextField(null=False, blank=False)
    txt_clean = models.TextField(null=True, blank=True)
    created_by_name = models.CharField(max_length=30, null=True, blank=True)
    created_by_email = models.EmailField(null=True, blank=True)
    src = models.TextField(null=False, blank=True)  # doctoctoc or website
    question_id = models.IntegerField(null=False)
    tweet_infos = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.txt