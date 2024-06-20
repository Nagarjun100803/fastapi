from typing import List 
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import Depends, APIRouter, HTTPException, status
import models, schemas, oauth2, database



post_router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


# @post_router.get("/", response_model = List[schemas.PostOut])
@post_router.get("/", response_model = List[schemas.PostGet])
async def get_all_posts(db : Session = Depends(database.get_db), 
                        user_id : int = Depends(oauth2.get_current_user),
                        limit : int = 10, skip : int = 0, search : str = "") : 

    # all_posts = db.query(models.Posts).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()

    all_posts = db.query(models.Posts, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Vote.post_id == models.Posts.id,
        isouter=True).group_by(models.Posts.id).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()
    
    # print(all_posts)
    # print(all_posts)
    # all_post is a models.Post object but FastAPI can serialize that into JSON
    
    return all_posts


@post_router.post("/", status_code = status.HTTP_201_CREATED)
async def create_post(post : schemas.Post, db : Session = Depends(database.get_db),
                      owner : schemas.TokenData = Depends(oauth2.get_current_user)):

    # new_post = models.Posts(
    #                 title=post.title, content=post.content, 
    #                 published= post.published)
    #The below and above statements are same

    new_post = models.Posts(owner_id = owner.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post



@post_router.get("/{post_id}", response_model = schemas.PostGet)
async def get_particular_post(post_id : int, db : Session = Depends(database.get_db),
                              owner : schemas.TokenData = Depends(oauth2.get_current_user)) : 

    # post =  db.query(models.Posts).filter(models.Posts.id == post_id).first()

    post = db.query(models.Posts, func.count(models.Posts.id).label('votes')).filter(models.Posts.id == post_id).join(models.Vote, models.Vote.post_id == models.Posts.id, isouter=True).group_by(models.Posts.id).first()
    
    # print(post)

    if not post :
        raise HTTPException(
            status_code=404, detail= f"No post found with id : {post_id} "
        )
    return post



@post_router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id : int, db : Session = Depends(database.get_db),
                      owner : schemas.TokenData = Depends(oauth2.get_current_user)) : 
     
    post_query = db.query(models.Posts).filter(models.Posts.id == post_id)
    post = post_query.first()

    if not post :
        raise HTTPException(
            status_code=404, detail= f"No post found with id : {post_id} "
        )
    
    if post.owner_id != owner.id :
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "You can't perform the requested action"
        )
    
    post_query.delete(synchronize_session=False)
    db.commit()

     



@post_router.put("/")
async def update_post(post_id : int, update_post : schemas.Post, db : Session = Depends(database.get_db),
                      owner : schemas.TokenData = Depends(oauth2.get_current_user)) : 

    post_query = db.query(models.Posts).filter(models.Posts.id == post_id)

    post = post_query.first()

    if not post : 
        raise HTTPException(
            status_code=404, detail= f"No post found with id : {post_id} "
        )      
    
    if post.owner_id != owner.id :
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "You can't perform the requested action"
        )
    
    post_query.update(update_post.dict())

    db.commit()

    return "Updated successfully"
