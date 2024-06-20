from typing import Literal
from pydantic import BaseModel, EmailStr



class Post(BaseModel):
    title : str 
    content : str 
    published : bool = False

class UserOut(BaseModel):
    username : str 
    email : str

    class Config : 
        orm_mode = True



class Vote(BaseModel):
    post_id : int 
    dir : Literal[1, 0]


class PostOut(BaseModel) : 
    id : int
    title : str 
    content : str 
    owner_id : int

    owner : UserOut


    class Config :
        orm_mode = True

class PostGet(BaseModel) :
    Posts : PostOut
    votes : int

    class Config :
        orm_mode = True


class UserIn(BaseModel) : 
    username : str 
    email : EmailStr
    password : str 





class UserLogin(BaseModel):
    email : EmailStr
    password : str



class Token(BaseModel) :
    access_token : str 
    token_type : str 



class TokenData(BaseModel) :
    id : int | None = None


