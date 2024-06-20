from fastapi import APIRouter, Depends, HTTPException, status
import schemas, models, database, utils, oauth2
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


authentication_router = APIRouter(
    tags=["Authentication"]
)



@authentication_router.post("/login")
def login_user(user_credentials : OAuth2PasswordRequestForm = Depends(), 
               db : Session = Depends(database.get_db)) -> schemas.Token:

    user = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()
    
    if not user :
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"No user found with this email"
        )
    
    if not utils.verify_password(user_credentials.password, user.password) :
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = f"Incorrect Password",
            headers = {"WWW_AUthenticate" : "Bearer"}
        )       
    access_token = oauth2.create_access_token(payload = {'user_id' : user.id})
    # create access token and return it
    return schemas.Token(access_token = access_token, token_type = "bearer")








