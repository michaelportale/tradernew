from fastapi import APIRouter

router = APIRouter()

@router.post("/fetch/{source}")
async def fetch_data(source: str):
    # Future: call async fetcher
    return {"message": f"Fetching data from {source}"}