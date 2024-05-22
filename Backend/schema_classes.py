from pydantic import BaseModel,Field

class CrawlingConfig(BaseModel):
    query: str = Field(..., description="The main query that user provides from frontend")

class GetDataConfig(BaseModel):
    business_name: str = Field(..., description="The name of the business asked.")

class UserLoginConfig(BaseModel):
    user_name: str = Field(..., description="The user name for login")
    password: str = Field(..., description="The password of that user")

