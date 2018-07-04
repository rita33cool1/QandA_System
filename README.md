QandA_System
===

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
│   ├── serializer.py
│   ├── tests.py
│   ├── urls.py
│   ├── user
│   │   ├── serializer.py
│   │   └── views.py
│   └── views.py
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
+ Get User Profile

Question
- Post Question
- Modify Question
- Get Question
- Delete Question
- Get All Questions

Reply
* Post Reply
* Modify Reply
* Get Reply
* Delete Reply
* Get All Replys for a question
  
## User
### Register  
Url: POST http://localhost:8000/api/user/register/  
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
**message** --  
+ "Success": If register successfully.
+ Error message

---
### Login  
Url: POST http://localhost:8000/api/user/login/  
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
**message** --  
+ "Success": If login successfully.
+ Error message

**key** --  
    Use as logined authority  

---
## Get Profile  
Url: POST http://localhost:8000/api/user/profile/  
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
        "email": EmailString
    }
Response details:  
**expertises** --  
    String list with non-fixed length, ex. ["expertise1", "expertise2"]  

---
### Set Profile
Url: POST http://localhost:8000/api/user/profile/update/  
I/O format: json  
Input:  
    
    {
        "key": String,
        "expertises": StringList
    {
Input details:  
**key** -- (require)  
**expertise** -- (require)  
    String list with non-fixed length, ex. ["expertise1", "expertise2", "question3]  
Response:  

    {
        "msg": <message>
    }
    
---
## Question
### Post Question
Url: POST http://localhost:8000/api/question/post/  

---
### Modify Question
Url: POST http://localhost:8000/api/question/edit/  

---
### Delete Question
Url: POST http://localhost:8000/api/question/delete/  

---
### Get Question
Url: GET http://localhost:8000/api/question/<question_id>/  
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

---
### Get All Questions
Url: GET http://localhost:8000/api/question/0/  
Response format: json  
Response:  

    {
        msg": String,
        "question_ids": IntegerList
    }
**question_ids** --  
    Integer list with non-fixed length.   

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
                                          
