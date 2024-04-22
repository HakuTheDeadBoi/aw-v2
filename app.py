from aw.scheduler import Scheduler
from aw.mailer import Mailer
from aw.scrapermanager import ScraperManager

mail = None
password = None
server = None
port = None

sch = Scheduler()
sm = ScraperManager()
ml = Mailer(mail, password, server, port)

sch.initMailer(ml, mail, password, server, port)
sch.initScraperManager(sm)
sch.setScheduling("daily", "16:02", "mon")
sch.schedule()