from pydantic import BaseModel

class StartSessionResponse(BaseModel):
    session_id: str
