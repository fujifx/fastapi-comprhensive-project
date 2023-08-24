from random import randrange
from typing import Optional
from fastapi import Body, FastAPI
from pydantic import UUID4, BaseModel

app = FastAPI()

# Comment 1:    FastAPI works Top to Down when searching and maching Paths (Routes). 
#               So the order of the PATHS really matter and always ensure structure your Paths in the API to avoid any Path conflicts.

    # id: UUID4 = UUID4()
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [
    {"title":"Title of post 1", "content":"Content of post 1", "id":1},
    {"title":"Title of post 2", "content":"Content of post 2", "id":2}
]

def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
async def get_posts():
    return {"data": my_posts}

@app.post("/createposts")
async def create_posts(post: Post):
    post_dict = post.model_dump()   # converts Pydantic model into Python Dictionary. .dict is deprecated
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

# If the get_latest_post() moved below get_posts() there would be error, since FastAPI attempting to match the 1 st path it finds. Refer Comment 1
@app.get("/posts/latest")
async def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"data": post}

@app.get("/posts/{id}")
async def get_post(id: int):
    # in the above specifying the parameter type int would enable FastAPI to enforce parameter type as int
    post = find_post(id)
    return{"data": post}
