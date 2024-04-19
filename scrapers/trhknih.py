import requests as rq

from bs4 import BeautifulSoup, Comment
from typing import Union, Optional
from urllib.parse import urljoin, urlencode

from aw.scraper import Scraper
from aw.query import Query
from aw.record import Record

class TrhknihScraper(Scraper):
    NL = '\n'
    COMMENT_TEXT = "Last page link"
    WEB_URL = "https://www.trhknih.cz"
    SEARCH_ENDPOINT = "/hledat"

    def __init__(self):
        self.records = []
        self.soup = None

    def getLastPageNumber(self) -> int:
        lastPageComment = self.soup.find(
            text = lambda text: isinstance(text, Comment) and TrhknihScraper.COMMENT_TEXT in text
        )

        if lastPageComment:
            nextElement = lastPageComment.find_next("li")
            lastPageUrl = nextElement.find("a")["href"]
            lastPageNumber = lastPageUrl[
                lastPageUrl.index("=") + 1:lastPageUrl.index("&")
            ]
            lastPageNumber = int(lastPageNumber)
        else:
            lastPageNumber = 1

        return lastPageNumber

    def getUrl(self, queryString: str, pageNum: Optional[Union[None, int]] = None) -> str:
        urlParams = {
            "q": queryString,
            "type": "issue"
        }

        if type(pageNum) != None:
            urlParams.update({"page": str(pageNum)})

        encodedParams = urlencode(urlParams)
        fullUrl = urljoin(TrhknihScraper.WEB_URL, TrhknihScraper.SEARCH_ENDPOINT)
        fullUrlWithParams = urljoin(fullUrl, "?" + encodedParams)

        return fullUrlWithParams

    def initSoup(self, queryString: str, pageNum: Optional[Union[None, int]] = None) -> None:
        if type(pageNum) == None:
            url = self.getUrl(queryString)
        else:
            url = self.getUrl(queryString, pageNum)
        response = rq.get(url)
        content = response.text
        self.soup = BeautifulSoup(content, 'html.parser')
    
    def scrape(self, query: Query) -> list:
        self.initSoup(query.q)
        pages = self.getLastPageNumber()

        for pageNum in range(1, pages+1):
            self.initSoup(query.q, pageNum)
            span6_list = self.soup.find_all("div", attrs={"class": "span6"})
            for span6 in span6_list:
                span_price = span6.find("span", attrs={"class": "ask-count"})
                if span_price:
                    record = Record()
                    
                    record.link = f"{TrhknihScraper.WEB_URL}{span6.find("a")["href"]}"
                    record.book = span6.find("a").text
                    record.price = span6.find("span").text
                    record.year = span6.find_all("em")[0].text
                    record.publisher = span6.find_all("em")[1].text

                    innerHTML = span6.decode_contents()
                    text_after_kc = innerHTML[innerHTML.index("Kč"):]
                    text_after_br = text_after_kc[text_after_kc.index("<br/>") + 5:]
                    text_before_second_br = text_after_br[:text_after_br.index("<br/>")]
                    record.author = text_before_second_br.strip()

                    self.records.append(record)
    
    def getRecords(self, query: Query):
        self.scrape(query)
        return self.records
    





    
        
