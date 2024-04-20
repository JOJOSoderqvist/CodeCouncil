import os.path

from askme_karpikhin.settings import STATIC_URL
from django.core.management.base import BaseCommand
from django.core.files import File
from django.contrib.auth.models import User
from app.models import *
from faker import Faker
import random


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('ratio', nargs='?', type=int, default=10000)

    def handle(self, *args, **options):
        fake = Faker()
        Faker.seed(0)

        ratio = options['ratio']
        # tags
        # unique_tag_names = set()
        # while len(unique_tag_names) < ratio:
        #     unique_tag_names.add(fake.text()[:random.randint(3, 6)])
        #
        # tags = [Tag(name=name) for name in unique_tag_names]
        # Tag.objects.bulk_create(tags)
        tag_objects = Tag.objects.all()

        # # profile and users
        # unique_usernames = set()
        # unique_emails = set()
        # while len(unique_usernames) < ratio and len(unique_emails) < ratio:
        #     unique_usernames.add(fake.unique.user_name())
        #     unique_emails.add(fake.unique.email())
        #
        # users = [
        #     User.objects.create_user(
        #         username=username,
        #         email=email,
        #         password=fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)
        #     ) for username, email in zip(unique_usernames, unique_emails)
        # ]
        #
        # User.objects.bulk_create(users)

        user_objects = User.objects.all()
        # profiles = [Profile(user=user, displayed_name=user.username,
        #                     avatar=os.path.join(STATIC_URL, 'img/default_profilepic.jpg')) for user in
        #             user_objects]
        # Profile.objects.bulk_create(profiles)
        profile_objects = Profile.objects.all()

        # # questions and answers
        # questions_list = []
        # answers_list = []
        #
        # for _ in range(ratio * 10):
        #     question = Question(
        #         user=random.choice(profile_objects),
        #         title=f"{fake.sentence()[:random.randint(10, 20)]}?",
        #         text=fake.text()[:random.randint(30, 100)],
        #         created_at=fake.past_date(),
        #         updated_at=fake.date_time_this_year()
        #     )
        #     questions_list.append(question)
        #
        # Question.objects.bulk_create(questions_list)
        # question_objects = Question.objects.all()
        #
        # for question in question_objects:
        #     for _ in range(0, random.randint(1, 5)):
        #         question.tags.add(random.choice(tag_objects))
        #
        #     num_answers = random.randint(5, 20)
        #     question.answers_count = num_answers
        #     question.save()
        #     for _ in range(num_answers):
        #         answer = Answer(
        #             question=question,
        #             text=fake.text()[:random.randint(5, 100)],
        #             user=random.choice(profile_objects),
        #             is_correct=fake.boolean(),
        #             created_at=fake.past_date(),
        #             updated_at=fake.date_time_this_year()
        #         )
        #         answers_list.append(answer)
        #
        # Answer.objects.bulk_create(answers_list)

        answer_objects = Answer.objects.all()
        #
        # # Ratings
        # question_rating = []
        # answer_rating = []
        # for profile in profile_objects:
        #     rated_questions = random.sample(list(question_objects), k=random.randint(70, 140))
        #     for question in rated_questions:
        #         question_rating.append(QuestionRating(
        #             user=profile,
        #             question=question,
        #             value=random.choice([-1, 0, 1])
        #         ))
        #
        #     rated_answers = random.sample(list(answer_objects), k=random.randint(70, 140))
        #     for answer in rated_answers:
        #         answer_rating.append(AnswerRating(
        #             user=profile,
        #             answer=answer,
        #             value=random.choice([-1, 0, 1])
        #         ))
        # QuestionRating.objects.bulk_create(question_rating)
        # AnswerRating.objects.bulk_create(answer_rating)

        question_rating_objects = QuestionRating.objects.all()
        answer_rating_objects = AnswerRating.objects.all()
        # for question_object in question_objects:
        #     rating_sum = question_rating_objects.filter(question=question_object).aggregate(Sum('value'))
        #     if rating_sum['value__sum']:
        #         question_object.rating = rating_sum['value__sum']
        #         question_object.save()
        for answer_object in answer_objects:
            rating_sum = answer_rating_objects.filter(answer=answer_object).aggregate(Sum('value'))
            if rating_sum['value__sum']:
                answer_object.rating = rating_sum['value__sum']
                answer_object.save()
        self.stdout.write('Success')
