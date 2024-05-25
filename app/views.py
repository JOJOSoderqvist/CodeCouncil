
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect

from app.forms import RegisterForm, LoginForm, UserEditForm, NewQuestionForm, NewAnswerForm
from app.models import Question, Answer, Tag, Profile


# Create your views here.


def paginator(object_list, request, elems_per_page=5):
    page_num = request.GET.get('page', 1)
    try:
        page_num = max(1, int(page_num))
    except ValueError:
        page_num = 1

    paginator_obj = Paginator(object_list, elems_per_page)
    pages = paginator_obj.get_page(page_num)
    return pages


def index(request):
    questions = Question.objects.get_latest()
    pages = paginator(questions, request)
    return render(request, 'index.html', {'questions': pages})


def hot(request):
    hot_questions = Question.objects.get_hot()
    pages = paginator(hot_questions, request)
    return render(request, 'hot.html', {'questions': pages})


@csrf_protect
def add_answer(request, single_question):
    answer_form = NewAnswerForm(request.POST)
    if answer_form.is_valid():
        answer = Answer.objects.create(question=single_question, text=answer_form.cleaned_data['answer_text'],
                                       user=Profile.objects.get(user=request.user))
        answer.save()

        single_question.answers_count += 1
        single_question.save()
        return True
    return False


def question(request, question_id):
    single_question = Question.objects.get_by_id(question_id)
    answers = Answer.objects.get_answers_for_question(question_id)
    pages = paginator(answers, request)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        if add_answer(request, single_question):
            return redirect('question', question_id=single_question.id)

    return render(request, 'question.html', {'question': single_question, 'answers': pages})


@csrf_protect
def login_view(request):
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            user = authenticate(request, username=login_form.cleaned_data['django_username'],
                                password=login_form.cleaned_data['password'])
            if user:
                login(request, user)
                if request.GET.get('next'):
                    return redirect(request.GET['next'])
                return redirect('index')
            else:
                print('failed to authenticate')
        else:
            print('form is not valid')
            for field in login_form:
                print("Field Error:", field.name, field.errors)

    return render(request, 'login.html')


@csrf_protect
def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(data=request.POST)
        for field in register_form:
            print("Field Error:", field.name, field.errors)
        if register_form.is_valid():
            try:
                new_user = User.objects.create_user(username=register_form.cleaned_data['django_username'],
                                                    email=register_form.cleaned_data['email'],
                                                    password=register_form.cleaned_data['password'])
                new_user.save()
                Profile.objects.create_profile(new_user, register_form.cleaned_data['username'])
                user = authenticate(request, username=register_form.cleaned_data['django_username'],
                                    password=register_form.cleaned_data['password'])
                if user:
                    login(request, user)
                    return redirect(reverse('index'))
                else:
                    print('failed register')
            except IntegrityError:
                register_form.add_error(None, 'Username already taken or email address is already in use.')
        else:
            print('form not valid')
    else:
        register_form = RegisterForm()
    return render(request, 'register.html', {'form': register_form})


def tags_parser(tags_string):
    tags_array = tags_string.split(',')
    tags_objects = Tag.objects.get_ot_create_tags(tags_array)
    return tags_objects


@csrf_protect
@login_required
def ask(request):
    if request.method == 'POST':
        new_question_form = NewQuestionForm(data=request.POST)
        if new_question_form.is_valid():
            tags = tags_parser(new_question_form.cleaned_data['tags'])
            new_question = Question.objects.create(title=new_question_form.cleaned_data['title'],
                                                   text=new_question_form.cleaned_data['text'],
                                                   user=Profile.objects.get(user=request.user))
            for question_tag in tags:
                _, question_id = question_tag
                new_question.tags.add(question_id)
            new_question.save()
            return redirect(f"/question/{new_question.id}")
    return render(request, 'ask.html')


def tag(request, tag_name):
    questions_by_tag = Question.objects.get_by_tag(tag_name)
    pages = paginator(questions_by_tag, request)
    return render(request, 'tag.html', {'questions': pages, 'tag_name': tag_name})


def update_user_credentials(request):
    user_edit_form = UserEditForm(data=request.POST)
    if user_edit_form.is_valid():
        current_user_profile, current_user = Profile.objects.get_current_user_profile(request.user)
        user_form_data = user_edit_form.cleaned_data
        if user_form_data['django_username']:
            current_user.username = user_form_data['django_username']
        if user_form_data['email']:
            current_user.email = user_form_data['email']
        if user_form_data['username']:
            current_user_profile.displayed_name = user_form_data['username']
        current_user_profile.save()
        current_user.save()
        return True
    return False


@csrf_protect
@login_required
def profile(request):
    if request.method == 'POST':
        if update_user_credentials(request):
            return redirect('profile')
    return render(request, 'profile.html')


def logout_view(request):
    logout(request)
    return redirect(reverse('index'))


def member(request):
    return HttpResponseNotFound("<h1>Page not found</h1>")
