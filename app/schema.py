from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# pydantic model for input validation. 
class Post(BaseModel):
    title: str
    content: str
    published: bool = True


