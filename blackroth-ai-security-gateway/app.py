from fastapi import FastAPI
from pydantic import BaseModel

from auth import authenticate

from auth import create_token

from auth import verify_token

from prompt_guard import validate

from output_guard import validate as output_validate

from audit_logger import log

from risk_score import calculate

app=FastAPI(title="BlackRoth AI Security Gateway")


class Login(BaseModel):

    username:str

    password:str


class Chat(BaseModel):

    token:str

    prompt:str


@app.post("/login")

def login(data:Login):

    user=authenticate(

        data.username,

        data.password

    )

    if not user:

        return {"error":"Invalid Login"}

    token=create_token(data.username)

    return{

    "token":token,

    "role":user["role"]

    }


@app.post("/chat")

def chat(data:Chat):

    payload=verify_token(data.token)

    username=payload["sub"]

    validate(data.prompt)

    risk=calculate(data.prompt)

    response="AI Response : "+data.prompt

    response=output_validate(response)

    log(

        username,

        data.prompt,

        response,

        risk

    )

    return{

    "response":response,

    "risk":risk

    }