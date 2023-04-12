from django.http import HttpResponse
from django.shortcuts import render
from . import models


def index(request):
    context = {'questions': models.QUESTIONS}
    return render(request, 'index.html', context)


def hot(request):
    context = {'questions': models.QUESTIONS}
    return render(request, 'hot.html', context)


def question(request, question_id):
    if question_id > models.QUESTIONS.__len__():
        return render(request, '404.html')
    context = {'question': models.QUESTIONS[question_id], 'answers': models.ANSWERS}
    return render(request, 'question.html', context)


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