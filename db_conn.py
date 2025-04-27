from sqlalchemy import create_engine, select, MetaData
import pyodbc
import os


class Database:
    TABLES = {'headers': 'SOP30200',
              'lines': 'SOP30300',
              'customers': 'RM00101',
              'weight': 'MH170121',
              }

    def __init__(self,
                 server=os.environ['GP_HOST'],
                 db=os.environ['GP_DB'],
                 driver='ODBC Driver 17 for SQL Server',
                 user=os.environ['GP_USER'],
                 psw=os.environ['GP_PASS']):
        self.server = server
        self.db = db
        self.driver = driver
        self.user = user
        self.psw = psw
        self.engine = None
        self.metadata = None
        self.prepare()

    def prepare(self):
        self.__init_db_engine()
        self.__init_metadata()

    def __init_db_engine(self):
        conn_string = f"mssql+pyodbc://{self.user}:{self.psw}@{self.server}/{self.db}?driver={self.driver}"
        self.engine = create_engine(conn_string)

    def __init_metadata(self):
        self.metadata = MetaData()
        self.metadata.reflect(bind=self.engine, only=list(self.TABLES.values()))

    def get_document_amount(self, sop_number):
        table = self.metadata.tables[self.TABLES['headers']]

        query = select(table.c.DOCAMNT).filter(table.c.SOPNUMBE.contains(f'{sop_number}'))
        with self.engine.connect() as conn:
            result = conn.execute(query)
            if result:
                return result.scalar()

    def get_weight(self, invoice_number=None):
        if invoice_number:
            dict_to_return = dict()

            for item in ["MOR200", "AGG200"]:
                query = (f"SELECT TRIM(ITEMNMBR) ITEMNMBR, MH_Weight_KG FROM MH170121 "
                         f"WHERE SOPNUMBE = '{invoice_number}' AND ITEMNMBR = '{item}'")
                with self.engine.connect() as conn:
                    result = conn.execute(query).fetchall()
                    if result:
                        dict_to_return[result[0][0]] = str(result[0][1])            # Change result[0][0] to _item_
            return dict_to_return
