
from data_provider_interface import CityDataProvider


class InMemoryCityDataProvider(CityDataProvider):
    def __init__(self) -> None:
        self.linkForTerm = {}
        self.dataForLink = {}
        return
    
    def getLinkForTerm(self, term : str) -> str:
        if term in self.linkForTerm:
            return self.linkForTerm[term]
        return None
    
    def getDataForLink(self, link : str) -> dict:
        if link in self.dataForLink:
            return self.dataForLink[link]
        return None
    
    def putLinkForTerm(self, term : str, link : str) -> None:
        self.linkForTerm[term] = link
        return
    
    def putDataForLink(self, link : str, data : str) -> None:
        self.dataForLink[link] = data
        return



