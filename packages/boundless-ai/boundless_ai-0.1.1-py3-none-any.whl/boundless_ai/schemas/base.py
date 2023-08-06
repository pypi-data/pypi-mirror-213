from pydantic import BaseModel, Field
from datetime import datetime


class ChatbotSchema(BaseModel):
    name: str
    prompt: str
    created_at: datetime = Field(default_factory=datetime.now)