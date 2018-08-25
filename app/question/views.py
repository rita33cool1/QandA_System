from ..models import Vote
from ..models import Expertise
from ..models import QuestionForm
from ..models import AnswerForm
from ..models import CommentForm
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponseNotFound
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import filters
from rest_framework.authtoken.models import Token
from .serializer import QuestionSerializer
from .serializer import GetQuestionSerializer
from .serializer import DeleteQuestionSerializer
from .serializer import AnswerSerializer
from .serializer import DeleteAnswerSerializer
from .serializer import GetAnswerSerializer
from .serializer import CommentSerializer
from .serializer import DeleteCommentSerializer
from .serializer import GetCommentSerializer
from .serializer import VoteForQuestionSerializer
from .serializer import VoteForAnswerSerializer
from .serializer import StarAnswerSerializer


##--------------------API-------------------##
success_msg = 'Success'
error_msg = 'Error'
httpstatus = status.HTTP_200_OK

def ParseErrorMsg(msg):
    #print(msg)
    if len(msg.keys()) == 0:
        return None
    for k in msg.keys():
        key = k
        break
    if key == 'non_field_errors':
        msg = msg[key][0]
    else:
        msg = key + ": " + msg[key][0]
    return msg

@api_view(['POST'])
def PostQuestion(request, format='json'):
    serializer = QuestionSerializer(data=request.data)
    if serializer.is_valid():
        question = serializer.save()
        json = {
                "msg": success_msg, 
                "question_id": question.id
                }
        return Response(json, status=httpstatus)
    json = {
            "msg": error_msg, 
            "errorMsg": ParseErrorMsg(serializer.errors)
            }   
    return Response(json, status=httpstatus)

@api_view(['POST'])
def ModifyQuestion(request, format='json'):
    try: question_id = request.data['question_id']
    except: error_message = 'No question_id or format is wrong'
    else:
        if QuestionForm.objects.filter(id__exact=question_id):
            question_instance = QuestionForm.objects.get(id=question_id)
            serializer = QuestionSerializer(question_instance, data=request.data, partial=True)
            if serializer.is_valid():
                question = serializer.save()
                json = {"msg": success_msg}
                return Response(json, status=httpstatus)
            else: error_message = ParseErrorMsg(serializer.errors)
        else: error_message = 'This question_id does not exist.'
    json = {"msg": error_msg, "errorMsg": error_message}
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
        else: error_message = 'The author of the question does not match the token.'
    else: error_message = ParseErrorMsg(serializer.errors)
    json = {"msg": error_msg, "errorMsg": error_message}
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
            quest['expertises'] = exps
            quest['username'] = quest['user'] 
            del quest['user'] 
            quest['question_id'] = quest['id'] 
            del quest['id'] 
        return Response(serializer.data)

@api_view(['POST'])
def PostAnswer(request, format='json'):
    serializer = AnswerSerializer(data=request.data)
    if serializer.is_valid():
        answer = serializer.save()
        json = {
                "msg": success_msg, 
                "answer_id": answer.id
                }
        return Response(json, status=httpstatus)
    json = {
            "msg": error_msg, 
            "errorMsg": ParseErrorMsg(serializer.errors)
            }   
    return Response(json, status=httpstatus)

@api_view(['POST'])
def ModifyAnswer(request, format='json'):
    try: answer_id = request.data['answer_id']
    except: error_message = 'No answer ID or format is wrong'
    else:
        if AnswerForm.objects.filter(id__exact=answer_id):
            answer_instance = AnswerForm.objects.get(id=answer_id)
            serializer = AnswerSerializer(answer_instance, data=request.data, partial=True)
            if serializer.is_valid():
                answer = serializer.save()
                json = {"msg": success_msg}
                return Response(json, status=httpstatus)
            else: error_message = ParseErrorMsg(serializer.errors)
        else: error_message = 'This answer ID does not exist.'
    json = {"msg": error_msg, "errorMsg": error_message}
    return Response(json, status=httpstatus)

@api_view(['POST'])
def DeleteAnswer(request, format='json'):
    serializer = DeleteAnswerSerializer(data=request.data)
    if serializer.is_valid():
        answer = AnswerForm.objects.get(id=serializer.data['answer_id'])
        question = QuestionForm.objects.get(id=answer.question.id)
        if question.star_answer == answer.id:
            question.star_answer = 0
            question.save()
        answer.delete()
        json = {"msg": success_msg}
        return Response(json, status=httpstatus)
    json = {"msg": error_msg, "errorMsg": ParseErrorMsg(serializer.errors)}
    return Response(json, status=httpstatus)

@api_view(['POST'])
def PostComment(request, format='json'):
    serializer = CommentSerializer(data=request.data)
    try: QorA = request.data['QorA']
    except: print("No 'QorA' field")
    else:
        if request.data['QorA'] == 'answer':
            try: answer_id = request.data['answer_id']
            except: 
                json = {
                        "msg": error_msg, 
                        "errorMsg": 'No answer ID or format is wrong'
                        }   
                return Response(json, status=httpstatus)
        else: request.data['answer_id'] = 1
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        comment = serializer.save()
        json = {
                "msg": success_msg, 
                "comment_id": comment.id
                }
        return Response(json, status=httpstatus)
    json = {
            "msg": error_msg, 
            "errorMsg": ParseErrorMsg(serializer.errors)
            }   
    return Response(json, status=httpstatus)

@api_view(['POST'])
def ModifyComment(request, format='json'):
    try: comment_id = request.data['comment_id']
    except: error_message = 'No comment ID or format is wrong'
    else:
        if CommentForm.objects.filter(id__exact=comment_id):
            comment_instance = CommentForm.objects.get(id=comment_id)
            serializer = CommentSerializer(comment_instance, data=request.data, partial=True)
            if serializer.is_valid():
                comment = serializer.save()
                json = {"msg": success_msg}
                return Response(json, status=httpstatus)
            else: error_message = ParseErrorMsg(serializer.errors)
        else: error_message = 'This comment ID does not exist.'
    json = {"msg": error_msg, "errorMsg": error_message}
    return Response(json, status=httpstatus)

@api_view(['POST'])
def DeleteComment(request, format='json'):
    serializer = DeleteCommentSerializer(data=request.data)
    if serializer.is_valid():
        CommentForm.objects.get(id=serializer.data['comment_id']).delete()
        json = {"msg": success_msg}
        return Response(json, status=httpstatus)
    json = {"msg": error_msg, "errorMsg": ParseErrorMsg(serializer.errors)}
    return Response(json, status=httpstatus)

@api_view(['POST'])
def VotePost(request, format='json'):
    error_message = ""
    try: QorA = request.data['QorA']
    except: error_message = "You should enter the field QorA."
    else:
        if QorA == 'question':
            serializer = VoteForQuestionSerializer(data=request.data)
            try: post = QuestionForm.objects.get(id=request.data['question_id'])
            except: error_message = "The field question_id is wrong or not existing."
        elif QorA == 'answer':
            serializer = VoteForAnswerSerializer(data=request.data)
            try: post = AnswerForm.objects.get(id=request.data['answer_id'])
            except: error_message = "The field answer_id is wrong or not existing."
        else:
            error_message = "QorA only can be 'question' or 'answer'. That is, you should define this post is a question or an answer."

    if error_message == "" and serializer.is_valid():
        token = Token.objects.get(key=serializer.data['key'])
        user = User.objects.get(id=token.user.id)
        is_vote = False
        for v in post.votes.all():
            if v.user == user:
                is_vote = True
                vote_number = v.vote + int(serializer.data['vote'])
                if vote_number <= 1 and vote_number >= -1:
                    v.vote = vote_number
                    v.save()
        if not is_vote:
            vote = Vote(user=user, vote=serializer.data['vote'])
            vote.save()
            post.save()
            post.votes.add(vote)
        json = {"msg": success_msg}
        return Response(json, status=httpstatus)
    elif error_message == "":
        error_message = ParseErrorMsg(serializer.errors)
    
    json = {"msg": error_msg, "errorMsg": error_message}
    return Response(json, status=httpstatus)

@api_view(['POST'])
def StarAnswer(request, format='json'):
    serializer = StarAnswerSerializer(data=request.data)
    if serializer.is_valid():
        question = QuestionForm.objects.get(id=serializer.data['question_id'])
        answer = AnswerForm.objects.get(id=serializer.data['answer_id'])
        try: ori_answer = AnswerForm.objects.get(id=question.star_answer)
        except: pass
        else:
            ori_answer.star = False
            ori_answer.save()
        answer.star = True
        answer.save()
        question.star_answer = answer.id
        question.save()
        json = {"msg": success_msg}
        return Response(json, status=httpstatus)
    json = {"msg": error_msg, "errorMsg": ParseErrorMsg(serializer.errors)}
    return Response(json, status=httpstatus)

def CommentContentModfy(serializer_data, QorA):
    for data in serializer_data:
        data['user_id'] = data['user']
        data['user'] = User.objects.get(id=data['user_id']).username
        data['question_id'] = data['question']
        del data['question']
        if QorA == 'answer':
            data['answer_id'] = data['answer']
        del data['answer']

def ExtractVoters(serializer_data):
    for data in serializer_data:
        votes = []
        for v in data['votes']:
            vote = Vote.objects.get(id=v)
            if vote.vote != 0:
                votes.append({"voter": vote.user.username, "vote": vote.vote})
        data['votes'] = votes

class GetQuestion(generics.ListAPIView):
    serializer_class = GetQuestionSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('question_id', 'answer_id')
    def get_queryset(self):
        queryset = QuestionForm.objects.all()
        qid = self.request.query_params.get('qid', None)
        #if qid is None:
        if qid is None or qid == '1':
            return QuestionForm.objects.none()
        else:
            return queryset.filter(id__exact=qid)

    def get_queryset_answer(self):
        queryset = AnswerForm.objects.all()
        qid = self.request.query_params.get('qid', None)
        aid = self.request.query_params.get('aid', None)
        if aid is None:
            return queryset.filter(question__exact=qid)
        else:
            return queryset.filter(question__exact=qid, id__exact=aid)

    def get_queryset_comment(self):
        queryset = CommentForm.objects.all()
        qid = self.request.query_params.get('qid', None)
        aid = self.request.query_params.get('aid', None)
        if aid is None:
            return queryset.filter(question__exact=qid)
        else:
            return queryset.filter(question=qid, answer=aid).filter(question=qid, answer=1)

    def list(self, request):
        comment_queryset = self.get_queryset_comment()
        queryset = self.get_queryset()
        if not queryset:
            return Response(queryset)
        else:
            question_serializer = GetQuestionSerializer(queryset, many=True)
            user = User.objects.get(id=question_serializer.data[0]['user'])
            question_serializer.data[0]['user_id'] = user.id
            question_serializer.data[0]['user'] = user.username
            exps = [] 
            for ei in question_serializer.data[0]['expertises']:
                exps.append(Expertise.objects.get(id=ei).expertise)
            question_serializer.data[0]['expertises'] = exps
            ExtractVoters(question_serializer.data)
            if comment_queryset:
                comment_serializer = GetCommentSerializer(comment_queryset.filter(answer_id=1), many=True)
                CommentContentModfy(comment_serializer.data, 'question')
                question_serializer.data[0]['comments'] = comment_serializer.data
            result = {"question": question_serializer.data}
        queryset = self.get_queryset_answer()
        if queryset:
            answer_serializer = GetAnswerSerializer(queryset, many=True)
            ExtractVoters(answer_serializer.data)
            for ans in answer_serializer.data:               
                user = User.objects.get(id=ans['user'])
                ans['user_id'] = user.id
                ans['user'] = user.username
                if comment_queryset:
                    comment_serializer = GetCommentSerializer(comment_queryset.filter(answer_id=ans['id']), many=True)
                    CommentContentModfy(comment_serializer.data, 'answer')
                    ans['comments'] = comment_serializer.data
            result['answers'] = answer_serializer.data                

        return Response(result)



