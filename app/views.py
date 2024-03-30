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
        'text': f"This is an answer {i}",
    } for i in range(10)
]


def index(request):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(QUESTIONS, 5)
    pages = paginator.get_page(page_num)
    return render(request, 'index.html', {'questions': pages, 'page_name': 'index'})

def hot(request):
    return render(request, 'hot.html', {'questions': QUESTIONS[::-1]})

def question(request, question_id):
    single_question = QUESTIONS[question_id]
    return render(request, 'question.html', {'question': single_question, 'answers': ANSWERS})