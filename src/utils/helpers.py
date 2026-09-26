from fastapi import status, Request, HTTPException, Depends
from src.utils.settings import settings
from src.utils.db import get_db
from src.users.models import User
from sqlalchemy.orm import Session
import jwt
from jwt.exceptions import InvalidTokenError


def is_authenticated(request:Request, db:Session = Depends(get_db)):
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