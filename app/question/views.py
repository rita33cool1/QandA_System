#from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
#from .models import UserProfile
from ..models import Expertise
from ..models import QuestionForm
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse
#from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
#from .serializer import TokenSerializer
from .serializer import QuestionSerializer
from .serializer import DeleteQuestionSerializer
from rest_framework.authtoken.models import Token


##--------------------API-------------------##
success_msg = 'Success'

@api_view(['POST'])
def PostQuestion(request, format='json'):
    serializer = QuestionSerializer(data=request.data)
    if serializer.is_valid():
        question = serializer.save()
        json = {
                "msg": success_msg, 
                "question_id": question.id
                }
        return Response(json, status=status.HTTP_202_ACCEPTED)
    json = {"msg": serializer.errors}
    return Response(json, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def ModifyQuestion(request, format='json'):
    try: question_id = request.data['question_id']
    except: error_msg = 'No question_id'
    else:
        if QuestionForm.objects.filter(id__exact=question_id):
            question_instance = QuestionForm.objects.get(id=question_id)
            serializer = QuestionSerializer(question_instance, data=request.data, partial=True)
            if serializer.is_valid():
                question = serializer.save()
                json = {"msg": success_msg}
                return Response(json, status=status.HTTP_202_ACCEPTED)
            else: error_msg = serializer.errors
        else: error_msg = 'This question_id does not exist.'
    json = {"msg": error_msg}
    return Response(json, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def DeleteQuestion(request, format='json'):
    serializer = DeleteQuestionSerializer(data=request.data)
    if serializer.is_valid():
        question_id = serializer.data['question_id']
        token = serializer.data['key']
        question = QuestionForm.objects.get(id=question_id)
        if Token.objects.get(key=token).user_id == question.user_id:
            question.delete()
            json = {"msg": success_msg}
            return Response(json, status=status.HTTP_202_ACCEPTED)
        else: error_msg = 'The author of the question does not match the token.'
    else: error_msg = serializer.errors
    json = {"msg": error_msg}
    return Response(json, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def GetQuestion(request, pk):
    if not QuestionForm.objects.filter(id=pk):
       error_msg = 'Wrong question id'
    else:
        question = QuestionForm.objects.get(id=pk)
        exps = []
        for exp in question.expertises.all():
            exps.append(exp.expertise)
        json = {
                "username": question.user.username,
                "title": question.title,
                "content": question.content,
                "create_date": question.create_date,
                "modify_date": question.mod_date,
                "reply_number": question.reply_number,
                "hashtags": exps,
                "msg": success_msg
                }
        return Response(json, status=status.HTTP_200_OK)
    json = {"msg": error_msg}
    return Response(json, status=status.HTTP_400_BAD_REQUEST)
