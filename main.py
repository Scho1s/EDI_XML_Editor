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
VATCode (strip), 
PartnerProductCode (strip), 
NetPrice (ITEMPRCE), 
TotalNetPrice (XTNDPRCE), 
PaymentValue (DOCAMNT)
"""


class XMLParser:
    def __main__(self, filename=None):
        self.filename = filename


if __name__ == '__main__':
    db = Database()
    db.

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

