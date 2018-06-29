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
### users/   
An app contains APIs related to user data.  
### v1/  
An app contains APIs related to other things.  
    
## Expected API  
+ Register
+ Login
+ Set User Profile
+ Get User Profile  
  
+ Post Question
+ Modify Question
+ Get Question
+ Delete Question
+ Get User Question
  
+ Post Reply
+ Modify Reply
+ Get Reply
+ Delete Reply
+ Get User Reply
  
### User
#### Register  
Url: POST http://localhost:8000/accounts/api/users/register/  
I/O format: json  
Input: {  
        "username": <username>,  
        "email": <email>,  
        "password": <password>  
        }  
Input details:  
  username: (require)  
  email: (require)  
  password: (require)  

Response: {  
        "msg": <message>  
        }  
Response details:
<<<<<<< HEAD
<message>  
+ "Success": If register successfully.
+ Error message

argon2$argon2i$v=19$m=512,t=2,p=2$M3ZLNGhRWXB5QjBT$ABwJmSX684adV2ObxHbjIQ
=======
  <message>  
    + "Success": If register successfully.
    + Error message
>>>>>>> db9a696b6e78fc7689336a88bd62cb8e9035b9e5

