from email.header import Header
from email.mime.text import MIMEText


class MailBuilder:
    def __init__(self) -> None:
        pass

    def content(self, content):
        self._content = content
        return self

    def frm(self, name, usn):
        self._from = '%s <%s>' % (
            Header(name, 'utf-8').encode(), usn)
        return self

    def to(self, addr):
        self._to = addr
        return self

    def subject(self, subject):
        self._subject = Header(subject, 'utf-8').encode()
        return self

    def build(self):
        message = MIMEText(self._content, 'html', 'utf-8')
        message['From'] = self._from
        message['To'] = self._to
        message['Subject'] = self._subject
        return message
