"""
    Author      - Val J.
    Date        - 16/04/2025
    Updated     -
    Dsecription -
"""


import xml.etree.ElementTree as et

# Logger
# TODO: Add logger


class XMLParser:
    def __init__(self, filename=None):
        self.filename = filename
        self.files = []
        self.invoices = dict()
        self.root = None

    def __check_file_exists(self):
        try:
            self.root = et.parse(self.filename)
            return True
        except AttributeError:
            print(f"Cannot parse - no file name provided or file does not exist.")

    def __find_all_invoices(self):
        self.invoices = {inv_num: {line_: line_.find('Prices')
                                   for line_ in inv_num.findall('Line')}
                         for inv_num in self.get_root().findall('Invoice')}

    @staticmethod
    def __change_net_price(prices_):
        gross_price = prices_.find('GrossPrice').text
        prices_.find('NetPrice').text = gross_price

    @staticmethod
    def __change_total_net_price(prices_):
        total_gross_price = prices_.find('TotalGrossPrice').text
        prices_.find('TotalNetPrice').text = total_gross_price

    @staticmethod
    def __change_payable(invoice):
        try:
            totals = invoice.find('Totals')

            total_gross = totals.find('TotalNetValue').text
            total_vat = totals.find('TotalVATValue').text
            totals.find('PaymentValue').text = str(format(float(total_gross) + float(total_vat), '.05f'))
        except AttributeError as ae:
            print(f'Invalid tag name. {ae}')

    def __extract_price_values(self):
        for invoice, lines in self.invoices.items():
            for line, prices in lines.items():
                self.__change_net_price(prices)
                self.__change_total_net_price(prices)

            self.__change_payable(invoice)

    def __rewrite_file(self):
        self.root.write(self.filename)

    def parse(self):
        if self.__check_file_exists():
            self.__find_all_invoices()
            self.__extract_price_values()
            self.__rewrite_file()

    def get_root(self):
        return self.root.getroot()


class Invoice:
    def __init__(self, doc_num=None, total_vat=0, total_net=0):
        self.doc_num = doc_num
        self.total_vat = total_vat
        self.total_net = total_net
        self.total_payable = total_vat + total_net

    def get_total_payable(self):
        return self.total_payable


if __name__ == '__main__':
    parser = XMLParser('TX003885.XML')
    parser.parse()
