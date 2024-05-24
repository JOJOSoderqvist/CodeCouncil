from django.contrib.auth.models import User
from django.db.models import Sum, Case, When, Count
from django.db import models


class QuestionManager(models.Manager):

    def get_all(self):
        return self.all()

    def get_latest(self):
        return self.get_all().order_by('-created_at')

    def get_hot(self):
        return self.get_all().order_by('-rating')

    def get_by_id(self, question_id):
        return self.get_all().get(id=question_id)

    def get_by_tag(self, tag_name):
        return self.get_all().filter(tags__name=tag_name)


class AnswerManager(models.Manager):
    def get_answers_for_question(self, q_id):
        return self.all().filter(question_id=q_id).order_by('created_at')


class TagManager(models.Manager):
    @staticmethod
    def get_popular_tags():
        popular_tags = Tag.objects.all().annotate(Count('question')).values('question__count').order_by(
            '-question__count')[:7].values('name')

        return popular_tags

    @staticmethod
    def get_ot_create_tags(tags):
        tag_objects = []
        for tag in tags:
            tag_object, _ = Tag.objects.get_or_create(name=tag)
            tag_objects.append((tag_object.name, tag_object.id))
        print(tag_objects)
        return tag_objects


class ProfileManager(models.Manager):
    @staticmethod
    def create_profile(user, displayed_name):
        user_profile = Profile.objects.create(user=user, displayed_name=displayed_name)
        user_profile.save()

    def get_current_user_profile(self, user):
        return self.get(user=user), User.objects.get(id=user.id)

    @staticmethod
    def get_popular_profiles():
        popular_profiles = Profile.objects.all().annotate(Count('question')).values('question__count').order_by(
            '-question__count')[:7].values('displayed_name')
        return popular_profiles


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True)
    displayed_name = models.CharField(max_length=100, unique=True)
    objects = ProfileManager()


class Tag(models.Model):
    name = models.CharField(max_length=10, unique=True)
    objects = TagManager()

    def __str__(self):
        return self.name


class Question(models.Model):
    tags = models.ManyToManyField(Tag)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    text = models.CharField(max_length=1000)
    rating = models.IntegerField(default=0)
    answers_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuestionManager()

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    is_correct = models.BooleanField(default=False)
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
