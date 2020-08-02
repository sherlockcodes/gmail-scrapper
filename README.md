# Gmail Invoice Scrapper
   Gmail scrapper to download Invoice & Bills from Gmail using IMAP and Python.

## How to Run?

Go to project root directory and then run driver.py using below command

```shell
python driver.py
```

It will ask for Gmail username, password, from and to date.
From and to date is optional field, script takes last 30 days by Default if no input provided.

## Output
All the downloaded invoices/bills can be found under 'invoice' folder under root directory.
Invoices are segregated by company by making folders. 
Add-on, Once all invoice is downloaded. Script displays total spend and company-wise total invoice amount.
Please refer output from [here](https://github.com/sherlockcodes/gmail-scrapper/blob/master/output.png). 

#### Facing problems during authentication?

You may have to enable Less secure app access from google settings. 
You can do that from [here](https://myaccount.google.com/lesssecureapps?pli=1)



 
