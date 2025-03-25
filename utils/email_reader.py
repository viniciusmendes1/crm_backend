import imaplib
import email

class EmailReader:
    def __init__(self, email_user, email_pass, imap_server):
        self.email_user = email_user
        self.email_pass = email_pass
        self.imap_server = imap_server
        self.mail = imaplib.IMAP4_SSL(self.imap_server)
        self.mail.login(self.email_user, self.email_pass)

    def fetch_emails(self, folder="inbox"):
        self.mail.select(folder)
        status, messages = self.mail.search(None, "ALL")
        email_ids = messages[0].split()
        emails = []
        for e_id in email_ids:
            status, msg_data = self.mail.fetch(e_id, "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])
            emails.append(msg)
        return emails