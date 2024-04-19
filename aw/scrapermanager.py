from os.path import join
from os import listdir
import importlib.util

from aw.constants import ROOT_DIR, SCRAPERS_DIR
from aw.scraper import Scraper

class ScraperManager:
    def __init__(self):
        self.queryParser = None
        self.scraperDirList = [SCRAPERS_DIR]
        self.scraperList = []
        self.queryList = []
        self.recordList = []

    def _attachQueryParser(self, qparser):
        self.queryParser = qparser

    def _scanForScrapers(self):
        for dirName in self.scraperDirList:
            absPath = join(ROOT_DIR, dirName)
            for file in listdir(absPath):
                print(file)
                if file.endswith(".py"):
                    fileAbsPath = join(absPath, file)
                    spec = importlib.util.spec_from_file_location("module", fileAbsPath)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    for object in dir(module):
                        print(object)
                        objectClass = getattr(module, object, None)
                        if isinstance(objectClass, type) and issubclass(objectClass, Scraper):
                            try:
                                self.scraperList.append(objectClass())
                            except TypeError:
                                pass

    
                    