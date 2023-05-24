"""
URL configuration for askme_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('hot/', views.hot, name='hot'),
    path('questions/<int:i>/', views.question, name="question"),
    path('ask/', views.ask, name="ask_form"),
    path('login/', views.login_view, name="login_page"),
    path('logut', views.logout_view, name="logout"),
    path('register/', views.signin, name="register"),
    path('tag/<str:title>/', views.tag, name="tag"),
    path('profile/<int:i>/', views.profile, name="profile"),
    path('profile/settings/', views.profile_settings, name="profile_settings"),
    path('like/question', views.like_question, name='like_q'),
    path('like/answer', views.like_answer, name='like_a'),
    path('answer/correct', views.correct, name='correct')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)


handler404 = "askme.views.exception404"
