from bs4 import BeautifulSoup
import requests

list = []

def request(version):
    version = str(version)
    url = f"https://files.minecraftforge.net/net/minecraftforge/forge/index_{version}.html"
    req = requests.get(url).text
    doc = BeautifulSoup(req, "html.parser")
    tags = doc.find_all(["a"], title="Installer", href=True)
    for a in tags:
        list.append(a["href"])
    
def GetLatestURL(version):
    request(version)
    latestURL = str(list[0])
    latestURL = latestURL[latestURL.find("&")+5:]
    return latestURL

def GetRecommendedURL(version):
    request(version)
    recommendedURL = str(list[1])
    recommendedURL = recommendedURL[recommendedURL.find("&")+5:]
    return recommendedURL


