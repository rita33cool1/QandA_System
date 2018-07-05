from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from ..models import UserProfile
from ..models import Expertise
from rest_framework.authtoken.models import Token
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

class ExpertiseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Expertise
        fields = ('expertise')
class GetUserProfileSerializer(serializers.ModelSerializer):
    expertises = ExpertiseSerializer(many=True, read_only= True)
    class Meta:
        model = UserProfile
        fields = ('expertises',)

class GetUserListSerializer(serializers.ModelSerializer):
    users = GetUserProfileSerializer( read_only= True)
    class Meta:
        model = User
        fields = ('username', 'id', 'users')
