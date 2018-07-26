from django.contrib.auth.models import User
from ..models import UserProfile
from ..models import Friend
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework import generics
from rest_framework import filters
from .serializer import AddFriendRequestSerializer
from .serializer import ConfirmFriendRequestSerializer

##--------------------API-------------------##
success_message = 'Success'
error_message = 'Error'
httpstatus = status.HTTP_200_OK
def ParseErrorMsg(msg):
    print(msg)
    if len(msg.keys()) == 0:
        return None
    for k in msg.keys():
        key = k
        break
    msg = key + ": " + msg[key][0]
    return msg

def getEleFromM2Mfield(all_objs, field):
    all_list = []
    for ele in all_objs:
        all_list.append(ele[field])
    return all_list

@api_view(['POST'])
def AddFriendRequest(request, format='json'):
    serializer = AddFriendRequestSerializer(data=request.data)
    blank = False
    if serializer.is_valid():
        requester = User.objects.get(username=serializer.data['requester'])
        replyer = User.objects.get(username=serializer.data['replyer'])
        if Friend.objects.filter(user_id__exact=requester.id):
            friend = Friend.objects.get(user_id=requester.id)
        else:
            friend = Friend(user=requester)
            friend.save()
        profile = UserProfile.objects.get(user_id=replyer.id)
        profile.save()
        profile.friend_requests.add(friend)        
        
        if Friend.objects.filter(user_id__exact=replyer.id):
            friend = Friend.objects.get(user_id=replyer.id)
        else:
            friend = Friend(user=replyer)
            friend.save()
        profile = UserProfile.objects.get(user_id=requester.id)
        profile.save()
        profile.expected_friends.add(friend)        
        json = {"msg": success_message}
        return Response(json, status=httpstatus)
    else: error_msg = ParseErrorMsg(serializer.errors)
    json = {'msg':error_message, 'errorMsg': error_msg}
    return Response(json, status=httpstatus)

@api_view(['POST'])
def ConfirmFriendRequest(request, format='json'):
    serializer = ConfirmFriendRequestSerializer(data=request.data)
    blank = False
    if serializer.is_valid():
        requester = User.objects.get(username=serializer.data['requester'])
        replyer = User.objects.get(username=serializer.data['replyer'])
        req_friend = Friend.objects.get(user_id=requester.id)
        rep_profile = UserProfile.objects.get(user_id=replyer.id)
        rep_profile.friend_requests.remove(req_friend)        
        rep_friend = Friend.objects.get(user_id=replyer.id)
        req_profile = UserProfile.objects.get(user_id=requester.id)
        req_profile.expected_friends.remove(rep_friend)     
        if serializer.data['action'] == 'reject':  
            json = {"msg": success_message}
            return Response(json, status=httpstatus)
        elif serializer.data['action'] == 'accept':
            req_profile.save()
            req_profile.friends.add(rep_friend)
            rep_profile.save()
            rep_profile.friends.add(req_friend)
            json = {"msg": success_message}
            return Response(json, status=httpstatus)
    else: error_msg = ParseErrorMsg(serializer.errors)
    json = {'msg':error_message, 'errorMsg': error_msg}
    return Response(json, status=httpstatus)



"""
@api_view(['POST'])
def DelFriend(request, format='json'):
    serializer = DelFriendSerializer(data=request.data)
    blank = False
    for f in request.data['friends']:
        if f == '': blank = True
    if request.data['key'] == '':    
        error_msg = 'key cannot be blank.'
    elif blank: 
        error_msg = 'friends cannot be blank.'
    elif serializer.is_valid():
        token_key = serializer.data['key']
        token = Token.objects.get(key=token_key)
        friend_list = serializer.data['friends']
        profile = UserProfile.objects.get(user_id=token.user_id)
        for f in friend_list:
            user = User.objects.get(username=f)
            friend = Friend.objects.get(user_id=user.id)
            profile.friends.remove(friend)
        json = {'msg': success_message}
        return Response(json, status=httpstatus)
    else: error_msg = ParseErrorMsg(serializer.errors)
    json = {'msg':error_message, 'errorMsg': error_msg}
    return Response(json, status=httpstatus)
"""


