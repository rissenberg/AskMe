from django.http import HttpResponse
from django.shortcuts import render
from . import models


def index(request):
    context = {'questions': models.QUESTIONS}
    return render(request, 'index.html', context)


def question(request, question_id):
    context = {'question': models.QUESTIONS[question_id]}
    return render(request, 'question.html', context)


def base(request):
    return render(request, 'inc/base.html')