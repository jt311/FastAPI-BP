from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Union
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends
from app.schemas import TokenData
from app.database import get_db
from sqlalchemy.orm import Session
from app import models, config

SECRET_KEY = config.settings.SECRET_KEY
ALGORITHM = config.settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = config.settings.ACCESS_TOKEN_EXPIRE_MINUTES
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")

def createAccessToken(data: dict, expireDelta: Union[timedelta, None] = None):
    dataCopyToEncode = data.copy()
    expire = datetime.utcnow() + expireDelta if expireDelta else datetime.utcnow() + timedelta(minutes=15)
    dataCopyToEncode.update({"exp": expire})
    encodedJWT = jwt.encode(dataCopyToEncode, SECRET_KEY, ALGORITHM)
    return encodedJWT

def getCurrentUser(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentialsException = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers = {
            "WWW-Authenticate": "Bearer"})

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        id: str = payload.get("user_id")
        if not id:
            raise credentialsException
        tokenData = TokenData(id = id)
        currUser = db.query(models.User).filter(models.User.id == tokenData.id).first()
    except JWTError as e:
        print(f"Error: {e}")
        raise credentialsException

    return currUser.id