import logging

from fastapi import APIRouter, HTTPException

from scrappers.ScraperHelper import ScrapperHelper

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/v1")

API_TOKEN = "your_static_token"


def get_token(token: str):
    if token != API_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")
    return token


@router.post("/scrape/{project}/execute")
async def scrape_project_execute(project: str):
    scraper_helper = ScrapperHelper(project="dental_stall")
    await scraper_helper.execute_scraper()
    return {"ok": True}
