from django.urls import re_path
from . import views
from .user import views as user_views
from .question import views as quest_views
from django.conf.urls import url

app_name = 'users'
urlpatterns = [
    url(r'api/users/register/$', user_views.UserCreate, name='account_create'),
    url(r'api/users/login/$', user_views.UserLogin, name='account_login'),
    url(r'api/users/profile/$', user_views.GetProfile, name='get_profile'),
    url(r'api/users/set_profile/$', user_views.SetProfile, name='set_profile'),
    url(r'api/users/post_question/$', quest_views.PostQuestion, name='post_question'),
    url(r'api/users/modify_question/$', quest_views.ModifyQuestion, name='modify_question'),
    url(r'api/get_question/(?P<pk>\d+)/$', quest_views.GetQuestion, name='get_question'),
]
