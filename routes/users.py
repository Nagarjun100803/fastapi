from typing import List
from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
import models, database, schemas, utils




users_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@users_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user : schemas.UserIn, db : Session = Depends(database.get_db)) :

    user_email = db.query(models.Users).filter(models.Users.email == user.email).first()
    
    if user_email :
        raise HTTPException(
            status_code = status.HTTP_406_NOT_ACCEPTABLE,
            detail = "Email already exist, try using different email"
        )
    
    new_user = models.Users(**user.dict())
    new_user.password = utils.hash_password(new_user.password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



@users_router.get("/{user_id}", response_model = schemas.UserOut)
async def get_particular_user(user_id : int, db : Session = Depends(database.get_db)) :

    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if not user :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f"User with id : {user_id} is not found"
        )
    return user



@users_router.get("/", response_model = List[schemas.UserOut])
async def get_all_users(db : Session = Depends(database.get_db)):
    
    users = db.query(models.Users).all()

    return users



