from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from ..models import UserProfile
from ..models import QuestionForm
from ..models import AnswerForm
from ..models import CommentForm
from ..models import Expertise
from rest_framework.authtoken.models import Token
from django.utils import timezone
import re

def GetUserFromToken(key):
    if Token.objects.filter(key__exact=key):
        token = Token.objects.get(key=key)
        user = User.objects.get(id=token.user_id)
        return user
    else:
        return None

class QuestionSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
            max_length=128,            
            required=True,
            )

    content = serializers.CharField(
            max_length=10000,
            )

    create_date = serializers.DateTimeField(
            default=serializers.CreateOnlyDefault(timezone.now),
            )

    expertises = serializers.ListField(
            child=serializers.CharField(max_length=32),
            )
    
    key = serializers.CharField(
            label='token',
            min_length=40,
            max_length=40,
            required=True
            )

    def validate_key(self, key):
        if not Token.objects.filter(key__exact=key):
            raise serializers.ValidationError("This token does exist")
        return key
    
    def create(self, validated_data):
        user = GetUserFromToken(validated_data['key'])
        question = QuestionForm(
                user=user,
                title=validated_data['title'],
                content=validated_data['content'],
                create_date=validated_data['create_date'],
                )
        question.save()
        print('tag: ', validated_data['expertises'])
        for tag in validated_data['expertises']:
            try: htag = Expertise.objects.get(expertise=tag)
            except:    
                htag = Expertise(expertise=tag)
                htag.save()
            question.save()
            question.expertises.add(htag)
        return question

    def update(self, instance, validated_data):
        user = GetUserFromToken(validated_data['key'])
        if instance.user_id != user.id :
            raise serializers.ValidationError('The author of the question does not match the token.')
        else:
            try: instance.title = validated_data['title']
            except: print('No title')
            try: instance.content = validated_data['content']
            except: print('No content,')
            try: validated_data['expertises']
            except: print('No expertises')
            else:
                instance.expertises.clear()
                for tag in validated_data['expertises']:
                    try: htag = Expertise.objects.get(expertise=tag)
                    except:    
                        htag = Expertise(expertise=tag)
                        htag.save()
                    instance.expertises.add(htag)
            instance.save()
            return instance 
        
    class Meta:
        model = QuestionForm 
        fields = ('key', 'title', 'content', 'create_date', 'expertises')   


class DeleteQuestionSerializer(serializers.ModelSerializer):
    key = serializers.CharField(
            min_length=40,
            max_length=40,
            required=True
            )
    
    question_id = serializers.IntegerField(
            required=True
            )

    def validate_key(self, key):
        if not Token.objects.filter(key__exact=key):
            raise serializers.ValidationError("This token does not exist")
        return key
     
    def validate_question_id(self, question_id):
        if not QuestionForm.objects.filter(id__exact=question_id):
            raise serializers.ValidationError("This question ID does not exist")
        return question_id        

    class Meta:
        model = QuestionForm 
        fields = ('key', 'question_id')   

    
class GetQuestionSerializer(serializers.ModelSerializer):
    class  Meta:
        model = QuestionForm
        fields = '__all__' 

class AnswerSerializer(serializers.ModelSerializer):
    question_id = serializers.IntegerField(
            required=True
            )

    content = serializers.CharField(
            max_length=10000,
            required=True
            )

    create_date = serializers.DateTimeField(
            default=serializers.CreateOnlyDefault(timezone.now),
            )

    key = serializers.CharField(
            label='token',
            min_length=40,
            max_length=40,
            required=True
            )

    def validate_question_id(self, question_id):
        if not QuestionForm.objects.filter(id__exact=question_id):
            raise serializers.ValidationError("This question ID does not exist")
        return question_id        
    
    def validate_key(self, key):
        if not Token.objects.filter(key__exact=key):
            raise serializers.ValidationError("This token does not exist")
        return key
    
    def create(self, validated_data):
        user = GetUserFromToken(validated_data['key'])
        question=QuestionForm.objects.get(id=validated_data['question_id']) 
        answer = AnswerForm(
                user=user,
                question=question, 
                content=validated_data['content'],
                create_date=validated_data['create_date'],
                )
        answer.save()
        return answer

    def update(self, instance, validated_data):
        user = GetUserFromToken(validated_data['key'])
        if instance.user_id != user.id :
            raise serializers.ValidationError('The author of the answer does not match the token.')
        else:
            try: instance.content = validated_data['content']
            except: serializers.ValidationError('The content cannot be blank')
            instance.save()
            return instance 
        
    class Meta:
        model = AnswerForm 
        fields = ('key', 'content', 'create_date', 'question_id')   

class DeleteAnswerSerializer(serializers.ModelSerializer):
    key = serializers.CharField(
            min_length=40,
            max_length=40,
            required=True
            )
    
    answer_id = serializers.IntegerField(
            required=True
            )

    def validate_key(self, key):
        if not Token.objects.filter(key__exact=key):
            raise serializers.ValidationError("This token does not exist")
        return key
     
    def validate_answer_id(self, answer_id):
        if not AnswerForm.objects.filter(id__exact=answer_id):
            raise serializers.ValidationError("This answer ID does not exist")
        return answer_id        
    
    def validate(self, data):
        if Token.objects.get(key=data['key']).user_id != AnswerForm.objects.get(id=data['answer_id']).user_id:
            raise serializers.ValidationError('The author of the answer does not match the token.')
        return data

    class Meta:
        model = AnswerForm 
        fields = ('key', 'answer_id')   

class GetAnswerSerializer(serializers.ModelSerializer):
    class  Meta:
        model = AnswerForm
        fields = '__all__' 

class CommentSerializer(serializers.ModelSerializer):
    question_id = serializers.IntegerField(
            required=True
            )

    answer_id = serializers.IntegerField()

    content = serializers.CharField(
            max_length=10000,
            required=True
            )

    create_date = serializers.DateTimeField(
            default=serializers.CreateOnlyDefault(timezone.now),
            )

    QorA = serializers.CharField(
            required=True
            )

    key = serializers.CharField(
            label='token',
            min_length=40,
            max_length=40,
            required=True
            )

    def validate_question_id(self, question_id):
        if not QuestionForm.objects.filter(id__exact=question_id):
            raise serializers.ValidationError("This question ID does not exist")
        return question_id        
    
    def validate_QorA(self, QorA):
        if QorA != 'question' and QorA != 'answer':
            raise serializers.ValidationError("QorA only can be 'question' or 'answer'. That is, you should define this comment is under a question or an answer")
        return QorA
    
    def validate_key(self, key):
        if not Token.objects.filter(key__exact=key):
            raise serializers.ValidationError("This token does not exist")
        return key
    
    def create(self, validated_data):
        user = GetUserFromToken(validated_data['key'])
        question = QuestionForm.objects.get(id=validated_data['question_id'])
        if validated_data['QorA'] == 'question': 
            answer = AnswerForm.objects.get(id=1)
        else: 
            if not AnswerForm.objects.filter(id=validated_data['answer_id']):
                raise serializers.ValidationError("This answer ID does not exist")
            answer = AnswerForm.objects.get(id=validated_data['answer_id']) 
            if answer.question.id != question.id:
                raise serializers.ValidationError("This answer is not under the question.") 
        comment = CommentForm(
                user=user,
                question=question, 
                answer=answer,
                content=validated_data['content'],
                create_date=validated_data['create_date'],
                )
        comment.save()
        return comment

    def update(self, instance, validated_data):
        user = GetUserFromToken(validated_data['key'])
        if instance.user_id != user.id :
            raise serializers.ValidationError('The author of the comment does not match the token.')
        else:
            try: instance.content = validated_data['content']
            except: serializers.ValidationError('The content cannot be blank')
            instance.save()
            return instance 
        
    class Meta:
        model = AnswerForm 
        fields = ('key', 'content', 'create_date', 'question_id', 'answer_id', 'QorA')   

class DeleteCommentSerializer(serializers.ModelSerializer):
    key = serializers.CharField(
            min_length=40,
            max_length=40,
            required=True
            )
    
    comment_id = serializers.IntegerField(
            required=True
            )

    def validate_key(self, key):
        if not Token.objects.filter(key__exact=key):
            raise serializers.ValidationError("This token does not exist")
        return key
     
    def validate_comment_id(self, comment_id):
        if not CommentForm.objects.filter(id__exact=comment_id):
            raise serializers.ValidationError("This comment ID does not exist")
        return comment_id        
    
    def validate(self, data):
        if Token.objects.get(key=data['key']).user_id != CommentForm.objects.get(id=data['comment_id']).user_id:
            raise serializers.ValidationError('The author of the comment does not match the token.')
        return data

    class Meta:
        model = AnswerForm 
        fields = ('key', 'comment_id')   

class GetCommentSerializer(serializers.ModelSerializer):
    class  Meta:
        model = CommentForm
        fields = '__all__' 

class VoteForQuestionSerializer(serializers.ModelSerializer):
    QorA = serializers.CharField(
            required=True
            )
   
    question_id = serializers.IntegerField(
            required=True
            )

    vote = serializers.IntegerField(
            required=True
            )

    key = serializers.CharField(
            label='token',
            min_length=40,
            max_length=40,
            required=True
            )
    
    def validate_vote(self, vote):
        if vote != 1 and vote != -1 and vote != 0:
            raise serializers.ValidationError("Vote only can be 1, 0 or -1, which represents you like or dislike this post.")
        return vote
    
    def validate_key(self, key):
        if not Token.objects.filter(key__exact=key):
            raise serializers.ValidationError("This token does not exist")
        return key
    
    def validate(self, data):
        user = User.objects.get(id=Token.objects.get(key=data['key']).user.id)
        question = QuestionForm.objects.get(id=data['question_id'])
        if user == question.user:
            raise serializers.ValidationError('You cannot vote for your own question.')
        return data 

    class Meta:
        model = QuestionForm 
        fields = ('key', 'question_id', 'QorA', 'vote')   

class VoteForAnswerSerializer(serializers.ModelSerializer):
    QorA = serializers.CharField(
            required=True
            )
   
    answer_id = serializers.IntegerField(
            required=True
            )

    vote = serializers.IntegerField(
            required=True
            )

    key = serializers.CharField(
            label='token',
            min_length=40,
            max_length=40,
            required=True
            )

    def validate_vote(self, vote):
        if vote != 1 and vote != -1:
            raise serializers.ValidationError("Vote only can be 1 or -1, which represents you like or dislike this post.")
        return vote
    
    def validate_key(self, key):
        if not Token.objects.filter(key__exact=key):
            raise serializers.ValidationError("This token does not exist")
        return key
    
    def validate(self, data):
        user = User.objects.get(id=Token.objects.get(key=data['key']).user.id)
        answer = AnswerForm.objects.get(id=data['answer_id'])
        if user == answer.user:
                raise serializers.ValidationError('You cannot vote for your own answer.')
        return data 

    class Meta:
        model = AnswerForm 
        fields = ('key', 'answer_id', 'QorA', 'vote')   

class StarAnswerSerializer(serializers.ModelSerializer):
    question_id = serializers.IntegerField(
            required=True
            )

    answer_id = serializers.IntegerField(
            required=True
            )

    key = serializers.CharField(
            label='token',
            min_length=40,
            max_length=40,
            required=True
            )
    
    def validate_question_id(self, question_id):
        if not QuestionForm.objects.filter(id__exact=question_id):
            raise serializers.ValidationError("This question ID does not exist")
        return question_id        
    
    def validate_answer_id(self, answer_id):
        if not AnswerForm.objects.filter(id__exact=answer_id):
            raise serializers.ValidationError("This answer ID does not exist")
        return answer_id        
    
    def validate_key(self, key):
        if not Token.objects.filter(key__exact=key):
            raise serializers.ValidationError("This token does not exist")
        return key
    
    def validate(self, data):
        user = User.objects.get(id=Token.objects.get(key=data['key']).user.id)
        question = QuestionForm.objects.get(id=data['question_id'])
        answer = AnswerForm.objects.get(id=data['answer_id'])
        if user != question.user:
            raise serializers.ValidationError('The author of the question does not match the token.')
        is_answer = False
        for ans in AnswerForm.objects.filter(question_id=question.id):
            if ans.id == answer.id:
                is_answer = True
                break
        if is_answer == False:
            raise serializers.ValidationError('This answer is not under this question')
        return data 

    class Meta:
        model = QuestionForm 
        fields = ('key', 'question_id', 'answer_id')   

