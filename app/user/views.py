from django.contrib.auth.models import User
from ..models import UserProfile
from ..models import Expertise
from ..models import Friend
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponseNotFound
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import filters
from .serializer import UserSerializer
from .serializer import LoginSerializer
from .serializer import TokenSerializer
from .serializer import SetExpertiseSerializer
from .serializer import GetUserListSerializer
from .serializer import AddFriendSerializer
from rest_framework.authtoken.models import Token
from django_filters.rest_framework import DjangoFilterBackend

##--------------------API-------------------##
success_message = 'Success'
error_message = 'Error'
httpstatus = status.HTTP_200_OK
def ParseErrorMsg(msg):
    print(msg)
    if len(msg.keys()) == 0:
        return None
    for k in msg.keys():
        key = k
        break
    return msg[key][0]

@api_view(['POST'])
def UserCreate(request, format='json'):
    serializer = UserSerializer(data=request.data)
    if request.data['username'] == '':
        error_msg = 'Please enter your username.'
    elif request.data['password'] == '':
        error_msg = 'Please enter your password'
    elif request.data['email'] == '':
        error_msg = 'Please enter your email'
    else:
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = {'msg':success_message }
                return Response(json, status=httpstatus)
        error_msg = ParseErrorMsg(serializer.errors)
    json = {      
            "msg": error_message,
            "errorMsg": error_msg
            }
    return Response(json, status=httpstatus)

@api_view(['POST'])
def UserDelete(request, format='json'):
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        token_key = serializer.data['key']
        token = Token.objects.get(key=token_key)
        user = User.objects.get(id=token.user_id)
        user.delete()
        json = {'msg':success_message}
        return Response(json, status=httpstatus)
    json = {
            'msg': error_message,
            'errorMsg': ParseErrorMsg(serializer.errors)
            }
    return Response(json, status=httpstatus)



@api_view(['POST'])
def UserLogin(request, format='json'):
    serializer = LoginSerializer(data=request.data)
    if request.data['username'] == '':
        error_msg = 'Please enter your username.' 
    elif request.data['password'] == '':
        error_msg = 'Please enter your password' 
    else:
        if serializer.is_valid():
            username = serializer.data['username']
            password = serializer.data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                if not Token.objects.filter(user_id__exact=user.id):
                    token = Token.objects.create(user=user)
                else:
                    token = Token.objects.get(user_id=user.id)
                json = {'msg':success_message, 'key':token.key}
                return Response(json, status=httpstatus)
        error_msg = ParseErrorMsg(serializer.errors)
    json = {
            "msg": error_message,
            "errorMsg": error_msg
            }
    return Response(json, status=httpstatus)
@api_view(['POST'])
def GetProfile(request, format='json'):
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        token_key = serializer.data['key']
        token = Token.objects.get(key=token_key)
        user = User.objects.get(id=token.user_id)
        profile = UserProfile.objects.get(user_id=token.user_id)
        exps = []
        for exp in profile.expertises.all():
            exps.append(exp.expertise)
        friends = []
        for f in profile.friends.all():
            friends.append(f.user.username)
        json = {
                'msg': success_message, 
                'username': user.username, 
                'email':user.email, 
                'expertise':exps,
                'friends': friends
                }
        return Response(json, status=httpstatus)
    
    json = {
            'msg': error_message,
            'errorMsg': ParseErrorMsg(serializer.errors)
            }       
    return Response(json, status=httpstatus)

@api_view(['POST'])
def AddFriend(request, format='json'):
    token_serializer = TokenSerializer(data=request.data)
    friend_serializer = AddFriendSerializer(data=request.data)
    if token_serializer.is_valid():
        token_key = token_serializer.data['key']
        token = Token.objects.get(key=token_key)
        if friend_serializer.is_valid():
            friend_list = friend_serializer.data['friends']
            profile = UserProfile.objects.get(user_id=token.user_id)
            for f in friend_list:
                print('f', f)
                user = User.objects.get(username=f)
                friend = Friend(user=user)
                friend.save()
                profile.save()
                profile.friends.add(friend)
            json = {'msg': success_message}
            return Response(json, status=httpstatus)
    print('token: ', token_serializer.errors)
    print('friend: ', friend_serializer.errors)
    if ParseErrorMsg(token_serializer.errors) == None:
        error_msg = ParseErrorMsg(friend_serializer.errors)
    else: error_msg = ParseErrorMsg(token_serializer.errors)
    json = {'msg':error_message, 'errorMsg': error_msg}
    return Response(json, status=httpstatus)

@api_view(['POST'])
def SetExpertise(request, format='json'):
    token_serializer = TokenSerializer(data=request.data)
    profile_serializer = SetExpertiseSerializer(data=request.data)
    if token_serializer.is_valid():
        token_key = token_serializer.data['key']
        token = Token.objects.get(key=token_key)
        if profile_serializer.is_valid():
            expertise_str = profile_serializer.data['expertises']
            profile = UserProfile.objects.get(user_id=token.user_id)
            profile.expertises.clear()
            for exp in expertise_str:
                exper = Expertise(expertise=exp)
                exper.save()
                profile.save()
                profile.expertises.add(exper)
            json = {'msg': success_message} #, 'expertise':exps}
            return Response(json, status=httpstatus)
    if ParseErrorMsg(token_serializer.errors) == None:
        error_msg = ParseErrorMsg(profile_serializer.errors)
    else: error_msg = ParseErrorMsg(token_serializer.errors)
    json = {'msg':error_message, 'errorMsg': error_msg}
    return Response(json, status=httpstatus)

class GetUserList(generics.ListAPIView):
    serializer_class = GetUserListSerializer
    lookup_url_kwarg = "username"
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username')
    def get_queryset(self):
        queryset = User.objects.all()
        username = self.request.query_params.get('username', None)
        if username is not None:
            return queryset.filter(username__contains=username)
            
        else:
            return queryset
