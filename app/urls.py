from django.urls import re_path
from . import views
from django.conf.urls import url

app_name = 'users'
urlpatterns = [
    url(r'api/users/register/$', views.UserCreate.as_view(), name='account_create'),
    url(r'api/users/login/$', views.UserLogin.as_view(), name='account_login'),
    url(r'api/users/profile/$', views.GetProfile.as_view(), name='get_profile'),
    url(r'api/users/set_profile/$', views.SetProfile.as_view(), name='set_profile'),
    url(r'api/users/post_question/$', views.PostQuestion.as_view(), name='post_question'),
    url(r'api/users/modify_question/$', views.ModifyQuestion.as_view(), name='modify_question'),
    url(r'api/users/delete_question/$', views.DeleteQuestion.as_view(), name='delete_question'),
]
