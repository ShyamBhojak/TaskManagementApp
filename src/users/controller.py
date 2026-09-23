from fastapi import HTTPException, status, Request
from src.users.dtos import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from src.users.models import User
from pwdlib import PasswordHash
import jwt
from src.utils.settings import settings
from datetime import datetime, timedelta
from jwt.exceptions import InvalidTokenError

password_hash = PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def register(data: UserSchema, db:Session):
    #1. Username Validation
    is_username = db.query(User).filter(User.username == data.username).first()
    if is_username:
        raise HTTPException(400, detail=f"Username {data.username} already exists...")

    #2. Email Validation
    is_email = db.query(User).filter(User.email == data.email).first()
    if is_email:
        raise HTTPException(400, f"Email {data.email} already exists...")

    hash_password = get_password_hash(data.password)

    user = User(
        name = data.name,
        username = data.username,
        password = hash_password,
        email = data.email
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def login(credentials: LoginSchema, db:Session):
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Username...")

    if not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Password...")

    #EXPIRY TIME
    exp_time = datetime.now() + timedelta(seconds=settings.EXP_TIME)
    print(exp_time)

    #GENERATE TOKEN
    token = jwt.encode({"_id":user.id, "username":user.username,"exp":exp_time.timestamp()},settings.SECRET_KEY, settings.ALGORITHM)

    return {"token":token}

#WHEN USER CALLS AN API, TOKEN WILL BE SENT
#TOKENS CAN BE SENT USING HEADERS

def is_authenticated(request:Request, db:Session):
    try:
        # print(request.headers)
        token = request.headers.get("authorization")
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized Token")
        
        token = token.split(" ")[-1]

        data = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        # print(data)
        user_id = data["_id"]
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized Access!")
        
        return user
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token Expired")
