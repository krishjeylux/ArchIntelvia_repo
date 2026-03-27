from pydantic import BaseModel

class AnalyzeRequest(BaseModel):
    params: dict

class AnalyzeResponse(BaseModel):
    status: str
    message: str
