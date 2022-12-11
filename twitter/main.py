# Python
import json
from uuid import UUID
from datetime import date, datetime
from typing import Optional, List

#  Pydantic
from pydantic import BaseModel
from pydantic.networks import EmailStr
from pydantic import Field

#  FastAPI
from fastapi import FastAPI, status, HTTPException
from fastapi import Body, Form, Path

import os
app = FastAPI()

# Models

class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)

class UserLogin(UserBase):
    password: str = Field(
        ..., 
        min_length=8,
        max_length=64
    )

class User(UserBase):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    birth_date: Optional[date] = Field(default=None)

class UserRegister(User):
    password: str = Field(
        ..., 
        min_length=8,
        max_length=64
    )

class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(
        ..., 
        min_length=1, 
        max_length=256
    )
    created_at: datetime = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None)
    by: User = Field(...)

class LoginOut(BaseModel): 
    email: EmailStr = Field(...)
    message: str = Field(default="Login Successfully!")

"""# Auxiliar funcion 

## funcion reed
def read_data(file):
    with open("{}.json".format(file), "r+", encoding="utf-8") as f: 
        return json.loads(f.read())

## funcion write
def read_data(file, results):
    with open("{}.json".format(file), "r+", encoding="utf-8") as f: 
        f.seek(0)
        f.write(json.dumps(results))"""

    
# Path Operations



## Users

### Register a user
@app.post(
    path="/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a User",
    tags=["Users"]
    )
def signup(user: UserRegister = Body(...)): 
    """
    Signup
    This path operation register a user in the app
    Parameters: 
        - Request body parameter
            - user: UserRegister
    
    Returns a json with the basic user information: 
        - user_id: UUID
        - email: Emailstr
        - first_name: str
        - last_name: str
        - birth_date: datetime
    """
    script_dir = os.path.dirname(__file__)
    rel_path = "users.json"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r+", encoding="utf-8") as f: 
        results = json.loads(f.read())
        user_dict = user.dict()
        user_dict["user_id"] = str(user_dict["user_id"])
        user_dict["birth_date"] = str(user_dict["birth_date"])
        results.append(user_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return user

### Login a user
@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    summary="Login a User",
    tags=["Users"]
    )
def Login(email: EmailStr  = Form(...), password: str = Form(...)):
    """
    Login

    This path operation login a Person in the app

    Parameters:
    - Request body parameters:
        - email: EmailStr
        - password: str

    Returns a LoginOut model with username and message
    """
    script_dir = os.path.dirname(__file__)
    rel_path = "users.json"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r+", encoding="utf-8") as f: 
        datos = json.loads(f.read())
        for user in datos:
            if email == user['email'] and password == user['password']:
                return LoginOut(email=email)
            else:
                return LoginOut(email=email, message="Login Unsuccessfully!")

### Show all users
@app.get(
    path="/user",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all users",
    tags=["Users"]
    )
def show_all_users():
    """
    This path operation shows all users in the app

    Parametes:
        -

    Return a json list whit all users in the app, with the following keys:
        - user_id: UUID
        - email: Emailstr
        - first_name: str
        - last_name: str
        - birth_date: datetime
    """
    script_dir = os.path.dirname(__file__)
    rel_path = "users.json"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results

### Show a user
@app.get(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a User",
    tags=["Users"]
    )
def show_a_user(user_id: UUID = Path(
    ...,
    title="User ID",
    description="This is the user ID",
    example="3fa85f64-5717-4562-b3fc-2c963f66afa2"
    )):
    """
    Show a User

    This path operation show if a person exist in the app

    Parameters:
        - user_id: UUID

    Returns a json with user data:
        - user_id: UUID
        - email: Emailstr
        - first_name: str
        - last_name: str
        - birth_date: datetime
    """
    script_dir = os.path.dirname(__file__)
    rel_path = "users.json"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r+", encoding="utf-8") as f: 
        results = json.loads(f.read())
        id = str(user_id)
    for data in results:
        if data["user_id"] == id:
            return data
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"¡This user_id doesn't exist!"
        )

### Delete a user
@app.delete(
    path="/users/{user_id}/delete",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a User",
    tags=["Users"]
    )
def delete_a_user(
    user_id: UUID = Path(
        ...,
        title="User ID",
        description="This is the user ID",
        example="3fa85f64-5717-4562-b3fc-2c963f66afa1"
    )):
    """
    Delete a User

    This path operation delete a user in the app

    Parameters:
        - user_id: UUID

    Returns a json with deleted user data:
        - user_id: UUID
        - email: Emailstr
        - first_name: str
        - last_name: str
        - birth_date: datetime
    """
    script_dir = os.path.dirname(__file__)
    rel_path = "users.json"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r+", encoding="utf-8") as f: 
        results = json.loads(f.read())
        id = str(user_id)
    for data in results:
        if data["user_id"] == id:
            results.remove(data)
            with open(abs_file_path, "w", encoding="utf-8") as f:
                f.seek(0)
                f.write(json.dumps(results))
            return data
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="¡This user_id doesn't exist!"
        )

### Update a user
@app.put(
    path="/users/{user_id}/update",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a User",
    tags=["Users"]
    )
def update_a_user(
        user_id: UUID = Path(
            ...,
            title="User ID",
            description="This is the user ID",
            example="3fa85f64-5717-4562-b3fc-2c963f66afa3"
        ),
        user: UserRegister = Body(...)
    ):
    """
    Update User

    This path operation update a user information in the app and save in the database

    Parameters:
    - user_id: UUID
    - Request body parameter:
        - **user: User** -> A user model with user_id, email, first name, last name, birth date and password
    
    Returns a user model with user_id, email, first_name, last_name and birth_date
    """
    user_id = str(user_id)
    user_dict = user.dict()
    user_dict["user_id"] = str(user_dict["user_id"])
    user_dict["birth_date"] = str(user_dict["birth_date"])
    script_dir = os.path.dirname(__file__)
    rel_path = "users.json"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r+", encoding="utf-8") as f: 
        results = json.loads(f.read())
    for user in results:
        if user["user_id"] == user_id:
            results[results.index(user)] = user_dict
            with open(abs_file_path, "w", encoding="utf-8") as f:
                f.seek(0)
                f.write(json.dumps(results))
            return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="¡This user_id doesn't exist!"
        )


## Tweets

### Show all tweers
@app.get(
    path="/",
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Show all tweets",
    tags=["Tweets"]
    )
def home():
    """
    This path operation shows all tweets in the app

    Parametes:
        -

    Return a json list whit all tweets in the app, with the following keys:
        - tweet_id: UUID  
        - content: str    
        - created_at: datetime
        - updated_at: Optional[datetime]
        - by: User
    """
    script_dir = os.path.dirname(__file__)
    rel_path = "tweets.json"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results

### Post a tweers
@app.post(
    path="/post",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a tweet",
    tags=["Tweets"]
    )
def post(tweet: Tweet = Body(...)): 
    """
    Post a Tweet

    This path operation post a tweet in the app

    Parameters: 
        - Request body parameter
            - tweet: Tweet
    
    Returns a json with the basic tweet information: 
        - tweet_id: UUID  
        - content: str    
        - created_at: datetime
        - updated_at: Optional[datetime]
        - by: User
    """
    script_dir = os.path.dirname(__file__)
    rel_path = "tweets.json"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r+", encoding="utf-8") as f: 
        results = json.loads(f.read())
        tweet_dict = tweet.dict()
        tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"])
        tweet_dict["created_at"] = str(tweet_dict["created_at"])
        tweet_dict["updated_at"] = str(tweet_dict["updated_at"])
        tweet_dict["by"]["user_id"] = str(tweet_dict["by"]["user_id"])
        tweet_dict["by"]["birth_date"] = str(tweet_dict["by"]["birth_date"])

        results.append(tweet_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return tweet

### Show a tweers
@app.get(
    path="/tweets/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Show a tweet",
    tags=["Tweets"]
    )
def show_a_tweet(tweet_id: UUID = Path(
    ...,
    title="Tweet ID",
    description="This is the tweet ID",
    example="3fa85f64-5717-4562-b3fc-2c963f66afa6"
    )):
    """
    Show a Tweet

    This path operation show if a tweet exist in the app

    Parameters:
        - tweet_id: UUID

    Returns a json with tweet data:
        - tweet_id: UUID
        - content: str
        - created_at: datetime
        - updated_at: Optional[datetime]
        - by: User
    """
    script_dir = os.path.dirname(__file__)
    rel_path = "tweets.json"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r+", encoding="utf-8") as f: 
        results = json.loads(f.read())
        id = str(tweet_id)
    for data in results:
        if data["tweet_id"] == id:
            return data
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"¡This tweet_id doesn't exist!"
        )

### Delete a tweers
@app.delete(
    path="/tweets/{tweet_id}/delete",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=["Tweets"]
    )
def delete_a_tweet(
    tweet_id: UUID = Path(
        ...,
        title="Tweet ID",
        description="This is the tweet ID",
        example="3fa85f64-5717-4562-b3fc-2c963f66afa2"
    )):
    """
    Delete a Tweet

    This path operation delete a tweet in the app

    Parameters:
        - tweet_id: UUID

    Returns a json with deleted tweet data:
        - tweet_id: UUID
        - content: str
        - created_at: datetime
        - updated_at: Optional[datetime]
        - by: User
    """
    script_dir = os.path.dirname(__file__)
    rel_path = "tweets.json"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r+", encoding="utf-8") as f: 
        results = json.loads(f.read())
        id = str(tweet_id)
    for data in results:
        if data["tweet_id"] == id:
            results.remove(data)
            with open(abs_file_path, "w", encoding="utf-8") as f:
                f.seek(0)
                f.write(json.dumps(results))
            return data
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="¡This tweet_id doesn't exist!"
        )

### Update a tweers
@app.put(
    path="/tweets/{tweet_id}/update",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Update a tweet",
    tags=["Tweets"]
    )
def upsate_a_tweet(
        tweet_id: UUID = Path(
            ...,
            title="Tweet ID",
            description="This is the tweet ID",
            example="3fa85f64-5717-4562-b3fc-2c963f66afa8"
        ),
         content: str = Form(
        ..., 
        min_length=1,
        max_length=256,
        title="Tweet content",
        description="This is the content of the tweet",
        )
    ):
    """
    Update Tweet

    This path operation update a tweet information in the app and save in the database

    Parameters:
    - tweet_id: UUID
    - contet:str
    
    Returns a json with:
        - tweet_id: UUID
        - content: str 
        - created_at: datetime 
        - updated_at: datetime
        - by: user: User
    """
    tweet_id = str(tweet_id)
    # tweet_dict = tweet.dict()
    # tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"])
    # tweet_dict["birth_date"] = str(tweet_dict["birth_date"])
    script_dir = os.path.dirname(__file__)
    rel_path = "tweets.json"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r+", encoding="utf-8") as f: 
        results = json.loads(f.read())
    for tweet in results:
        if tweet["tweet_id"] == tweet_id:
            tweet['content'] = content
            tweet['updated_at'] = str(datetime.now())
            print(tweet)
            with open(abs_file_path, "w", encoding="utf-8") as f:
                f.seek(0)
                f.write(json.dumps(results))
            return tweet
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="¡This tweet_id doesn't exist!"
        )