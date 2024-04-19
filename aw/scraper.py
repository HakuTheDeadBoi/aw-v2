from abc import ABC, abstractmethod

class Scraper(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def getRecords():
        pass