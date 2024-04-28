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

        self.enabled = False
        self.currentJob = None

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

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def switch(self):
        self.enabled = not(self.enabled)

    def run(self):
        print("start run")
        records = self.scraperManager.getRecords()
        if self.mail and self.password and self.smtpServer and self.port:
            self.mailer.sendMail(records)
            print("mail sent")
        else:
            raise ValueError("Mailer is not initialized!")
        
    def threadedRun(self):
        thread = threading.Thread(target=self.run)
        thread.start()

    def reset(self):
        if self.currentJob:
            schedule.cancel_job(self.currentJob)
            self.currentJob = None
        
        self.schedule(self)

    def changesScheduling(self, newFreq = None, newDay = None, newHour = None):
        self.freq = newFreq or self.freq
        self.day = newDay or self.day
        self.hour = newHour or self.hour

        self.reset()

    def schedule(self):
        match self.freq:
            case "hourly":
                print("start hourly")
                self.currentJob = schedule.every().hour.at(self.hour[2:]).do(self.threadedRun)
            case "daily":
                self.currentJob = schedule.every().day.at(self.hour).do(self.threadedRun)
            case "weekly":
                match self.day[:3]:
                    case "mon":
                        self.currentJob = schedule.every().monday.at(self.hour).do(self.threadedRun)
                    case "tue":
                        self.currentJob = schedule.every().tuesday.at(self.hour).do(self.threadedRun)
                    case "wed":
                        self.currentJob = schedule.every().wednesday.at(self.hour).do(self.threadedRun)
                    case "thu":
                        self.currentJob = schedule.every().thursday.at(self.hour).do(self.threadedRun)
                    case "fri":
                        self.currentJob = schedule.every().friday.at(self.hour).do(self.threadedRun)
                    case "sat":
                        self.currentJob = schedule.every().saturday.at(self.hour).do(self.threadedRun)
                    case "sun":
                        self.currentJob = schedule.every().sunday.at(self.hour).do(self.threadedRun)
        
        while self.enabled:
            schedule.run_pending()
            time.sleep(1)
