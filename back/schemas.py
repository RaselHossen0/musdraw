from pydantic import BaseModel

class UserData(BaseModel):
    user_name: str