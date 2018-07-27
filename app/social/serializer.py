from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from ..models import UserProfile
from ..models import Expertise
from ..models import QuestionForm
from rest_framework.authtoken.models import Token
import re

class AddFriendRequestSerializer(serializers.ModelSerializer):
    requester = serializers.CharField(
            required=True
    )
    replyer = serializers.CharField(
            required=True
    )
    key = serializers.CharField(
            min_length=40,
            max_length=40,
            required=True
            )

    def validate_requester(self, requester):
        try: user = User.objects.get(username=requester)
        except: raise serializers.ValidationError('The user '+requester+" does not exist")
        if not Token.objects.filter(user_id__exact=user.id):
            raise serializers.ValidationError(requester+" has not logined")
        return requester
    
    def validate_replyer(self, replyer):
        try: user = User.objects.get(username=replyer)
        except: raise serializers.ValidationError('The user '+replyer+" does not exist")
        return replyer

    def validate_key(self, key):
        try: Token.objects.get(key=key)
        except: raise serializers.ValidationError('The user has not logined.')
        return key

    def validate(self, data):
        if data['requester'] == data['replyer']:
            raise serializers.ValidationError('You cannot add yourself as your friend.')
        elif Token.objects.get(key=data['key']).user_id != User.objects.get(username=data['requester']).id:
            raise serializers.ValidationError('The request is not sent by the account holder') 
        else:
            requester = User.objects.get(username=data['requester'])
            for uf in UserProfile.objects.get(user=requester).friends.all():
                if str(data['replyer']) == str(uf.user):
                    raise serializers.ValidationError('The user '+data['replyer']+' has been your friend.')
            for uef in UserProfile.objects.get(user=requester).expected_friends.all():
                if str(data['replyer']) == str(uef.user):
                    raise serializers.ValidationError('You have sent the request to the user '+data['replyer'])
        return data
    
    class Meta:
        model = UserProfile
        fields = ('key', 'requester', 'replyer')    

class ConfirmFriendRequestSerializer(serializers.ModelSerializer):
    requester = serializers.CharField(
            required=True
    )
    replyer = serializers.CharField(
            required=True
    )
    action = serializers.CharField(
            required=True
    )
    key = serializers.CharField(
            min_length=40,
            max_length=40,
            required=True
            )

    def validate_requester(self, requester):
        try: user = User.objects.get(username=requester)
        except: raise serializers.ValidationError('The user '+requester+" does not exist")
        return requester
    
    def validate_replyer(self, replyer):
        try: user = User.objects.get(username=replyer)
        except: raise serializers.ValidationError('The user '+replyer+" does not exist")
        if not Token.objects.filter(user_id__exact=user.id):
            raise serializers.ValidationError(replyer+" has not logined")
        return replyer

    def validate_key(self, key):
        try: Token.objects.get(key=key)
        except: raise serializers.ValidationError('The user has not logined.')
        return key

    def validate_action(self, action):
        if action != 'reject' and action != 'accept':
            raise serializers.ValidationError('The action only can be reject or accept')
        return action

    def validate(self, data):
        if Token.objects.get(key=data['key']).user_id != User.objects.get(username=data['replyer']).id:
            raise serializers.ValidationError('The reply is not sent by the account holder') 
        else:
            requester = User.objects.get(username=data['requester'])
            is_friend = False
            for uef in UserProfile.objects.get(user=requester).expected_friends.all():
                if str(data['replyer']) == str(uef.user):
                    is_friend = True
                    break
                if not is_friend:
                    raise serializers.ValidationError('The user '+data['rquester']+' cancel the request or did not send the request.')
            replyer = User.objects.get(username=data['replyer'])
            is_friend = False
            for ufr in UserProfile.objects.get(user=replyer).friend_requests.all():
                if str(data['requester']) == str(ufr.user):
                    is_friend = True
                    break
                if not is_friend:
                    raise serializers.ValidationError('The user '+data['replyer']+' did not receive the request from '+data['requester']+'. Or the requester '+data['requester']+' did not send the request.')
        return data
    
    class Meta:
        model = UserProfile
        fields = ('action', 'key', 'requester', 'replyer')    

class DelFriendSerializer(serializers.ModelSerializer):
    friend = serializers.CharField(
            required=True
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
    
    def validate_friend(self, friend):
        if not User.objects.filter(username__exact=friend):
            raise serializers.ValidationError('The user '+friend+' is not exist')        
        return friend

    def validate(self, data):
        token = Token.objects.get(key=data['key'])
        if User.objects.get(username=data['friend']).id == token.user_id:
            raise serializers.ValidationError('Yourself is not your friend.')
        else:
            is_friend = False
            for uf in UserProfile.objects.get(user_id=token.user_id).friends.all():
                if data['friend'] == str(uf.user): 
                    is_friend = True
                    break
            if not is_friend: raise serializers.ValidationError('The user '+f+' has not been your friend.')
        return data
    
    class Meta:
        model = UserProfile
        fields = ('key', 'friend')    


