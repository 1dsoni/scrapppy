from models import ProductScraperConfig
from scrappers.DentalStallProductsScrapper import DentalStallProductsScrapper
from scrappers.constants import ScrapperType


class ScrapperHelper:

    def __init__(self, project):
        self.project = project

        self.scrapper = None
        if self.project == ScrapperType.dental_stall:
            self.scrapper = DentalStallProductsScrapper()

        if not self.scrapper:
            raise NotImplementedError(f"scraper for {self.project} is not implemented")

    async def execute_scraper(self, scraper_config: ProductScraperConfig):
        await self.scrapper.scrape(scraper_config)

    async def get_scrapped_data(self):
        return await self.scrapper.get_scrapped_data()
