from django.urls import re_path
from . import views
from .user import views as user_views
from .question import views as quest_views
from django.conf.urls import url

app_name = 'app'
urlpatterns = [
    url(r'user/register/$', user_views.UserCreate, name='account_create'),
    url(r'user/login/$', user_views.UserLogin, name='account_login'),
    url(r'user/profile/$', user_views.GetProfile, name='get_profile'),
    url(r'user/profile/update/$', user_views.SetProfile, name='set_profile'),
    url(r'question/post/$', quest_views.PostQuestion, name='post_question'),
    url(r'question/modify/$', quest_views.ModifyQuestion, name='modify_question'),
    url(r'question/(?P<pk>\d+)/$', quest_views.GetQuestion, name='get_question'),
]
