from mail_clients.gmail.gmail_parser import GmailParser

if __name__ == '__main__':
    email_user = input("Enter your gmail email id:")
    email_pass = input("Enter your password:")
    GmailParser(email_user, email_pass).download_invoices()
