import re


def get_from_email_id(raw_email_string):
    email_str = raw_email_string.split("From:")[-1].split("\n")[0]
    return re.findall('\S+@\S+', email_str)[0].replace("<", "").replace(">", "")


def get_domain_from_email(email_id):
    return email_id.split("@")[1].split(".")[0]


def get_invoice_date(raw_email_string):
    return raw_email_string.split("Received: by")[-1].split("\n")[1].strip()


def get_invoice_amount(raw_email_string):
    if "₹" not in raw_email_string and "E2=82=B9=C2=A0" not in raw_email_string:  # not a invoice
        return 0
    amount = 0
    if "₹" in raw_email_string:
        amount = raw_email_string.split("₹")[-1].split()[0].strip()
    if "E2=82=B9=C2=A0" in raw_email_string:
        amount = raw_email_string.split("E2=82=B9=C2=A0")[-1].split()[0].strip()
        amount = re.findall(r'\d+', amount)[0]
    if amount.isnumeric():
        return int(amount)
    return 0
