from citydata.data_provider_interface import CityDataProvider

import json
from pathlib import Path
import re

def sanitizeLink(link : str) -> str:
    key = re.sub(r"^.*\/", "", link)
    return key

def sanitizeTerm(term : str) -> str:
    key = term.lower().strip()
    return key

class FileBasedCityDataProvider(CityDataProvider):
    def __init__(self, baseDir : str) -> None:
        baseDirPath = Path(baseDir)
        if not baseDirPath.exists():
            baseDirPath.mkdir()
        if not baseDirPath.is_dir():
            raise Exception("Not a dir: " + baseDir)
        self.baseDir = baseDir
        return

    def getFilePath(self, type : str, key : str):
        path = self.baseDir + "/" + type + "_" + key + ".json"
        return path
        
    def getLinkForTerm(self, term : str) -> str:
        filePathName = self.getFilePath("link", sanitizeTerm(term))
        filePath = Path(filePathName)
        if filePath.is_file():
            file = open(filePathName, "r")
            linkData = json.load(file)
            link = linkData["link"]
            return link
        return None
            
    def getDataForLink(self, link : str) -> dict:
        filePathName = self.getFilePath("data", sanitizeLink(link))
        filePath = Path(filePathName)
        if filePath.is_file():
            file = open(filePathName, "r")
            data = json.load(file)
            return data
        return None

    def putLinkForTerm(self, term : str, link : str) -> None:
        filePathName = self.getFilePath("link", term)
        linkData = {"link": link}
        file = open(filePathName, "w")
        json.dump(linkData, file)
        pass

    def putDataForLink(self, link : str, data : str) -> None:
        filePathName = self.getFilePath("data", sanitizeLink(link))
        file = open(filePathName, "w")
        json.dump(data, file)
        pass



