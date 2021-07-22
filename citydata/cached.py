from citydata.data_provider_interface import CityDataProvider



class CachedCityDataProvider(CityDataProvider):
    def __init__(self, dataStores : list[CityDataProvider]) -> None:
        self.dataStores = dataStores

    def getLinkForTerm(self, term : str) -> str:
        link = None
        storesWithoutLink = []
        for store in self.dataStores:
            link = store.getLinkForTerm(term)
            if link:
                break
            else:
                storesWithoutLink.append(store)
        if link:
            for store in storesWithoutLink:
                store.putLinkForTerm(term, link)
        return link

    def getDataForLink(self, link : str) -> dict:
        data = None
        storesWithoutData = []
        for store in self.dataStores:
            data = store.getDataForLink(link)
            if data:
                break
            else:
                storesWithoutData.append(store)
        if data:
            for store in storesWithoutData:
                store.putDataForLink(link, data)
        return data

    def putLinkForTerm(self, term : str, link : str) -> None:
        for store in self.dataStores:
            store.putLinkForTerm(term, link)
        return
    
    def putDataForLink(self, link : str, data : str) -> None:
        for store in self.dataStores:
            store.putDataForLink(link, data)
        return




