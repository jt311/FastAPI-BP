from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(pwd: str):
    return pwd_context.hash(pwd)

def verify(pwd: str, hashedPwd: str):
    return pwd_context.verify(pwd, hashedPwd)