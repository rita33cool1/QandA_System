from django.urls import re_path
#from . import views
from .user import views as user_views
from .question import views as quest_views
from django.conf.urls import url

app_name = 'app'
urlpatterns = [
    url(r'user/register/$', user_views.UserCreate, name='account_create'),
    url(r'user/login/$', user_views.UserLogin, name='account_login'),
    url(r'user/profile/$', user_views.GetProfile, name='get_profile'),
    url(r'user/expertise/update/$', user_views.SetExpertise, name='set_expertise'),
    url(r'user/friend/add/$', user_views.AddFriend, name='add_friend'),
    url(r'user/friend/delete/$', user_views.DelFriend, name='delete_friend'),
    url(r'users/list/$', user_views.GetUserList.as_view(), name='user_list'),
    url(r'expertises/list/$', user_views.GetExpertiseList.as_view(), name='expertise_list'),
    url(r'question/post/$', quest_views.PostQuestion, name='post_question'),
    url(r'question/edit/$', quest_views.ModifyQuestion, name='modify_question'),
    url(r'question/delete/$', quest_views.DeleteQuestion, name='delete_question'),
    url(r'question/(?P<pk>\d+)/$', quest_views.GetQuestion, name='get_question'),
    url(r'questions/$', quest_views.GetQuestionList.as_view(), name='question_list'),
]
