# QandA_System
This is the server side of a Q&A system with social network.  
This server is developed on Django 2.0 and uses MySQL as database.  
  
Environment: Linux 16.04  
Developed Language: Python 3.5  
Django version: 2.0.6  
MySQL version: 14.14  
Data encolding: utf8  
Server display language: zh-TW  
  
### QandA_System/  
Including basical settings such as urls.  
### app/   
An app contains APIs.

## File Structure 
QandA_System/  
|── app  
│     |── admin.py  
│     |── apps.py  
│     |── __init__.py  
│     |── models.py  
│     |── question   
│     │   |── serializer.py  
│     │   └── views.py  
│     |── serializer.py  
│     |── tests.py  
│     |── urls.py  
│     |── user  
│     │   |── serializer.py  
│     │   └── views.py  
│     └── views.py  
|── manage.py  
|── QandA_System  
│     |── __init__.py  
│     |── settings.py  
│     |── urls.py  
│     └── wsgi.py  
|── README.md   
    
## Expected API  
+ Register
+ Login
+ Set User Profile
+ Get User Profile  
---  
+ Post Question
+ Modify Question
+ Get Question
+ Delete Question
+ Get User Question
---  
+ Post Reply
+ Modify Reply
+ Get Reply
+ Delete Reply
+ Get User Reply
---  
### User
#### Register  
Url: POST http://localhost:8000/accounts/api/users/register/  
I/O format: json  
Input: 
    {  
        "username": <username>,  
        "email": <email>,  
        "password": <password>  
    }  
Input details:  
  username: (require)  
  email: (require)  
  password: (require)  
Response: 
    {  
        "msg": <message>  
    }  
Response details:
<message>  
+ "Success": If register successfully.
+ Error message

#### Login
Url: POST http://localhost:8000/accounts/api/users/login/  
I/O format: json  
Input: 
    {  
        "username": <username>,  
        "email": <email>,  
        "password": <password>  
    }   
Input details:    
  username: (require)  
  password: (require)  
Response: 
    {  
        "msg": <message>,
        "token": <key>  
    }  
Response details:  
<message>  
+ "Success": If login successfully.  
+ Error message   
<key>  
    Use as logined authority


#### Get Profile  
Url: POST http://localhost:8000/accounts/api/users/profile/  
I/O format: json  
Input:   
    {  
        "key": <key>  
    }  
Input details:  
<key> (require)  
    To authrize the user has logined or not  
Respinse:  
    {  
        "msg": <message>,  
        "username": <username>,  
        "expertise": <expertises[]>,  
        "email": <email>  
    }  
Respinse details:  
<expertises[]>  
    String array with non-fixed length, ex. ["expertise1", "expertise2"] 

#### Set Profile
Url: POST http://localhost:8000/accounts/api/users/set_profile/  
I/O format: json  
Input:   
    {
        "key": <key>, 
        "expertises": <expertises[]>
    {  
Input details:  
<key>
    "msg": <message>,
    "expertise": <expertises[]>
}
