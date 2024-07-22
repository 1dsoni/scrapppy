from fastapi import APIRouter

router = APIRouter()


@router.get("/ht")
async def ht_api():
    return {
        "ok": True
    }
