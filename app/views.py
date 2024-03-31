from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.

QUESTIONS = [
    {
        'id': i,
        'title': f"Question {i}",
        'text': f"This is a question {i}",
    } for i in range(20)
]

ANSWERS = [
    {
        'id': i,
        'text': f"This is an answer {i}",
    } for i in range(10)
]

TAGS = [
    {
        'id': i,
        'name': f"Tag {i}"
    } for i in range(10)
]

def paginator(object_list, request, elems_per_page=5):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(object_list, elems_per_page)
    pages = paginator.get_page(page_num)
    return pages

def index(request):
    pages = paginator(QUESTIONS, request)
    return render(request, 'index.html', {'questions': pages, 'page_name': 'index'})

def hot(request):
    reversed_question = QUESTIONS[::-1]
    pages = paginator(reversed_question, request)
    return render(request, 'hot.html', {'questions': pages, 'page_name': 'hot'})

def question(request, question_id):
    single_question = QUESTIONS[question_id]
    pages = paginator(ANSWERS, request)
    return render(request, 'question.html', {'question': single_question, 'answers': pages, 'page_name': 'question', 'question_id': str(question_id)})

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def ask(request):
    return render(request, 'ask.html')

def tag(request, tag_name):
    pages = paginator(QUESTIONS, request)
    return render(request, 'tag.html', {'questions': pages, 'page_name': 'tag', 'tag_name': tag_name})
     
def profile(request):
    return render(request, 'profile.html')