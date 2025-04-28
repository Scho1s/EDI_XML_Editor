"""
    Author      - Val J.
    Date        - 16/04/2025
    Updated     - 27/04/2025
    Description -
"""


import xml.etree.ElementTree as et
import os

# Logger
# TODO: Add logger


class XMLParser:
    def __init__(self, filename=None):
        self.filename = filename
        self.files = []
        self.invoices = dict()
        self.root = None

    def scan_dir(self, folder='.'):
        for file in os.scandir(folder):
            filename = file.name
            if filename.endswith('.XML'):
                self.files.append(filename)

    def parse(self):
        for file in self.files:
            if self.__init_root(file):
                if self.__check_file_is_edi():
                    self.__find_all_invoices()
                    self.__change_prices()
                    self.__rewrite_file()

    def __init_root(self, file):
        self.filename = file
        return self.__parse_root()

    def __parse_root(self):
        try:
            self.root = et.parse(self.filename)
            return True
        except FileNotFoundError:
            print(f"Error parsing {self.filename}. No file name provided or file does not exist.")
        except et.ParseError:
            print(f"Error parsing {self.filename}. XML file does not have tags")

    def __check_file_is_edi(self):
        try:
            assert self.__check_invoices_tag() is True
            assert self.__check_invoice_tags() is True
            return True
        except AttributeError as ae:
            print(f"Could not find root. Perhaps XML file is not an EDI file. {ae}")
        except AssertionError:
            pass

    def __check_invoices_tag(self):
        result = False
        try:
            tag_name = self.get_root().tag
            assert tag_name == 'Invoices'
            result = True
        except AssertionError:
            print(f"Tag error. Expect 'Invoices', got '{tag_name}'")
        finally:
            return result

    def __check_invoice_tags(self):
        try:
            all_tags = [tag.tag for tag in self.get_root()]
            assert "Invoice" in all_tags
        except AssertionError:
            print(f"Could not find any invoice tags. Got {all_tags}")

    def __find_all_invoices(self):
        self.invoices = {inv_num: {line_: line_.find('Prices')
                                   for line_ in inv_num.findall('Line')}
                         for inv_num in self.get_root().findall('Invoice')}

    def __change_prices(self):
        for invoice, lines in self.invoices.items():
            for line, prices in lines.items():
                self.__change_net_price(prices)
                self.__change_total_net_price(prices)
            self.__change_payment(invoice)

    @staticmethod
    def __change_net_price(prices_):
        gross_price = prices_.find('GrossPrice').text
        prices_.find('NetPrice').text = gross_price

    @staticmethod
    def __change_total_net_price(prices_):
        total_gross_price = prices_.find('TotalGrossPrice').text
        prices_.find('TotalNetPrice').text = total_gross_price

    @staticmethod
    def __change_payment(invoice):
        try:
            totals = invoice.find('Totals')

            total_gross = totals.find('TotalNetValue').text
            total_vat = totals.find('TotalVATValue').text
            totals.find('PaymentValue').text = str(format(float(total_gross) + float(total_vat), '.05f'))
        except AttributeError as ae:
            print(f'Invalid tag name. {ae}')

    def __rewrite_file(self):
        self.root.write(self.filename)

    def get_root(self):
        return self.root.getroot()


if __name__ == '__main__':
    parser = XMLParser()
    parser.scan_dir()
    parser.parse()
