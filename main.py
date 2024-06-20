from fastapi import  FastAPI
import models
from database import engine 
from routes import posts, users, auth, vote
from config import settings
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine) # This line will create a table if it doesnt exist



app = FastAPI()

origins = ['*']



app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ['*'],  
    allow_headers = ['*']
)



app.include_router(posts.post_router)
app.include_router(users.users_router)
app.include_router(auth.authentication_router)
app.include_router(vote.voting_router)



# conn = get_db()
# print(conn)


@app.get("/", tags=["Default"])
async def test():
    return {'response' : "HELLO NAGARJUN"}






