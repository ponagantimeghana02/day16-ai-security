from jose import jwt
from datetime import datetime,timedelta
from config import *

users={

"alice":
{
"password":"alice123",
"role":"HR"
},

"bob":
{
"password":"bob123",
"role":"Payroll"
},

"admin":
{
"password":"admin123",
"role":"Admin"
}

}

def authenticate(username,password):

    if username not in users:
        return None

    if users[username]["password"]!=password:
        return None

    return users[username]


def create_token(username):

    expire=datetime.utcnow()+timedelta(minutes=30)

    payload={
        "sub":username,
        "exp":expire
    }

    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)


def verify_token(token):

    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )