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
    scraper_helper = ScrapperHelper(project=project)
    await scraper_helper.execute_scraper()
    return {"ok": True}


@router.get("/scrape/{project}/data")
async def get_scraped_project_data(project: str):
    scraper_helper = ScrapperHelper(project=project)
    return {"data": await scraper_helper.get_scrapped_data()}
