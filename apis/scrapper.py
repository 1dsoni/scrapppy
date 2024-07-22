import logging

from fastapi import APIRouter, Depends

from auth import StaticJWTBearer
from models import ProductScraperConfig
from scrappers.ScraperHelper import ScrapperHelper

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/v1")


@router.post("/scrape/{project}/execute", dependencies=[Depends(StaticJWTBearer())])
async def scrape_project_execute(project: str, scraper_config: ProductScraperConfig):
    scraper_helper = ScrapperHelper(project=project)
    await scraper_helper.execute_scraper(scraper_config=scraper_config)
    return {"ok": True}


@router.get("/scrape/{project}/data", dependencies=[Depends(StaticJWTBearer())])
async def get_scraped_project_data(project: str):
    scraper_helper = ScrapperHelper(project=project)
    return {"data": await scraper_helper.get_scrapped_data()}
