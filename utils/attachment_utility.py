import os


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
