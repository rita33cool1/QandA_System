from django.contrib.auth.models import User
from ..models import UserProfile
from ..models import Expertise
from ..models import Friend
from ..models import QuestionForm
from django.contrib import auth
#from django.http import HttpResponseRedirect
#from django.urls import reverse
#from django.http import HttpResponseNotFound
#from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework import generics
from rest_framework import filters
from .serializer import UserSerializer
from .serializer import LoginSerializer
from .serializer import TokenSerializer
from .serializer import ExpertiseSerializer
from .serializer import SetExpertiseSerializer
from .serializer import GetExpertiseListSerializer
from .serializer import GetQuestionSerializer
from .serializer import GetUserListSerializer
#from django_filters.rest_framework import DjangoFilterBackend

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

def getEleFromM2Mfield(all_objs, field):
    all_list = []
    if field == '':
        for ele in all_objs:
            all_list.append(ele)
    else:
        for ele in all_objs:
            all_list.append(ele[field])
    return all_list

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

    def list(self, request):
        queryset = self.get_queryset()
        serializer = GetUserListSerializer(queryset, many=True)
        for ori_data in serializer.data:
            ori_data['user_id'] = ori_data['id']
            del ori_data['id']
            user = User.objects.get(id=ori_data['user_id'])
            profile = UserProfile.objects.get(user_id=ori_data['user_id'])
            ori_data['email'] = user.email
            ori_data['friends'] = getEleFromM2Mfield(profile.friends.all().values(), 'friend')
            ori_data['expertises'] = getEleFromM2Mfield(profile.expertises.all().values(), 'expertise')
            
        return Response(serializer.data)

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
        expected_friends = []
        print(profile.expected_friends.all())
        for f in profile.expected_friends.all():
            expected_friends.append(f.user.username)
        friend_requests = []
        print(profile.friend_requests.all())
        for f in profile.friend_requests.all():
            friend_requests.append(f.user.username)
        json = {
                'msg': success_message, 
                'username': user.username, 
                'email':user.email, 
                'expertise':exps,
                'friends': friends,
                'expected_friends': expected_friends,
                'friend_requests': friend_requests
                }
        return Response(json, status=httpstatus)
    
    json = {
            'msg': error_message,
            'errorMsg': ParseErrorMsg(serializer.errors)
            }       
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
                if Expertise.objects.filter(expertise__exact=exp):
                    exper = Expertise.objects.get(expertise=exp)
                else:
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

def RemoveDuplic(datas):
    no_du_data = []
    for data in datas:
        if len(no_du_data)==0:
            no_du_data.append(data)
        else:
            is_duplic = False
            for nd_data in no_du_data:
                if data == nd_data:
                    is_duplic = True
                    break
            if not is_duplic:
                no_du_data.append(data)
    return no_du_data

class GetExpertiseList(generics.ListAPIView):
    serializer_class = GetExpertiseListSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('expertises__expertise')
    def get_queryset(self):
        queryset = Expertise.objects.all()
        exp = self.request.query_params.get('key', None)
        if exp is None:
            return queryset
        else:
            #return queryset.filter(expertises__contains=exp)
            return queryset.filter(expertise__contains=exp)

    def get_queryset_user(self):
        queryset = UserProfile.objects.all()
        exp = self.request.query_params.get('key', None)
        if exp is None:
            return queryset
        else:
            #return queryset.filter(expertises__contains=exp)
            return queryset.filter(expertises__expertise__contains=exp)

    def get_queryset_question(self):
        queryset = QuestionForm.objects.all()
        exp = self.request.query_params.get('key', None)
        if exp is None:
            return queryset
        else:
            return queryset.filter(expertises__expertise__contains=exp)

    def list(self, request):
        expertise = self.request.query_params.get('key', None)
        queryset = self.get_queryset()
        queryset_user = self.get_queryset_user()
        queryset_question = self.get_queryset_question()
        serializer = GetExpertiseListSerializer(queryset, many=True)
        exps = []
        users = []
        questions = []
        for exp in queryset.values():
            category = {
                        "expertise": exp['expertise'],
                        "users": users,
                        "questions": questions
                        }
            exps.append(category)
        # response related user
        serializer = GetExpertiseListSerializer(queryset_user, many=True)
        for ori_data in RemoveDuplic(serializer.data):
            if len(ori_data['expertises']) > 0:
                for ori_exp in ori_data['expertises']:
                    for exp in exps:
                        if ori_exp['expertise'] == exp['expertise']:
                            user = []
                            for u in exp['users']:
                                user.append(u)
                            user.append({
                                "user_id": ori_data['user_id'],
                                "username": User.objects.get(id=ori_data['user_id']).username
                                })
                            exp['users'] = user
                            break
        # response related question
        serializer = GetQuestionSerializer(queryset_question, many=True)
        for ori_data in RemoveDuplic(serializer.data):
        #for ori_data in serializer.data:
            if len(ori_data['expertises']) > 0:
                for ori_exp in ori_data['expertises']:
                    for exp in exps:
                        if ori_exp['expertise'] == exp['expertise']:
                            user = []
                            for u in exp['questions']:
                                user.append(u)
                            user.append({
                                "question_id": ori_data['id'],
                                "title": QuestionForm.objects.get(id=ori_data['id']).title,
                                "user_id": ori_data['user_id'],
                                "username": User.objects.get(id=ori_data['user_id']).username
                                })
                            exp['questions'] = user
                            break
        return Response(exps)


