from scrappers.DentalStallProductsScrapper import DentalStallProductsScrapper


class ScrapperHelper:

    def __init__(self, project):
        self.project = project

    async def execute_scraper(self):
        scrapper = None
        if self.project == 'dental_stall':
            scrapper = DentalStallProductsScrapper()

        if not scrapper:
            raise NotImplementedError(f"scraper for {self.project} is not implemented")

        await scrapper.scrape()
