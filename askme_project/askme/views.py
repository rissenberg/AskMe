from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from . import models


def paginate(contact_list, request, pages):
    paginator = Paginator(contact_list, pages)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    context = {'questions': models.QUESTIONS}
    return render(request, 'index.html', {'page_obj': paginate(models.QUESTIONS, request, 4)})


def hot(request):
    context = {'questions': models.QUESTIONS}
    return render(request, 'hot.html', {'page_obj': paginate(models.QUESTIONS, request, 4)})


def tag(request):
    context = {'questions': models.QUESTIONS}
    return render(request, 'tag.html', {'page_obj': paginate(models.QUESTIONS, request, 4)})


def question(request, question_id):
    if question_id > models.QUESTIONS.__len__():
        return render(request, '404.html')
    context = {'question': models.QUESTIONS[question_id]}
    return render(request, 'question.html', {'page_obj': paginate(models.ANSWERS, request, 3)})


def ask(request):
    return render(request, 'ask.html')


def settings(request):
    return render(request, 'settings.html')


def signin(request):
    return render(request, 'signin.html')


def login(request):
    return render(request, 'login.html')


def base(request):
    return render(request, 'inc/base.html')


def exception404(request, exception):
    return render(request, '404.html', status=404)
