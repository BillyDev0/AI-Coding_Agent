from jose import jwt, JWTError
from datetime import timedelta,datetime,timezone
from dotenv  import load_dotenv
import os

load_dotenv()
SECREATE_KEY=os.getenv("SECREATE_KEY")
ALGORITHM='HS256'

def create_token(username:str):
    payload={
        'username':username,
        'exp':datetime.now(timezone.utc) + timedelta(minutes=30)
    }

    token=jwt.encode(payload,SECREATE_KEY,algorithm=ALGORITHM)
    return token

def verif_token(token):
    try:
        payload=jwt.decode(token,SECREATE_KEY,algorithms=[ALGORITHM])
        return payload['username']
    except JWTError:
        return None