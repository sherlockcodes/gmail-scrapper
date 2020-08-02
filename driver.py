from datetime import date, timedelta, datetime

from mail_clients.gmail.gmail_parser import GmailParser

DATE_FORMAT = "%d-%b-%Y"


def run():
    print("Welcome to GMAIL Invoice parser.")
    email_user = input("Enter your gmail email id:")
    email_pass = input("Enter your password:")
    print("Enter date range: (default last 30 days)")
    from_date = input("Enter From Date DD-Mon-YYYY e.g., 3-Jul-2020")
    to_date = input("Enter To Date DD-Mon-YYYY e.g., 13-July-2020")
    if len(from_date) == 0 and len(to_date) == 0:
        today = date.today()
        to_date = datetime.strftime(today, DATE_FORMAT)
        from_date = datetime.strftime(today - timedelta(30), DATE_FORMAT)

    invoice_data = GmailParser(email_user, email_pass).download_invoices(from_date=from_date, to_date=to_date)
    print("{} invoices downloaded from {} to {} under 'invoice' folder".format(len(invoice_data), from_date, to_date))
    total_spend = sum(invoice['amount'] for invoice in invoice_data)
    print("You spent total ₹ {}".format(total_spend))
    spent_map = {}

    for invoice in invoice_data:
        if invoice["company"] not in spent_map and invoice["amount"] > 0:
            spent_map[invoice["company"]] = 0
        if invoice["amount"] > 0:
            spent_map[invoice["company"]] += invoice["amount"]

    for company, total_spent_by_company in spent_map.items():
        print("You spent ₹{} in {}".format(total_spent_by_company, company))


if __name__ == '__main__':
    run()
