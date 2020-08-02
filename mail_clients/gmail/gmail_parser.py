import imaplib
import email

from utils import mail_parser, attachment_utility

GET_LATEST_FIRST = True


class GmailParser:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.mail_server = "imap.gmail.com"
        self.mail = self.authenticate()

    def download_invoices(self, from_date=None, to_date=None):
        print("Downloading invoice from {} to {}".format(from_date, to_date))
        return self.download_attachments(keyword="invoice", from_date=from_date, to_date=to_date)

    def download_attachments(self, keyword, from_date=None, to_date=None):
        self.mail.select()  # select all folders. can pass "INBOX|UPDATES|PROMOTIONS"
        query = '(BODY "{}" SINCE "{}" BEFORE "{}")'.format(keyword, from_date, to_date)
        type, data = self.mail.search(None, query)
        message_ids = data[0].split()
        if GET_LATEST_FIRST:
            message_ids.reverse()
        attachments_data = []
        for num in message_ids:
            res, data = self.mail.fetch(num, '(RFC822)')
            raw_email = data[0][1]
            try:
                raw_email_string = raw_email.decode('utf-8')
            except:
                continue
            email_message = email.message_from_string(raw_email_string)
            for part in email_message.walk():
                from_email = mail_parser.get_from_email_id(raw_email_string)
                company = mail_parser.get_domain_from_email(from_email)
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue
                file_name = part.get_filename()
                amount = mail_parser.get_invoice_amount(raw_email_string)
                invoice_date = mail_parser.get_invoice_date(raw_email_string)
                if bool(file_name):
                    file_name = file_name.split("/")[-1]  # to ignore email attachments with slashes
                    file_path = attachment_utility.save_invoice(part=part, folder_name=company, file_name=file_name)
                    data = {"file_path": file_path, "from_email": from_email,
                            "invoice_date": invoice_date, "amount": amount, "company": company}
                    attachments_data.append(data)
        return attachments_data

    def authenticate(self):
        print("Authenticating user {}".format(self.username))
        mail = imaplib.IMAP4_SSL(self.mail_server)
        try:
            mail.login(self.username, self.password)
            print("Authentication success.")
        except mail.error as e:
            print("Authentication failed.")
            if 'Invalid credentials' in str(e):
                print("Problem authenticating user. Please check credentials")
                exit(0)
            raise e
        return mail
