from fastapi import APIRouter
from .schemas import AnalyzeRequest, AnalyzeResponse

router = APIRouter()

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    return {"status": "success", "message": "Analysis started"}

@router.post("/decide")
async def decide():
    return {"status": "success"}

@router.post("/generate")
async def generate():
    return {"status": "success"}
