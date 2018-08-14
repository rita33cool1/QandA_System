from django.urls import re_path
from .user import views as user_views
from .social import views as social_views
from .question import views as quest_views
from django.conf.urls import url

app_name = 'app'
urlpatterns = [
    url(r'user/register/$', user_views.UserCreate, name='account_create'),
    url(r'user/login/$', user_views.UserLogin, name='account_login'),
    url(r'user/profile/$', user_views.GetProfile, name='get_profile'),
    url(r'users/list/$', user_views.GetUserList.as_view(), name='user_list'),
    url(r'user/expertise/update/$', user_views.SetExpertise, name='set_expertise'),
    url(r'expertises/search$', user_views.GetExpertiseList.as_view(), name='expertise_list'),
    
    url(r'social/friend/send/$', social_views.AddFriendRequest, name='send_friend_request'),
    url(r'social/friend/confirm/$', social_views.ConfirmFriendRequest, name='confirm_friend_request'),
    url(r'social/friend/delete/$', social_views.DelFriend, name='delete_friend'),
    url(r'social/following/add/$', social_views.AddFollowing, name='add_following'),
    url(r'social/following/cancel/$', social_views.CancelFollowing, name='cancel_following'),
    #url(r'social/star/give/$', social_views.GiveStar, name='give_star'),
    #url(r'social/star/cancel/$', social_views.CancelStar, name='cancel_star'),
    
    url(r'questions/list/$', quest_views.GetQuestionList.as_view(), name='question_list'),
    url(r'question/post/$', quest_views.PostQuestion, name='post_question'),
    url(r'question/edit/$', quest_views.ModifyQuestion, name='modify_question'),
    url(r'question/delete/$', quest_views.DeleteQuestion, name='delete_question'),
    url(r'question/$', quest_views.GetQuestion.as_view(), name='get_question'),
    url(r'questions/$', quest_views.GetQuestionList.as_view(), name='question_list'),
    url(r'question/answer/post/$', quest_views.PostAnswer, name='post_answer'),
    url(r'question/answer/edit/$', quest_views.ModifyAnswer, name='modify_answer'),
    url(r'question/answer/delete/$', quest_views.DeleteAnswer, name='delete_answer'),
    url(r'question/comment/post/$', quest_views.PostComment, name='post_comment'),
    url(r'question/comment/edit/$', quest_views.ModifyComment, name='modify_comment'),
    url(r'question/comment/delete/$', quest_views.DeleteComment, name='delete_comment'),
]
