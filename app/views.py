import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponseNotFound, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import urlencode
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods

from app.forms import RegisterForm, LoginForm, UserEditForm, NewQuestionForm, NewAnswerForm
from app.models import Question, Answer, Tag, Profile


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
def question_view(request, question_id):
    try:
        single_question = Question.objects.get_by_id(question_id)
    except Question.DoesNotExist:
        raise Http404
    answers = Answer.objects.get_answers_for_question(question_id)
    pages = paginator(answers, request)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            current_url = request.get_full_path()
            login_url = reverse('login')
            question_url = urlencode({'next': current_url})
            login_redirect_url = f"{login_url}?{question_url}"
            return HttpResponseRedirect(login_redirect_url)

        answer_form = NewAnswerForm(request.POST)
        if answer_form.is_valid():
            answer = Answer.objects.create(
                question=single_question,
                text=answer_form.cleaned_data['answer_text'],
                user=Profile.objects.get(user=request.user)
            )
            answer.save()
            single_question.answers_count += 1
            single_question.save()
            return redirect('question', question_id=single_question.id)
    else:
        answer_form = NewAnswerForm()

    return render(request, 'question.html', {
        'question': single_question,
        'answers': pages,
        'form': answer_form
    })


@csrf_protect
def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            user = authenticate(request, username=login_form.cleaned_data['django_username'],
                                password=login_form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                if request.GET.get('next'):
                    return redirect(request.GET['next'])
                return redirect('index')
            else:
                login_form.add_error(None, 'Invalid username or password')
    else:
        login_form = LoginForm()
    return render(request, 'login.html', {'form': login_form})


@csrf_protect
def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        register_form = RegisterForm(data=request.POST, files=request.FILES)
        for error in register_form.errors:
            print(error)
        if register_form.is_valid():
            try:
                new_user = User.objects.create_user(username=register_form.cleaned_data['django_username'],
                                                    email=register_form.cleaned_data['email'],
                                                    password=register_form.cleaned_data['password'])
                new_user.save()
                Profile.objects.create_profile(new_user, register_form.cleaned_data['username'],
                                               register_form.cleaned_data['profile_img'])
                user = authenticate(request, username=register_form.cleaned_data['django_username'],
                                    password=register_form.cleaned_data['password'])
                if user:
                    login(request, user)
                    return redirect(reverse('index'))
            except IntegrityError:
                register_form.add_error(None, 'Username already taken or email address is already in use.')
    else:
        register_form = RegisterForm()
    return render(request, 'register.html', {'form': register_form})


def tags_parser(tags_string):
    tags_array = []
    if ',' in tags_string:
        tags_array = tags_string.split(',')
    elif ' ' in tags_string:
        tags_array = tags_string.split(' ')
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
    else:
        new_question_form = NewQuestionForm()
    return render(request, 'ask.html', {'form': new_question_form})


def tag(request, tag_name):
    questions_by_tag = Question.objects.get_by_tag(tag_name)
    pages = paginator(questions_by_tag, request)
    return render(request, 'tag.html', {'questions': pages, 'tag_name': tag_name})


@csrf_protect
@login_required
def profile(request):
    if request.method == 'POST':
        user_edit_form = UserEditForm(data=request.POST, files=request.FILES)
        if user_edit_form.is_valid():
            current_user_profile, current_user = Profile.objects.get_current_user_profile(request.user)
            user_form_data = user_edit_form.cleaned_data
            if user_form_data['django_username']:
                current_user.username = user_form_data['django_username']
            if user_form_data['email']:
                current_user.email = user_form_data['email']
            if user_form_data['username']:
                current_user_profile.displayed_name = user_form_data['username']
            if user_form_data['profile_img']:
                current_user_profile.avatar = user_form_data['profile_img']
            current_user_profile.save()
            current_user.save()
            return redirect('profile')
    else:
        user_edit_form = UserEditForm()
    return render(request, 'profile.html', {'form': user_edit_form})


def logout_view(request):
    logout(request)
    return redirect(reverse('index'))


@require_http_methods(['POST'])
@login_required
def change_rating(request, card_id):
    card_data = json.loads(request.body)
    card_type = card_data['card_type']
    current_rating = card_data['current_rating']
    if card_type == 'question':
        question = Question.objects.get(id=card_id)
        current_user = request.user
        if current_user != question.user:
            Profile.objects.set_new_rating(current_user, card_id, card_type, current_rating)
    return JsonResponse({'success': True})
