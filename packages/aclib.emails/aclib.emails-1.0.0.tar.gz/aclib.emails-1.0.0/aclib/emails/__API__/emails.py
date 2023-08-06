from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Self, Union
    FilePath = FileName = str
    FileData = Union[str, bytes]

import os, re, base64, smtplib, imaplib
from imapclient import imap_utf7
from email import message_from_bytes
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

class Mail(object):
    def __init__(self,
        From='', To='', FromAddr='', ToAddr='', Date='', Size='', Subject='', ContentType='text/plain',
        Content='', Attachments: list[FilePath | tuple[FileName, FileData]]=None
    ):
        self.From = From
        self.To = To
        self.FromAddr = FromAddr
        self.ToAddr = ToAddr
        self.Date = Date
        self.Size = Size
        self.Subject = Subject
        self.ContentType = ContentType
        self.Content = Content
        self.Attachments = Attachments or []

    def __repr__(self) -> str:
        sender = (self.From, self.FromAddr)
        recver = (self.To, self.ToAddr)
        subject = self.Subject
        nattachment = len(self.Attachments)
        return f'<Mail Sender={sender}, Recver={recver}, Subject={subject}, nattachment={nattachment}>'


class Server(object):

    @classmethod
    def sslimap_QQ(cls) -> Self:
        return cls('imap.qq.com', 993, True)

    @classmethod
    def sslsmtp_QQ(cls) -> Self:
        return cls('smtp.qq.com', 465, True)

    @classmethod
    def sslimap_126(cls) -> Self:
        return cls('imap.126.com', 993, True)

    @classmethod
    def sslsmtp_126(cls) -> Self:
        return cls('smtp.126.com', 465, True)

    def __init__(self, host: str, port: int, ssl=True):
        self.host = host
        self.port = port
        self.ssl = ssl


class User(object):

    def __init__(self, account: str, password: str):
        self.account = account
        self.password = password


class Recver(object):
    def __init__(self, server: Server, user: User, timeout=5):
        self.__imap = None
        self.__IMAP = imaplib.IMAP4_SSL if server.ssl else imaplib.IMAP4
        self.__server = (server.host, server.port)
        self.__user = (user.account, user.password)
        self.__timeout = timeout or None

    def connect(self):
        self.__imap = self.__IMAP(*self.__server, timeout=self.__timeout)

    def login(self) -> tuple[str, list[bytes]]:
        """return like: ('OK', [b'Success login ok'])"""
        reply = self.__imap.login(*self.__user)
        return reply

    def logout(self) -> tuple[str, list[bytes]]:
        """return like: ('BYE', [b'LOGOUT received'])"""
        reply = self.__imap.logout()
        return reply

    def cd(self, floderName) -> tuple[str, list[bytes]]:
        """return like: ('OK', [b'0'])"""
        reply = self.__imap.select(imap_utf7.encode(floderName))
        return reply

    def ls(self) -> list[str]:
        """list all folder of current user"""
        floders = []
        for floder in self.__imap.list()[1]:
            floders.append(imap_utf7.decode(floder.split(b' "/" ')[-1])[1:-1])
        return floders

    @staticmethod
    def __parseHeader_(data: str):
        if not data.find('?')+1:
            return data
        match = re.search(r'=\?(.*?)\?.*?\?(.*?)\?=', data)
        raw = match[0]
        charset = match[1]
        content = base64.b64decode(match[2]).decode(charset)
        return data.replace(raw, content)

    @staticmethod
    def __parseUser_(data: str):
        if not data.find('<')+1:
            return '', data
        match = re.search(r'<([^<]*)>$', data)
        username = data.replace(match[0], '').strip()
        useraddr = match[1]
        return username, useraddr

    def get_all_mailindex(self) -> list[str]:
        mailindex = self.__imap.search(None, 'ALL')[1][0].decode().split(' ')
        if not mailindex[0]:
            mailindex.clear()
        return mailindex

    def get_mail_byindex(self, index: int | str) -> Mail | None:
        data = self.__imap.fetch(str(index), '(INTERNALDATE RFC822.SIZE RFC822)')[1][0]
        if data is not None:
            mail = Mail()
            # 日期，大小
            meta = data[0].decode()
            mail.Date = re.search(r'"(.*)"', meta)[1]
            mail.Size = str(int(re.search(r'RFC822.SIZE (.*?) ', meta)[1])/1000) + 'KB'
            # 主体
            msg = message_from_bytes(data[1])
            mail.Subject = self.__parseHeader_(msg.get('Subject'))
            mail.From, mail.FromAddr = self.__parseUser_(self.__parseHeader_(msg.get('From')))
            mail.To, mail.ToAddr = self.__parseUser_(self.__parseHeader_(msg.get('To')))
            for part in filter(lambda _part: not _part.is_multipart(), msg.walk()):
                filename = part.get_filename()
                if filename:
                    fileName = self.__parseHeader_(filename)
                    fileContent = part.get_payload(decode=True)
                    mail.Attachments.append((fileName, fileContent))
                else:
                    content_type = part.get_content_type()
                    content_charset = part.get_content_charset()
                    content = part.get_payload(decode=True).decode(content_charset)
                    mail.ContentType = content_type
                    mail.Content = content
            return mail


class Sender(object):
    def __init__(self, server: Server, user: User):
        self.__SMTP = smtplib.SMTP_SSL if server.ssl else smtplib.SMTP
        self.__smtp = None
        self.__server = (server.host, server.port)
        self.__user = (user.account, user.password)

    def connect(self):
        self.__smtp = self.__SMTP(*self.__server)

    def login(self) -> tuple[int, bytes]:
        reply = self.__smtp.login(*self.__user)
        return reply

    def quit(self) -> tuple[int, bytes]:
        reply = self.__smtp.quit()
        return reply

    def send(self, mail: Mail):
        mime = MIMEMultipart('mixed')
        mime['Subject'] = mail.Subject
        mime['From'] = formataddr((mail.From, mail.FromAddr))
        mime['To'] = formataddr((mail.To, mail.ToAddr))
        mime.attach(MIMEText(mail.Content, mail.ContentType.split('/')[-1], 'utf-8'))
        for attachment in mail.Attachments:
            if type(attachment) == tuple:
                fname = attachment[0]
                fdata = attachment[1]
            if type(attachment) == str:
                with open(attachment, 'rb') as f:
                    fdata = f.read()
                fname = os.path.basename(attachment)
            mimeAttachment = MIMEApplication(fdata)
            mimeAttachment.add_header('Content-Disposition', 'attachment', filename=fname)
            mime.attach(mimeAttachment)
        self.__smtp.sendmail(mail.FromAddr, mail.ToAddr, mime.as_string())
