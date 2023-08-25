from random import randrange
from typing import Optional
from fastapi import Body, FastAPI, HTTPException, Response, status
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
        
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
async def get_posts():
    return {"data": my_posts}

@app.post("/createposts", status_code=status.HTTP_201_CREATED)
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
async def get_post(id: int, response: Response):
    # in the above specifying the parameter type int would enable FastAPI to enforce parameter type as int
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return{"data": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    # Deleting a post
    # find the index in the array that has required ID
    post_index = find_index_post(id)

    if post_index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    my_posts.pop(post_index)

    # When the status code is 204, you are not supposed send back any data, 
    # if done so you'd end up with the error 'Too much data for declated Content-Length'
    # return{'message': f"Post with id {id} successfully deleted"}

    # So instead, return as below
    return Response(status_code=status.HTTP_204_NO_CONTENT)
 

@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    post_index = find_index_post(id)

    if post_index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    post_dict = post.model_dump()
    post_dict['id'] = id
    my_posts[post_index] = post_dict
    return {"message": post_dict}    