""" Monkey-patch smtplib so we don't send actual emails.
Thanks to http://www.psychicorigami.com/2007/09/20/monkey-patching-pythons-smtp-lib-for-unit-testing/

Importing this module and smtplib.SMTP will refer to the DummySMTP bellow.

It provides access to any sent messages via emailutils.inbox and the last 
SMTP class created via emailutils.smtp.

Example : 

	import emailutils

	def test_some_email():
	    emailutils.inbox = [] # clear the inbox
	    # code that does some emailing here
	    assert len(emailutils.inbox) == 1 # check one email was sent
	    assert emailutils.inbox[0].to_address == 'someone@somewhere.com'
"""

smtp = None
inbox = []

class Message(object):

    def __init__(self, from_address, to_address, fullmessage):
        self.from_address = from_address
        self.to_address = to_address
        self.fullmessage = fullmessage

class DummySMTP(object):

    def __init__(self, address):
        self.address = address
        global smtp
        smtp = self

    def login(self, username, password):
        self.username = username
        self.password = password

    def sendmail(self, from_address, to_address, fullmessage):
        global inbox
        inbox.append(Message(from_address, to_address, fullmessage))
        return []

    def quit(self):
        self.has_quit = True

# this is the actual monkey patch (simply replacing one class with another)
import smtplib
smtplib.SMTP = DummySMTP