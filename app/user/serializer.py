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
            )
    username = serializers.CharField(
            label='Username',
            required=True,
            )
    password = serializers.CharField(
            label='Password', 
            min_length=6, 
            max_length=32,
            required=True, 
            write_only=True)
  
    def validate_username(self, username):
        if User.objects.filter(username=username):
            raise serializers.ValidationError('This username has been registered, please choose another one.')
        return username    
     
    def validate_email(self, email):
        if User.objects.filter(email=email):
            raise serializers.ValidationError('This email has been registered, please choose another one.')
        return email 

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
            raise serializers.ValidationError("This token does not exist")
        return key
    
    class Meta:
        model = Token
        fields = ('key','user_id')    

class SetExpertiseSerializer(serializers.ModelSerializer):
    expertises = serializers.ListField(
            child=serializers.CharField(max_length=32),
            )

#    def validate_expertises(self, expertises):
#        if len(expertises) == 0:
#            raise serializers.ValidationError('Please enter the new expertises')
#        return expertises    

    class Meta:
        model = UserProfile
        fields = (['expertises'])    

class AddFriendSerializer(serializers.ModelSerializer):
    friends = serializers.ListField(
            child=serializers.CharField(),
            )
    key = serializers.CharField(
            label='token',
            min_length=40,
            max_length=40,
            required=True
            )

    def validate_key(self, key):
        if not Token.objects.filter(key__exact=key):
            raise serializers.ValidationError("This token does not exist")
        return key
    
    def validate_friends(self, friends):
        if len(friends) == 0:
            raise serializers.ValidationError('Please enter the new friends')
        else:
            for f in friends:
                if not User.objects.filter(username__exact=f):
                    raise serializers.ValidationError('The user '+f+' is not exist')        
        return friends

    def validate(self, data):
        token = Token.objects.get(key=data['key'])
        for f in data['friends']:
            if User.objects.get(username=f).id == token.user_id:
                raise serializers.ValidationError('You cannot add yourself as your friend.')
            else:
                for uf in UserProfile.objects.get(user_id=token.user_id).friends.all():
                    if f == str(uf.user):
                        raise serializers.ValidationError('The user '+f+' has been your friend.')
        return data
    
    class Meta:
        model = UserProfile
        fields = ('key', 'friends')    


class DelFriendSerializer(serializers.ModelSerializer):
    friends = serializers.ListField(
            child=serializers.CharField(),
            )
    key = serializers.CharField(
            label='token',
            min_length=40,
            max_length=40,
            required=True
            )

    def validate_key(self, key):
        if not Token.objects.filter(key__exact=key):
            raise serializers.ValidationError("This token does not exist")
        return key
    
    def validate_friends(self, friends):
        if len(friends) == 0:
            raise serializers.ValidationError('Please enter the new friends')
        else:
            for f in friends:
                if not User.objects.filter(username__exact=f):
                    raise serializers.ValidationError('The user '+f+' is not exist')        
        return friends

    def validate(self, data):
        token = Token.objects.get(key=data['key'])
        for f in data['friends']:
            if User.objects.get(username=f).id == token.user_id:
                raise serializers.ValidationError('Yourself is not your friend.')
            else:
                is_friend = False
                for uf in UserProfile.objects.get(user_id=token.user_id).friends.all():
                    if f == str(uf.user): 
                        is_friend = True
                        break
                if not is_friend: raise serializers.ValidationError('The user '+f+' has not been your friend.')
        return data
    
    class Meta:
        model = UserProfile
        fields = ('key', 'friends')    

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
