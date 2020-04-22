import sqlite3


class SqLiteConnector:

    def __init__(self, name='stData'):
        self.dn = name
        self.connector = None
        self.cursor = None

    def name_database(self, dname):
        self.dn = dname

    def start_database_connection(self):
        self.connector = sqlite3.connect('{}.db'.format(self.dn))
        self.cursor = self.connector.cursor()

    def create_table(self, tname):
        if not self.connector:
            raise ConnectorNotOpenError('while creating a table.')
        self.connector.execute('''CREATE TABLE IF NOT EXISTS '{}' 
        (time real, name text, message_text real)'''.format(tname))

    def insert_to_table(self, tname, timestamp, name, message):
        if not self.connector:
            raise ConnectorNotOpenError('while creating a table.')
        self.connector.execute('''INSERT INTO {} VALUES('{}','{}', '{}')'''.format(tname, timestamp, name, message))

    def commit_changes(self):
        if self.connector:
            self.connector.commit()

    def close_database_connection(self):
        if self.connector:
            self.connector.close()

    def close_table(self, tname):
        self.connector.execute('''DROP TABLE '{}'; '''.format(tname))

    def get_all_from_table(self, tname):
        self.cursor.execute('''SELECT * FROM '{}';'''.format(tname))

    def search_in_table(self, tname, name):
        self.cursor.execute('''SELECT * FROM '{}' WHERE name='{}';'''.format(tname, name))


class ConnectorNotOpenError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'Connector to Database not open, {0}'.format(self.message)
        else:
            return 'Connector to Database not open'
