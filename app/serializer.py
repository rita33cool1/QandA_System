from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from .models import UserProfile
from .models import QuestionForm
from .models import Hashtag
from drf_braces.serializers.form_serializer import FormSerializer
from rest_framework.authtoken.models import Token
from django.utils import timezone
import re

def email_check(email):
    pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")
    return re.match(pattern, email)

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            label='Email',
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    username = serializers.CharField(
            label='Username',
            min_length=6,
            max_length=32,
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(
            label='Password', 
            min_length=6, 
            max_length=32,
            required=True, 
            write_only=True)
   
    def create(self, validated_data):
        if not email_check(validated_data['email']):
            raise serializers.ValidationError("Your email format is wrong!")
        
        user = User.objects.create_user(username=validated_data['username'], email=validated_data['email'], password=validated_data['password'])
        user_profile = UserProfile(user=user)
        user_profile.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
            min_length=6,
            max_length=32,
            required=True
            )
    password = serializers.CharField(
            min_length=6, 
            max_length=32,
            required=True
            )
    def validate_username(self, username):
        print('validates username: ', username)
            
        filter_result = User.objects.filter(username__exact=username)
        if not filter_result:
            raise serializers.ValidationError("This username does not exist. Please register first.")

        return username

    class Meta:
        model = User
        fields = ('username', 'password')    

class TokenSerializer(serializers.ModelSerializer):
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
    
    class Meta:
        model = Token
        fields = ('key','user_id')    

class SetProfileSerializer(serializers.ModelSerializer):
    expertises = serializers.ListField(
            child=serializers.CharField(max_length=32),
            )
    
    class Meta:
        model = UserProfile
        fields = (['expertises'])    


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

    hashtags = serializers.ListField(
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
        print('tag: ', validated_data['hashtags'])
        for tag in validated_data['hashtags']:
            htag = Hashtag(hashtag=tag)
            htag.save()
            question.hashtags.add(htag)
        question.save()
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
            try: validated_data['hashtags']
            except: print('No hasgtags')
            else:
                instance.hashtags.clear()
                for tag in validated_data['hashtags']:
                    htag = Hashtag(hashtag=tag)
                    htag.save()
                    instance.hashtags.add(htag)
            instance.save()
            return instance 
        
    class Meta:
        model = QuestionForm 
        fields = ('key', 'title', 'content', 'create_date', 'hashtags')   


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
            raise serializers.ValidationError("This token does exist")
        return key
     
    def validate_question_id(self, question_id):
        if not QuestionForm.objects.filter(id__exact=question_id):
            raise serializers.ValidationError("This question ID does exist")
        return question_id        

    class Meta:
        model = QuestionForm 
        fields = ('key', 'question_id')   
    

