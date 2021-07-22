
class CityDataProvider:
    def getLinkForTerm(self, term : str) -> str:
        pass

    def getDataForLink(self, link : str) -> dict:
        pass

    def putLinkForTerm(self, term : str, link : str) -> None:
        pass

    def putDataForLink(self, link : str, data : str) -> None:
        pass

    def getDataForTerm(self, term : str) -> dict:
        link = self.getLinkForTerm(term)
        if link:
            data = self.getDataForLink(link)
            return data
        return None
    


