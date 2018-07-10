from django.contrib.auth.models import User
from ..models import Expertise
from ..models import QuestionForm
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
from .serializer import QuestionSerializer
from .serializer import GetQuestionSerializer
from .serializer import DeleteQuestionSerializer
from rest_framework.authtoken.models import Token


##--------------------API-------------------##
success_msg = 'Success'
error_message = 'Error'
httpstatus = status.HTTP_200_OK

@api_view(['POST'])
def PostQuestion(request, format='json'):
    serializer = QuestionSerializer(data=request.data)
    if serializer.is_valid():
        question = serializer.save()
        json = {
                "msg": success_msg, 
                "question_id": question.id
                }
        return Response(json, status=status.httpstatus)
    json = {"msg": serializer.errors}
    return Response(json, status=httpstatus)

@api_view(['POST'])
def ModifyQuestion(request, format='json'):
    try: question_id = request.data['question_id']
    except: error_msg = 'No question_id or format is wrong'
    else:
        if QuestionForm.objects.filter(id__exact=question_id):
            question_instance = QuestionForm.objects.get(id=question_id)
            serializer = QuestionSerializer(question_instance, data=request.data, partial=True)
            if serializer.is_valid():
                question = serializer.save()
                json = {"msg": success_msg}
                return Response(json, status=httpstatus)
            else: error_msg = serializer.errors
        else: error_msg = 'This question_id does not exist.'
    json = {"msg": error_msg}
    return Response(json, status=httpstatus)

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
            return Response(json, status=httpstatus)
        else: error_msg = 'The author of the question does not match the token.'
    else: error_msg = serializer.errors
    json = {"msg": error_msg}
    return Response(json, status=httpstatus)


def GetQuestionByID(id):
    question = QuestionForm.objects.get(id=id)
    exps = []
    for exp in question.expertises.all():
        exps.append(exp.expertise)
    json = {
            "question_id": id,
            "username": question.user.username,
            "title": question.title,
            "content": question.content,
            "create_date": question.create_date,
            "modify_date": question.mod_date,
            "reply_number": question.reply_number,
            "expertises": exps,
            }
    return json

@api_view(['GET'])
def GetQuestion(request, pk):
    if pk == '0':
        quests = []
        for quest in QuestionForm.objects.all():
            quests.append({"question": GetQuestionByID(quest.id)})
        json = {
                "msg": success_msg,
                "questions": quests
                }
        return Response(json, status=httpstatus)
    else:
        if not QuestionForm.objects.filter(id=pk):
            error_msg = 'Wrong question id'
        else:
            json =GetQuestionByID(pk)
            return Response(json, status=httpstatus)
        json = {"msg": error_msg}
        return Response(json, status=httpstatus)


class GetQuestionList(generics.ListAPIView):
    serializer_class = GetQuestionSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('user_id', 'id')
    def get_queryset(self):
        queryset = QuestionForm.objects.all()
        uid = self.request.query_params.get('uid', None)
        qid = self.request.query_params.get('qid', None)
        if uid is None and qid is None:
            return queryset
        elif uid is not None and qid is not None:
            return queryset.filter(user__exact=uid).filter(id__exact=qid)
        elif uid is not None:
            return queryset.filter(user__exact=uid)
        else:
            return queryset.filter(id__exact=qid)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = GetQuestionSerializer(queryset, many=True)
        usernames = {}
        for quest in serializer.data:
            quest['user_id'] = quest['user']
            quest['user'] = User.objects.get(id=quest['user_id']).username
            exps = []
            for eid in quest['expertises']:
                exps.append(Expertise.objects.get(id=eid).expertise)
            quest['expertises']=exps 
        return Response(serializer.data)
    


