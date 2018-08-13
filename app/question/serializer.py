from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from ..models import UserProfile
from ..models import QuestionForm
from ..models import AnswerForm
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
        question.answer_number+=1
        question.save()
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

