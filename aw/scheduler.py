import schedule
import threading
import time

from aw.mailer import Mailer
from aw.scrapermanager import ScraperManager

class Scheduler:
    def __init__(self):
        self.freq = None
        self.hour = None
        self.day = None

        self.mail = None
        self.password = None
        self.smtpServer = None
        self.port = None

        self.logger = None
        self.mailer = None
        self.scraperManager = None

    def setScheduling(self, freq, hour, day):
        self.freq = freq
        self.hour = hour
        self.day = day

    def initMailer(self, mailer, mail, password, server, port):
        self.mailer = mailer
        self.mail = mail
        self.password = password
        self.smtpServer = server
        self.port = port

    def initScraperManager(self, sManager):
        self.scraperManager = sManager

    def initLogger(self, logger):
        self.logger = logger

    def run(self):
        records = self.scraperManager.getRecords()
        if self.mail and self.password and self.smtpServer and self.port:
            self.mailer.sendMail(records)
        else:
            raise ValueError("Mailer is not initialized!")
        
    def threadedRun(self):
        thread = threading.Thread(target=self.run)
        thread.start()

    def schedule(self):
        match self.freq:
            case "hourly":
                schedule.every().hour.at(self.hour).do(self.threadedRun)
            case "daily":
                schedule.every().day.at(self.hour).do(self.threadedRun)
            case "weekly":
                match self.day[:3]:
                    case "mon":
                        schedule.every().monday.at(self.hour).do(self.threadedRun)
                    case "tue":
                        schedule.every().tuesday.at(self.hour).do(self.threadedRun)
                    case "wed":
                        schedule.every().wednesday.at(self.hour).do(self.threadedRun)
                    case "thu":
                        schedule.every().thursday.at(self.hour).do(self.threadedRun)
                    case "fri":
                        schedule.every().friday.at(self.hour).do(self.threadedRun)
                    case "sat":
                        schedule.every().saturday.at(self.hour).do(self.threadedRun)
                    case "sun":
                        schedule.every().sunday.at(self.hour).do(self.threadedRun)
        
        while True:
            schedule.run_pending()
            time.sleep(1)
