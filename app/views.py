from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import UserProfile
from .models import Expertise
from .models import QuestionForm
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import UserSerializer
from .serializer import LoginSerializer
from .serializer import TokenSerializer
from .serializer import SetProfileSerializer
from .serializer import QuestionSerializer
from .serializer import DeleteQuestionSerializer
from rest_framework.authtoken.models import Token


##--------------------API-------------------##

class UserCreate(APIView):

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                success_message = 'Success!'
                json = {'msg':success_message}
                return Response(json, status=status.HTTP_201_CREATED)
        json = {'msg':serializer.errors}
        return Response(json, status=status.HTTP_400_BAD_REQUEST)



class UserLogin(APIView):

    def post(self, request, format='json'):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            
            username = serializer.data['username']
            password = serializer.data['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None and user.is_active:
                auth.login(request, user)
                success_message = 'Authoriented user'
                if not Token.objects.filter(user_id__exact=user.id):
                    token = Token.objects.create(user=user)
                else:
                    token = Token.objects.get(user_id=user.id)
                    success_message = 'Authoriented user and has been logged in'
                json = {'msg':success_message, 'token':token.key}
                return Response(json, status=status.HTTP_202_ACCEPTED)
        json = {'msg':serializer.errors}       
        return Response(json, status=status.HTTP_400_BAD_REQUEST)

class GetProfile(APIView): 
    def post(self, request, format='json'):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            token_key = serializer.data['key']
            token = Token.objects.get(key=token_key)
            user = User.objects.get(id=token.user_id)
            profile = UserProfile.objects.get(user_id=token.user_id)
            exps = []
            for exp in profile.expertises.all():
                exps.append(exp.expertise)
            json = {'msg':'Get profile successfully', 'username': user.username, 'email':user.email, 'expertise':exps}
            return Response(json, status=status.HTTP_202_ACCEPTED)
        
        json = {'msg':serializer.errors}       
        return Response(json, status=status.HTTP_400_BAD_REQUEST)

class SetProfile(APIView): 
    def post(self, request, format='json'):
        token_serializer = TokenSerializer(data=request.data)
        profile_serializer = SetProfileSerializer(data=request.data)
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
                exps = []
                for exp in profile.expertises.all():
                    exps.append(exp.expertise)
                json = {'msg':'Set profile successfully', 'expertise':exps}
                return Response(json, status=status.HTTP_202_ACCEPTED)
        json = {'msg':token_serializer.errors+profile_serializer.errors}
        return Response(json,status=status.HTTP_400_BAD_REQUEST)

class PostQuestion(APIView):
    def post(self, request, format='json'):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            question = serializer.save()
            json = {
                    "msg": "Post the question successfully.", 
                    "question_id": question.id
                    }
            return Response(json, status=status.HTTP_202_ACCEPTED)
        json = {"msg": serializer.errors}
        return Response(json, status=status.HTTP_400_BAD_REQUEST)

class ModifyQuestion(APIView):
    def post(self, request, format='json'):
        try: question_id = request.data['question_id']
        except: error_msg = 'No question_id'
        else:
            if QuestionForm.objects.filter(id__exact=question_id):
                question_instance = QuestionForm.objects.get(id=question_id)
                serializer = QuestionSerializer(question_instance, data=request.data, partial=True)
                if serializer.is_valid():
                    question = serializer.save()
                    json = {"msg": 'Modify question successfully'}
                    return Response(json, status=status.HTTP_202_ACCEPTED)
                else: error_msg = serializer.errors
            else: error_msg = 'This question_id does not exist.'
        json = {"msg": error_msg}
        return Response(json, status=status.HTTP_400_BAD_REQUEST)

class DeleteQuestion(APIView):
    def post(self, request, format='json'):
        serializer = DeleteQuestionSerializer(data=request.data)
        if serializer.is_valid():
            question_id = serializer.data['question_id']
            token = serializer.data['key']
            question = QuestionForm.objects.get(id=question_id)
            if Token.objects.get(key=token).user_id == question.user_id:
                question.delete()
                json = {"msg": 'Delete question successfully'}
                return Response(json, status=status.HTTP_202_ACCEPTED)
            else: error_msg = 'The author of the question does not match the token.'
        else: error_msg = serializer.errors
        json = {"msg": error_msg}
        return Response(json, status=status.HTTP_400_BAD_REQUEST)
        


