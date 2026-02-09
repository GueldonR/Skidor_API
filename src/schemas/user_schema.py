from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from src.domain.enums import UserEnum


class User(BaseModel):
    user_id: UUID = Field(description="The unique identifier of the user")
    username: str = Field(description="The username of the user")
    password_hash: str = Field(description="The password hash of the user")
    role: UserEnum = Field(description="The role of the user")
    created: datetime = Field(
        description="The date and time the user was created")
    last_updated: datetime = Field(
        description="The date and time the user was last updated")

    class Config:
        from_attributes = True  # To not require dict input and allow ORM models
