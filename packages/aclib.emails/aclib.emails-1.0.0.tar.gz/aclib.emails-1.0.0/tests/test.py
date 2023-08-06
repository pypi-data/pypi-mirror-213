from time import sleep
from aclib.emails import Mail, Server, User, Recver, Sender

recver = Recver(Server.sslimap_QQ(), User('mailserver_acsr@foxmail.com', 'sdubxmmbotrvbaee'))
print(recver)
print(recver.connect())
print(recver.login())
print(recver.ls())

print(recver.cd('INBOX'))

print(recver.get_all_mailindex())

print(recver.get_mail_byindex(6))

sleep(1)
print(recver.logout())

# sender = Sender(Server('smtp.126.com', 465), User('vmfkuitpyoiutewfae@126.com', 'JXBKMPPXMIIODUIQ'))
# sender.connect()

# print(sender.login())

# sender.send(Mail('WYYX', 'QQYX', 'vmfkuitpyoiutewfae@126.com', 'mailserver_acsr@foxmail.com', Content='Hello aclib.emails!',
# Subject='Source', Attachments=[('x.txt', 'hhh')]))

# sleep(1)
# print(sender.quit())