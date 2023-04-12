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
from askme import views


urlpatterns = [
    path('', views.index, name="index"),
    path('hot/', views.hot, name="hot"),
    path('base/', views.base),
    path('question/<int:question_id>/', views.question, name="question"),
    path('admin/', admin.site.urls),
    path('404/', views.exception404),
    path('ask/', views.ask, name="ask"),
    path('settings/', views.settings, name="settings"),
    path('login/', views.login, name="login"),
    path('signin/', views.signin, name="signin"),
]


handler404 = "askme.views.exception404"
