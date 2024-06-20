from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session
import models, schemas, oauth2, database


voting_router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)


@voting_router.post("/")
async def vote(vote : schemas.Vote, db : Session = Depends(database.get_db),
               user : schemas.TokenData = Depends(oauth2.get_current_user)) :

    post_query = db.query(models.Posts).filter(models.Posts.id == vote.post_id)
    # print(post_query)
    
    post = post_query.first()
    # print(post)

    if not post : 
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"No post found with id {vote.post_id}" 
        )
    
    vote_query = db.query(models.Vote).filter(models.Vote.user_id == user.id, models.Vote.post_id == vote.post_id)
    # print(vote_query)

    vote_found = vote_query.first()
    # print(vote_found)

    if vote.dir == 1 :

        if vote_found :

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail  = f"User {user.id} already voted this post"
            )
        
        
        new_vote = models.Vote(user_id = user.id, post_id = vote.post_id)
        db.add(new_vote)
        db.commit()
        
        return {"Message" : "Successfully voted"}
    
    else :

        if not vote_found :
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "No vote found with this post"
            )
        
        vote_query.delete(synchronize_session = False)
        db.commit()

        return {"Message" : "Vote is deleted"}
    



        


