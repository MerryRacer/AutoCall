from datetime import date

from imap_tools import MailBox, AND
from twilio.rest import Client
from configparser import ConfigParser
import time
import re

config = ConfigParser()
# https://stackoverflow.com/questions/19078170/python-how-would-you-save-a-simple-settings-config-file
config.read('config.ini')

sec_utc = time.time()
s1: str = (config.get('main', 'time_start'))  # -> "value1"
s2: str = (config.get('main', 'time_finish'))
member = str((config.get('phones', 'member')))
member_main = str((config.get('phones', 'member_main')))
member_email = (config.get('main', 'member_email'))
member_pas = (config.get('main', 'member_pas'))
imap = (config.get('main', 'imap'))
sid = (config.get('main', 'sid'))
token = (config.get('main', 'token'))
FMT = '%H:%M:%S'
x = time.localtime(sec_utc)

now = time.strftime('%H:%M:%S', x)
found = False
if s1 < now < s2:
    mb = MailBox(imap).login(member_email, member_pas)
    messages = mb.fetch(criteria=AND(seen=False),
                        mark_seen=False,
                        bulk=True)  # непрочитанные сообщения, не отмечать флагом
    words = str((config.get('main', 'words')))
    for msg in messages:
        if re.match(words, msg.subject): #Если содержиться в заголовке слово
            print('Есть почта')
            account_sid = sid  # Your Account SID from www.twilio.com/console
            auth_token = token  # Your Auth Token from www.twilio.com/console
            client = Client(account_sid, auth_token)
            current_date = str(date.today())
            print(current_date)
            calls = client.calls.list(status='no-answer',
                                      to=member,
                                      start_time=current_date,
                                      limit=20
                                      )
            tc = int((config.get('main', 'try_call')))

            count_calls = len(calls)
            member_from = (config.get('phones', 'member_from'))
            if int(count_calls) < tc:  # Кол-во звонков с указанным статусов
                print(count_calls)
                print("Звоним")
                call = client.calls.create(
                    to=member,
                    from_=member_from,
                    url="http://demo.twilio.com/docs/voice.xml"
                )
                found = True
                break
            else:
                print('Не звоним')
                call = client.calls.create(
                    to=member_main,
                    from_=member_from,
                    url="http://demo.twilio.com/docs/voice.xml"
                )
                found = True
                break
else:
    print('End')
