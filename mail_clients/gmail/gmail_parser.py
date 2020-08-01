import imaplib
import base64
import os
import email

from utils import mail_parser


class GmailParser:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.mail_server = "imap.gmail.com"
        self.mail = self.authenticate()

    def download_invoices(self):
        return self.download_attachments(keyword="invoice")

    def download_attachments(self, keyword):
        self.mail.select()
        type, data = self.mail.search(None, 'BODY', '"{}"'.format(keyword))
        email_ids = data[0].split()
        email_ids.reverse()
        attachments = []
        for num in email_ids:
            res, data = self.mail.fetch(num, '(RFC822)')
            raw_email = data[0][1]
            try:
                raw_email_string = raw_email.decode('utf-8')
            except:
                print("Problem reading email, ignoring")
                continue
            email_message = email.message_from_string(raw_email_string)
            for part in email_message.walk():
                # this part comes from the snipped I don't understand yet...
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue
                file_name = part.get_filename()
                if len(raw_email_string.split("₹")) == 0:  # not a invoice
                    continue
                amount = raw_email_string.split("₹")[-1].split()[0].strip()
                from_email = mail_parser.get_from_email_id(raw_email_string)
                invoice_date = mail_parser.get_invoice_date(raw_email_string)
                company = mail_parser.get_domain_from_email(from_email)
                if amount.isnumeric() and bool(file_name):
                    file_path = save_invoice(part=part, folder_name=company, file_name=file_name)
                    data = {"file_path": file_path, "amount": amount, "from_email": from_email,
                            "invoice_date": invoice_date}
                    attachments.append(data)
                    print(data)

    def authenticate(self):
        print("Authenticating user {}".format(self.username))
        mail = imaplib.IMAP4_SSL(self.mail_server)
        try:
            mail.login(self.username, self.password)
        except mail.error as e:
            if 'Invalid credentials' in str(e):
                print("Problem authenticating user. Please check credentials")
                exit(0)
            raise e
        return mail


def save_invoice(part, folder_name, file_name):
    base_dir = os.path.join(os.path.abspath(os.getcwd()), "invoices", folder_name)
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    file_path = os.path.join(os.path.abspath(os.getcwd()), "invoices", folder_name, file_name)
    if not os.path.isfile(file_path):
        fp = open(file_path, 'wb')
        fp.write(part.get_payload(decode=True))
        fp.close()
    return file_path
