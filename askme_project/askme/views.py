from django.forms import model_to_dict
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.urls import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib import auth

from . import models
from .forms import AskForm, AnswerForm, LoginForm, RegistrationForm, EditForm

from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


PAGINATION_SIZE = 5
top_users = models.Profile.objects.get_top_users()[:10]
top_tags = models.Tag.objects.get_hot_tags()[:10]


def paginate(objects, request):
    paginator = Paginator(objects, PAGINATION_SIZE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def create_content_right():
    content = {
        "tags": top_tags,
        "users": top_users,
    }

    return content


def create_content(objects, request):
    page = paginate(objects, request)
    content = create_content_right()
    content["content"] = page
    return content


def hot(request):
    return render(request, 'hot.html', create_content(models.Post.objects.get_hot_posts(), request))


def index(request):
    return render(request, 'index.html', create_content(models.Post.objects.get_recent_posts(), request))


def exception404(request, exception):
    return render(request, '404.html', status=404)


def question(request, i: int):
    if request.method == 'GET':
        form = AnswerForm()
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(reverse('login_page'))
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = models.Answer.objects.create(text=form.cleaned_data['text'],
                                                  question=models.Post.objects.get(id=i),
                                                  author=models.Profile.objects.get(user_id=request.user.id))
            answer.save()
            if answer:
                return redirect(reverse("question", args=[i]))

    content = create_content(models.Answer.objects.get_answers_for_question(i), request)
    try:
        content["question"] = models.Post.objects.get(id=i)
    except Exception:
        return render(request, '404.html', create_content_right())

    content['form'] = form

    return render(request, 'question.html', content)


def tag(request, title: str):
    content = create_content(models.Post.objects.get_posts_for_tag(title), request)
    try:
        content["tag"] = models.Tag.objects.get_tag_by_title(title)
    except Exception:
        return render(request, '404.html', create_content_right())

    return render(request, 'tag.html', content)


def profile(request, i: int):
    content = create_content(models.Post.objects.get_questions_for_user(i), request)
    content["user"] = models.Profile.objects.get_user_by_id(i)
    return render(request, 'profile.html', content)


@login_required(login_url='login_page', redirect_field_name="continue")
def profile_settings(request):
    if request.method == 'GET':
        initial_data = model_to_dict(request.user)
        initial_data['avatar'] = request.user.profile_related.avatar
        initial_data['bio'] = request.user.profile_related.bio
        form = EditForm(initial=initial_data)
    elif request.method == 'POST':
        form = EditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse("profile_settings"))

    content = create_content_right()
    content['form'] = form
    return render(request, 'settings.html', content)


@login_required(login_url='login_page', redirect_field_name="continue")
def ask(request):
    if request.method == 'POST':
        ask_form = AskForm(request.POST)
        if ask_form.is_valid():
            quest = models.Post.objects.create(
                title=ask_form.cleaned_data['title'],
                text=ask_form.cleaned_data['text'],
                author=models.Profile.objects.get(user=request.user)
            )
            quest.save()
            for tag_ in ask_form.cleaned_data['tags'].split(' '):
                to_add = models.Tag.objects.get_or_create(title=tag_)
                quest.tags.add(to_add[0].id)
            quest.save()
            if quest:
                return redirect("question", i=quest.id)

    elif request.method == 'GET':
        ask_form = AskForm()

    content = create_content_right()
    content['form'] = ask_form
    return render(request, 'ask.html', content)


def login_view(request):
    if request.method == 'POST':
        user_form = LoginForm(data=request.POST)
        if user_form.is_valid():
            user = authenticate(request, **user_form.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect(reverse('index'))
            else:
                user_form.add_error(field=None, error="Wrong Login/Password")
    elif request.method == 'GET':
        user_form = LoginForm()

    content = create_content_right()
    content["form"] = user_form
    return render(request, 'login.html', content)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def signin(request):
    if request.method == 'POST':
        user_form = RegistrationForm(data=request.POST, files=request.FILES)
        if user_form.is_valid():
            user = user_form.save()
            if user:
                login(request, user)
                return redirect(reverse('index'))
            else:
                return redirect(reverse('signin'))
    elif request.method == 'GET':
        user_form = RegistrationForm()

    content = create_content_right()
    content["form"] = user_form
    return render(request, 'signin.html', content)


@require_POST
@login_required(login_url='login_page', redirect_field_name="continue")
def like_question(request):
    quest_id = request.POST['quest_id']
    quest = models.Post.objects.get(id=quest_id)
    try:
        like = models.LikeQ.objects.get(question_id=quest_id, user_id=request.user.profile_related.id)
    except models.LikeQ.DoesNotExist:
        like = models.LikeQ.objects.create(question=quest, user=request.user.profile_related)
        like.save()
    else:
        like.delete()

    quest.save()
    return JsonResponse(
        {'status': 'ok',
         'likes_count': quest.get_like_count()})


@require_POST
@login_required(login_url='login_page', redirect_field_name="continue")
def like_answer(request):
    answer_id = request.POST['answer_id']
    answer = models.Answer.objects.get(id=answer_id)
    try:
        like = models.LikeA.objects.get(answer_id=answer_id, user_id=request.user.profile_related.id)
    except models.LikeA.DoesNotExist:
        like = models.LikeA.objects.create(answer=answer, user=request.user.profile_related)
        like.save()
    else:
        like.delete()
    answer.save()
    return JsonResponse(
        {'status': 'ok',
         'likes_count': answer.get_like_count()})


@require_POST
@login_required(login_url='login_page', redirect_field_name="continue")
def correct(request):
    answer_id = request.POST['answer_id']
    answer = models.Answer.objects.get(id=answer_id)
    if answer.question.get_author_id() != request.user.id:
        JsonResponse(
            {'sus': 'forbidden'})
        return
    answer.solution = not answer.is_solution()
    answer.save()
    return JsonResponse(
            {'sus': 'ok',
             'solution': f'{answer.is_solution()}'}
        )
