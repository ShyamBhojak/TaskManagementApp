from fastapi import HTTPException
from src.users.dtos import UserSchema
from sqlalchemy.orm import Session
from src.users.models import User
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)

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
