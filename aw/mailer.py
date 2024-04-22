from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

class Mailer:
    def __init__(self, mail, password, smtp, smtpport):
        self.sender, self.receiver = mail, mail
        self.password = password
        self.smtp = smtp
        self.smtpport = smtpport

        self.message = None
        self.messageBody = None

    def sendMail(self, records):
        self._composeMail(records)

        with smtplib.SMTP_SSL(self.smtp, self.smtpport) as server:
            server.login(self.sender, self.password)
            server.send_message(self.message)


    def _composeMail(self, records):
        self.message = MIMEMultipart()
        self.message["From"] = self.sender
        self.message["To"] = self.receiver
        self.message["Subject"] = "subject"

        self.messageBody = self._composeMailBody(records)

        self.message.attach(MIMEText(self.messageBody, "html"))

    def _composeMailBody(self, records):
        header = "<h1>Record.</h1>"
        table = self._composeHtmlTable(records)
        html = f"<html><body>{header}{table}</body></html>"

        return html
    
    def _composeHtmlTable(self, records):
        table_header = "<th>Book</th><th>Author</th><th>Price</th><th>Year</th><th>Publisher</th><th>Link</th>"
        html_table = f"<table border='1'><tr>{table_header}</tr>"
        for rec in records:
            html_table += f"<tr><td>{rec.book}</td><td>{rec.author}</td><td>{rec.price}</td><td>{rec.year}</td><td>{rec.publisher}</td><td><a href=\"{rec.link}\">LINK</a></td></tr>"
        html_table += "</table>"

        return html_table