from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
import schemas
from fastapi.security.oauth2 import OAuth2PasswordBearer
from config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(payload : dict):

    to_enode = payload.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_enode.update({"exp" : expire})

    encoded_jwt = jwt.encode(to_enode, SECRET_KEY, ALGORITHM)

    return encoded_jwt



def get_current_user(token : str = Depends(oauth2_scheme)) :

    credential_exception =  HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Your session expired need to login"
        )
    # decode the token 
    try :
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id : int =  payload.get("user_id")
        # print(payload)

        if not id :
            raise  credential_exception

    except JWTError as e :
        credential_exception

    return schemas.TokenData(id = id)









# def verify_access_token(token : str, credential_exception : HTTPException) :

#     try :
        
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         id : int = payload.get('user_id')

#         if id is None :
#             raise credential_exception

#         token_data = schemas.TokenData(id=id)

#     except JWTError :
#         raise credential_exception

    
#     return token_data
    

# def get_current_user(token : str = Depends(oauth2_scheme)):

#     credential_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail= "Your session expired, need to login"
#     )

#     return verify_access_token(token, credential_exception)


