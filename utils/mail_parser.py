import re


def get_from_email_id(raw_email_string):
    email_str = raw_email_string.split("From:")[-1].split("\n")[0]
    return re.findall('\S+@\S+', email_str)[0].replace("<", "").replace(">", "")


def get_domain_from_email(email_id):
    return email_id.split("@")[1].split(".")[0]


def get_invoice_date(raw_email_string):
    return raw_email_string.split("Received: by")[-1].split("\n")[1].strip()
