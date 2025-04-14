"""
    Author      - Val J.
    Date        - 09/04/2025
    Updated     -
    Dsecription -
"""


import xml.etree.ElementTree as et
from os import scandir, path
from db_conn import Database

# Logger
# TODO: Add logger

# Header elements
HEADER = "Header"
PARTNER = "Partner"
ACC_CODE = "PartnerAccountCode"
CUSTOMER = "WAIT002"

# Item line elements
LINE = "Line"
LINE_NUM = "LineNumber"
PRODUCT = "Product"
PR_CODE = "ProductCode"
CODE = "PartnerProductCode"

# TODO:
"""
VATCode
PartnerProductCode
NetPrice 
TotalNetPrice
PaymentValue
"""


class XMLParser:
    def __init__(self, filename=None):
        self.filename = filename
        self.root = None

    def __check_file_exists(self):
        try:
            self.root = et.parse(self.filename)
            return True
        except AttributeError:
            print(f"Cannot parse - no file name provided.")

    def get_root(self):
        return self.root.getroot()

    def get_document_number(self, child_):
        try:
            document_number = child_.find('Header').find('ReferenceNumbers').find('DocumentNumber').text
            return document_number
        except AttributeError as e:
            print(f"One or more tags could not be recognised.\n{e}")
            return None

    def get_all_invoices(self):
        invoices = self.get_root().findall('Invoice')
        return invoices

    def get_all_invoice_lines(self):


    def get_all_invoices(self):
        xml_file.invoices = self.get_all_invoices()

        for child in xml_file.invoices:
            doc_num = self.get_document_number(child)
            lines = self.get_all_invoice_lines(child)


class Invoice:
    def __init__(self, doc_num=None, total_vat=0, net=0, total_net=0):
        self.doc_num = doc_num
        self.total_vat = total_vat
        self.net = net
        self.total_net = total_net
        self.total_payable = 0

    def calculate_total_payable(self):
        self.total_payable = self.total_vat + self.total_net


class XMLFile:
    def __init__(self, filename=None):
        self.filename = filename
        self.invoices = []



if __name__ == '__main__':
    xml_file = XMLFile()



    #db = Database()
    #print(db.get_document_amount('INV476617'))

"""
def __is_waitrose(parent, file):
    try:
        header = parent.find(HEADER).find(PARTNER).find(ACC_CODE).text
        logger.info(f"{'Matching order found - ' + file.name if header==CUSTOMER else 'No matching orders found for ' + header}")
        return header == CUSTOMER
    except Exception as e:
        logger.info(f'{__is_waitrose.__name__}. {e}')

def __sort_children_by(parent):
    header_ = [parent[0], ]
    try:
        line = parent.find(LINE).find(PRODUCT).find(CODE).text
        if line:
            counter = 1
            parent[:] = header_ + sorted(parent[1:], key=lambda child: int(line))
            for child in parent[1:]:
                child.find(LINE_NUM).text = str(counter)
                counter += 1
            return True
    except Exception as e:
        logger.info(f"{__sort_children_by.__name__}. File has not been sorted. {e}")


def scan_folder(folder='.'):
    files = 0
    for file in scandir(folder):
        if not file.name.endswith(".XML"):
            continue
        tree = et.parse(path.join(folder if folder != '.' else '', file.name))
        root = tree.getroot()[0]
        if __is_waitrose(root, file):
            if __sort_children_by(root):
                tree.write(file.name)
                files += 1
    return files


if __name__ == "__main__":
    try:
        files_processed = scan_folder()
        logger.info(f"Main function. Files processed: {files_processed}\n{'No errors found.' if files_processed else ''}")
        input("Press any key to proceed...")
    except Exception as e:
        logger.info(f'Main function. {e}')
"""

