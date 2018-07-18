QandA_System
===

This is the server side of a Q&A system with social network.  
This server is developed on Django 2.0 and uses MySQL as database.  

Environment: Linux 16.04  
Developed Language: Python 3.5  
Django version: 2.0.6  
MySQL version: Ver 14.14 Distrib 5.7.22  
Data encolding: utf8  
Server display language: zh-TW  

### QandA_System/  
Including basical settings such as urls.  
### app/   
An app contains APIs.  

# File Structure
<pre>
QandA_System/   
├── app
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── models.py
│   ├── question
│   |   ├── serializer.py
│   |   └── views.py
│   ├── tests.py
│   ├── urls.py
│   └── user
│       ├── serializer.py
│       └── views.py
├── manage.py
├── QandA_System
│     ├── __init__.py
│     ├── settings.py
│     ├── urls.py
│     └── wsgi.py
├── README.md
</pre>

# Expected API  
User
+ Register
+ Login
+ Set User Profile
+ Get User Expertise
+ Search Expertise
+ Get User list and Search User
+ Add Friends to Users
+ Delete Friends of Users

Question
- Post Question
- Modify Question
- Get Question
- Delete Question
- Get All Questions
- Get and Search Questions

Reply
* Post Reply
* Modify Reply
* Get Reply
* Delete Reply
* Get All Replys for a question
  
## User
### Register  
POST **/api/user/register/**  
I/O format: json  
Input:  

    {
        "username": String,
        "email": EmailString,
        "password": String
    }
    
Input details:  
  **username** -- (require)  
  **email** -- (require)  
  **password** -- (require)  
Response:  

    {
        "msg": String
    }
Response details:  
**msg** --  
+ 'Success': If successful.
+ 'Error': If failed.

**"ErrorMsg"** (When `"msg": "Error"`) --
String, reasons why It is faild.

---
### Login  
POST **/api/user/login/**  
I/O format: json  
Input:  
    
    {
        "username": String,
        "email": EmailString,
        "password": String
    }
Input details:  
  **username** -- (require)  
  **password** -- (require)  
Response:  
    
    {
        "msg": String,
        "key": String
    }
Response details:  
**msg** --  
+ 'Success': If successful.
+ 'Error': If failed.

**"ErrorMsg"** (When `"msg": "Error"`) --
String, reasons why It is faild.

**key** --  
    Use as logined authority  

---
### Get User Profile  
POST **/api/user/profile/**  
I/O format: json  
Input:  
    
    {
        "key": String
    }
Input details:  
**key** -- (require)  
    To authrize the user has logined or not  
Response:  
    
    {
        "msg": String,
        "username": String,
        "expertise": StringList,
        "email": EmailString,
        "friends": StringList
    }
Response details:  
**expertises** --  
    String list with non-fixed length, ex. ["expertise1", "expertise2"]  
**friends** -- (require)  
    String list with non-fixed length, ex. ["foobar2", "foobar12"]. Every String Should be an existing username.  

---
### Set User Expertise  
POST **/api/user/profile/update/**  
I/O format: json  
Input:  
    
    {
        "key": String,
        "expertises": StringList
    {
Input details:  
**key** -- (require)  
**expertise** -- (require)  
    String list with non-fixed length, ex. ["expertise1", "expertise2"]  
Response:  

    {
        "msg": String
    }

---
### Search Expertise
GET **/api/expertises/search?key=<expertise>**
Url examples:
+ **/api/expertises/search**
    + Get all expertises, and users and questions related to them 
+ **/api/expertises/search?key=<expertise>**
    + Get all expertises containing <expertise>, and users and questions related to these expertises. 
    
Input details:   
**<expertise>** -- String  
Response format: json  
Response:  
    
    [
        {
            "expertise": String,
            "questions": [
                {
                    "question_id": Integer,
                    "user_id": Integer,
                    "username": String,
                    "title": String
                },
                :
                :
            ],
            "users": [
                {
                    "user_id": Integer,
                    "username": String
                },
                :
                :
            ]
        }
        :
        :
    ]
---
### Add Friends to Users
POST **/api/user/friend/add/**  
I/O format: json  
Input:  
    
    {
        "key": String,
        "friends": StringList
    {
Input details:  
**key** -- (require)  
**friends** -- (require)  
    String list with non-fixed length, ex. ["foobar2", "foobar12"]. Every String Should be an existing username.  
Response:  

    {
        "msg": String
    }

---
### Delete Friends of Users
POST **/api/user/friend/delete/**  
I/O format: json  
Input:  
    
    {
        "key": String,
        "friends": StringList
    {
Input details:  
**key** -- (require)  
**friends** -- (require)  
    String list with non-fixed length, ex. ["foobar2", "foobar12"]. Every String Should be an existing username.  
Response:  

    {
        "msg": String
    }

---
### Get User list and Search User
POST **/api/users/list/?username=<username>/**  
Url examples:
+ GET **/api/users/list/** 
    + Get all users.
+ GET **/api/users/list/?username=<username>** 
    + Get all the users whose names containes <username>

Input details:   
**<username>** -- String  
Response format: json  
Response:  

    [
        {
            "username": String,
            "id": Integer
        },
        :
        :
    ]
    
---
## Question
### Post Question
POST **/api/question/post/**  
I/O format: json  
Input:  
    
    {
        "key": String, 
        "title": String, 
        "content": String, "hashtags": ["tag1", "tag2"]}
    }

---
### Modify Question
POST **/api/question/edit/**  
I/O format: json  
Input:  

    {
        "key": String, 
        "question_id": Integer, 
        "title": String, 
        "content": String, 
        "expertises": StringList
    }
Input details:  
**key** -- (require)  
**question_id** -- (require)  
**title** -- (**Not** require)  
**content** -- (**Not** require)  
**expertise** -- (**Not** require)  
    String list with non-fixed length, ex. ["expertise1", "expertise2", "question3"]  

---
### Delete Question
POST **/api/question/delete/**  
I/O format: json  
Input:  

    {
        "key": String, 
        "question_id": Integer
    }
Input details:  
**key** -- (require)  
**question_id** -- (require)  

---
### Get Question
GET **/api/question/<question_id>/**  
Response format: json  
Response:  

    {
        "msg": String,
        "username": String
        "title": String,
        "content": String,
        "modify_date": DateString,
        "expertises": Stringlist,
        "create_date": DateString,
        "reply_number": Integer,
    }
**expertises** --  
    Integer list with non-fixed length.   
**modify_date** --
    DateString. Ex. "2018-07-09T02:43:25.360641+08:00"
**create_date** --
    DateString. Ex. "2018-07-09T02:43:25.360641+08:00"

---
### Get All Questions 
GET **/api/question/0/**  
Response format: json  
Response:  

    {
        msg": String,
        "question_ids": IntegerList
    }
**question_ids** --  
    Integer list with non-fixed length.   

### Get and Search Questions
GET **/api/questions/?uid=<user_id>&qid=<question_id>/**
Url examples:
+ GET **/api/questions/**
    + Get all questions.
+ GET **/api/question/?uid=<user_id>/**
    + Get all the questions of the user whose id is <user_id>
+ GET **/api/question/?qid=<question_id>/**
    + Get the question whose id is <question_id>
+ GET **/api/questions/?uid=<user_id>&qid=<question_id>/**
    + Get the question whose question_id is <question_id> (but the user id of the question should equal to <user_id>)

Input details:   
**<user_id>** -- Integer  
**<question_id>** -- Integer  

Response format: json  
Response:  

    [
        {
            "user_id": Integer,
            "username": String,
            "question_id": Integer,
            "title": String,
            "content": String,
            "create_date": DateString,
            "mod_date": DateString,
            "reply_number": Integer,
            "expertises": StringList
            
        },
        :
        :
    ]  
**create_date** --  
    DateString. Ex. "2018-07-09T02:43:25.360641+08:00"  
**modify_date** --  
    DateString. Ex. "2018-07-09T02:43:25.360641+08:00"  
**expertise** --   
    String list with non-fixed length, ex. ["test", "C++"]  

---
## Reply
### Post Reply

---
### Modify Reply

---
### Delete Reply

---
### Get Reply

---
### Get All Replys for a question
                                          
