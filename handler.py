
from citydata.in_memory import InMemoryCityDataProvider
from citydata.file_based import FileBasedCityDataProvider
from citydata.scraper import ScraperCityDataProvider
from citydata.cached import CachedCityDataProvider



import json

inMemory = InMemoryCityDataProvider()
fileBased = FileBasedCityDataProvider("./data")
scraper = ScraperCityDataProvider()

cached = CachedCityDataProvider([inMemory, fileBased, scraper])


def handle_get_city(term):
    cityData = cached.getDataForTerm(term)
    return cityData





