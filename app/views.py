from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render
from django.urls import reverse

from app.forms import RegisterForm
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


def question(request, question_id):
    single_question = Question.objects.get_by_id(question_id)
    answers = Answer.objects.get_answers_for_question(question_id)
    pages = paginator(answers, request)
    return render(request, 'question.html', {'question': single_question, 'answers': pages})


def loginn(request):
    return render(request, 'login.html')


def register(request):
    if request.method == "POST":
        register_form = RegisterForm(data=request.POST)
        for field in register_form:
            print("Field Error:", field.name, field.errors)
        if register_form.is_valid():
            new_user = User.objects.create_user(username=register_form.cleaned_data['django_username'],
                                                email=register_form.cleaned_data['email'],
                                                password=register_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create_profile(new_user, register_form.cleaned_data['username'])
            user = authenticate(request, username=register_form.cleaned_data['django_username'], password=register_form.cleaned_data['password'])
            print(new_user.username)
            if user:
                login(request, user)
                return redirect(reverse('index'))
            else:
                print('failed register')
        else:
            print('form not valid')

    return render(request, 'register.html')


def ask(request):
    return render(request, 'ask.html')


def tag(request, tag_name):
    questions_by_tag = Question.objects.get_by_tag(tag_name)
    pages = paginator(questions_by_tag, request)
    return render(request, 'tag.html', {'questions': pages, 'tag_name': tag_name})


def profile(request):
    return render(request, 'profile.html')


def logout(request):
    return redirect('/login')


def member(request):
    return HttpResponseNotFound("<h1>Page not found</h1>")
