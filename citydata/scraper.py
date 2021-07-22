
from citydata.data_provider_interface import CityDataProvider


from bs4 import BeautifulSoup
import requests
import re

GOOGLE_URL_PREFIX = "https://www.google.com/search?q=site%3Aen.wikipedia.org+"
WIKIPEDIA_URL_PREFIX = "https://en.wikipedia.org/wiki/"



def getWikipediaRawText(link):
    wikipediaRawTextLink = link + "?action=raw"
    response = requests.get(wikipediaRawTextLink)
    return response.text


def parseCoordinate(coordinateText, coordinateDirection):
    coordParts = coordinateText.split("|")
    coordinate = float(coordParts[0])
    if len(coordParts) >= 2:
        coordinate += float(coordParts[1]) / 60
    if len(coordParts) >= 3:
        coordinate += float(coordParts[2]) / 3600
    if coordinateDirection == "S" or coordinateDirection == "W":
        coordinate *= -1
    return coordinate


def findAndExtractFirstGroup(pattern, text, groupNumber):
    matchObject = re.search(pattern, text)
    if matchObject:
        return matchObject.group(groupNumber)
    return None
        

def extractWikipediaTemplateValue(text, fieldName):
    pattern = "\|\s*" + fieldName + "\s*=\s*(.*?)\s+[\|\}]"
    filedValue = findAndExtractFirstGroup(pattern, text, 1)
    return filedValue

def parseWikipediaLinkFormatting(text):
    textFiltered = re.sub(r"[\[\]]", "", text)
    return textFiltered

def parseWikipediaLocation(text):
    flagFormatMatch = re.search("\{\{flag\|(.*)\}\}", text)
    if flagFormatMatch:
        textFiltered = flagFormatMatch.group(1)
    else:
        textFiltered = text
    textFiltered = re.sub("\{\{flagicon\|.*\}\}\s*", "", text)
    textFiltered = re.sub("^.*name=", "", textFiltered)
    textFiltered = re.sub("^.*\|", "", textFiltered)
    return textFiltered

def parsePositiveInt(text):
    if not text:
        return 0
    textFiltered = text.replace(",", "")
    textFiltered = re.sub(r"\D.*$", "", textFiltered)
    if not textFiltered:
        return 0
    population = int(textFiltered)
    return population

def parseFloat(text):
    if not text:
        return 0
    textFiltered = text.replace(",", "").replace("−", "-")
    textFiltered = re.sub(r"[^\d\.\-].*$", "", textFiltered)
    value = 0
    if textFiltered:
        value = float(textFiltered)
    return value

def parseWikipediaCoordinates(rawText):
    coordinatesData = re.search(r"\{\{coord\|(.*?)\|([NS])\|(.*?)\|([EW])", rawText, re.MULTILINE)
    if coordinatesData:
        latText = coordinatesData.group(1)
        latDir = coordinatesData.group(2)
        lonText = coordinatesData.group(3)
        lonDir = coordinatesData.group(4)
        lat = parseCoordinate(latText, latDir)
        lon = parseCoordinate(lonText, lonDir)
        return {"lat": lat, "lon": lon}
    return None

def parseWikipediaPopulation(rawText):
    populationText = extractWikipediaTemplateValue(rawText, "population_total")
    return parsePositiveInt(populationText)

def parseWikipediaElevation(rawText):
    elevationText = extractWikipediaTemplateValue(rawText, "elevation_m")
    return parseFloat(elevationText)

def parseWikipediaSubdivisions(rawText):
    subdivisionsPrelim = [
        extractWikipediaTemplateValue(rawText, "subdivision_name"),
        extractWikipediaTemplateValue(rawText, "subdivision_name1"),
        extractWikipediaTemplateValue(rawText, "subdivision_name2")]
    subdivisions = []
    for subdivisionPrelim in subdivisionsPrelim:
        if subdivisionPrelim:
            subdivision = parseWikipediaLocation(parseWikipediaLinkFormatting(subdivisionPrelim))
            if subdivision not in subdivisions:
                subdivisions.append(subdivision)
    return subdivisions

def getDataForWikipediaRawText(rawText):
    data = {}
    data["coordinates"] = parseWikipediaCoordinates(rawText)
    data["population"] = parseWikipediaPopulation(rawText)
    data["elevation"] = parseWikipediaElevation(rawText)
    data["subdivisions"] = parseWikipediaSubdivisions(rawText)
    return data



class ScraperCityDataProvider(CityDataProvider):
    def __init__(self) -> None:
        pass

    def getLinkForTerm(self, term : str) -> str:
        # Search Google
        #
        searchUrl = GOOGLE_URL_PREFIX + term
        response = requests.get(searchUrl)
        # Parse results looking for link matching Wikipedia
        #
        soup = BeautifulSoup(response.text, features="html.parser")
        links = soup("a")
        firstWikipediaRawResultLink = ""
        for link in links:
            linkUrl = link["href"]
            if WIKIPEDIA_URL_PREFIX in linkUrl:
                firstWikipediaRawResultLink = linkUrl
                break
        # Extract just Wikipedia link
        #
        linkSubstringStart = firstWikipediaRawResultLink.index(WIKIPEDIA_URL_PREFIX)
        linkSubstringEnd = firstWikipediaRawResultLink.index("&", linkSubstringStart)
        firstWikipediaLink = firstWikipediaRawResultLink[linkSubstringStart:linkSubstringEnd]
        return firstWikipediaLink
        
    def getDataForLink(self, link : str) -> dict:
        wikipediaRawText = getWikipediaRawText(link)
        data = getDataForWikipediaRawText(wikipediaRawText)
        return data

    def putLinkForTerm(self, term : str, link : str) -> None:
        pass

    def putDataForLink(self, link : str, data : str) -> None:
        pass    





