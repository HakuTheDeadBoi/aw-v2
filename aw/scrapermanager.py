from os.path import join
from os import listdir
import importlib.util

from conf import (
    ROOT_DIR, SCRAPERS_DIR, QUERIES_DIR, QUERIES_FILENAME_DEFAULT
)
from aw.scraper import Scraper
from aw.queryparser import QueryParser

class ScraperManager:
    def __init__(self):
        self.queryParser = QueryParser()
        self.scraperDirList = [SCRAPERS_DIR]
        self.scraperList = []
        self.queryList = []
        self.recordList = []

    def _initQueryParser(self):
        self.queryParser.initFile(ROOT_DIR, QUERIES_DIR, QUERIES_FILENAME_DEFAULT)

    def _scanForQueries(self):
        self.queryList.extend(self.queryParser.getQueryList())

    def _scanForScrapers(self):
        for dirName in self.scraperDirList:
            absPath = join(ROOT_DIR, dirName)
            for file in listdir(absPath):
                if file.endswith(".py"):
                    fileAbsPath = join(absPath, file)
                    spec = importlib.util.spec_from_file_location("module", fileAbsPath)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    for object in dir(module):
                        objectClass = getattr(module, object, None)
                        if isinstance(objectClass, type) and issubclass(objectClass, Scraper):
                            try:
                                self.scraperList.append(objectClass())
                            except TypeError:
                                pass

    def _scanForRecords(self):
        for scraper in self.scraperList:
            for query in self.queryList:
                allRecords = []
                # place to filter results
                allRecords.extend(scraper.getRecords(query))

                self.recordList.extend(allRecords)

    def _filterResults(self, query):
        # filter results by given constraints
        pass

    def getRecords(self):
        self._initQueryParser()
        self._scanForScrapers()
        self._scanForQueries()
        self._scanForRecords()

        result = self.recordList

        # reset state
        self.scraperList = []
        self.queryList = []
        self.recordList = []

        return result

    
                    