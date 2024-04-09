from django.contrib.auth.models import User
from django.db.models import Sum, Case, When, Count
from django.db import models


class QuestionManager(models.Manager):
    def get_all(self):
        return self.annotate(
            total_rating=Sum(Case(When(rating__question__isnull=False, then='rating__value')), default=0),
            answers_number=Count('answer'))

    def get_hot(self):
        return self.get_all().order_by('-total_rating')

    def get_latest(self):
        return self.get_all().order_by('-created_at')

    def get_by_id(self, question_id):
        return self.get_all().get(pk=question_id)

    def get_by_tag(self, tag_name):
        return self.get_all().filter(tags__name=tag_name)


class AnswerManager(models.Manager):
    def get_all(self):
        return self.annotate(
            total_rating=Sum(Case(When(rating__answer__isnull=False, then='rating__value')), default=0))

    def get_answers_for_question(self, question_id):
        return self.get_all().filter(question_id=question_id)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True)


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    tags = models.ManyToManyField(Tag)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=1000)
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AnswerManager()


class Rating(models.Model):
    class RateEntity(models.IntegerChoices):
        NOT_HELPFUL = -1, 'Not Helpful'
        NEUTRAL = 0, 'Neutral'
        HELPFUL = 1, 'Helpful'

    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
    value = models.IntegerField(choices=RateEntity.choices)

    class Meta:
        unique_together = ('user', 'question'), ('user', 'answer')
        constraints = [
            models.CheckConstraint(
                check=models.Q(question__isnull=False, answer__isnull=True) | models.Q(question__isnull=True,
                                                                                       answer__isnull=False),
                name='rating_for_either_question_or_answer'
            ),
        ]
