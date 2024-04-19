from django.contrib.auth.models import User
from django.db.models import Sum, Case, When, Count
from django.db import models


class QuestionManager(models.Manager):
    pass


class AnswerManager(models.Manager):
    pass


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True)
    displayed_name = models.CharField(max_length=100, unique=True)


class Tag(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    tags = models.ManyToManyField(Tag)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=1000)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuestionManager()

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    is_correct = models.BooleanField()
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AnswerManager()


class RateEntity(models.IntegerChoices):
    NOT_HELPFUL = -1, 'Not Helpful'
    NEUTRAL = 0, 'Neutral'
    HELPFUL = 1, 'Helpful'


class QuestionRating(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    value = models.IntegerField(choices=RateEntity.choices)

    class Meta:
        unique_together = ('user', 'question')


class AnswerRating(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    value = models.IntegerField(choices=RateEntity.choices)

    class Meta:
        unique_together = ('user', 'answer')
