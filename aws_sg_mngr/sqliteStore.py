from aws_sg_mngr.cidrStore import CidrStore
from aws_sg_mngr.registeredCidr import RegisteredCidr
import os
import sqlite3


class SqliteStore(CidrStore):

    def __init__(self, config, logger=None):
        self.db_conn = None
        # TODO: how does this file be packaged?
        self.CREATE_SCHEMA_FILE = 'config/cidrs_schema.sql'
        self.db_filename = config.get('DB', 'path')
        # self.schema_file = config.get('DB', 'schema_path')
        self.__init_db__()

    def __del__(self):
        if self.db_conn is not None:
            self.db_conn.close()
            self.db_conn = None

    def __init_db__(self):
        # sqlite3 will not error on a non-existant file, but simply create a new one
        if not os.path.exists(self.db_filename):
            self.db_conn = sqlite3.connect(self.db_filename)
            with open(self.CREATE_SCHEMA_FILE, 'r') as schema:
                self.db_conn.execute(schema.read())

                # We'll define the global Cidr
                self.db_conn.execute(
                    "insert into registeredCidrs " +
                    "(cidr, description, location, owner, expiration) " +
                    "VALUES ('0.0.0.0/0', 'Global', 'Internet', 'aws-sg-mngr', {0});"
                    .format(RegisteredCidr.DO_NOT_EXPIRE))
                # self.db_conn.execute(
                #     "insert into registeredCidrs(cidr, description) " +
                #     "VALUES ('75.67.236.14/32', 'Company HQ');")

                self.db_conn.commit()
        else:
            self.db_conn = sqlite3.connect(self.db_filename)

    def store_cidr(self, cidr):
        self.db_conn.execute(
            "insert into registeredCidrs " +
            " (cidr, description, location, owner, expiration)" +
            " VALUES (?, ?, ?, ?, ?);",
            (cidr.cidr, cidr.description, cidr.location, cidr.owner, cidr.expiration))
        self.db_conn.commit()

    def query_all(self):
        cidrs = []
        cur = self.db_conn.cursor()
        cur.execute("SELECT * FROM registeredCidrs;")
        self.db_conn.commit()
        recordset = cur.fetchall()
        for row in recordset:
            cidrs.append(SqliteStore.__from_cursor__(row))
        return cidrs

    def query_one(self, cidr_str):
        cur = self.db_conn.cursor()
        cur.execute("SELECT * FROM registeredCidrs WHERE cidr=?;", (cidr_str,))
        self.db_conn.commit()
        row = cur.fetchone()

        if row is None:
            return None

        return SqliteStore.__from_cursor__(row)

    @staticmethod
    def __from_cursor__(cursor):
        # id = cursor[0]
        cidr_str = cursor[1]
        description = cursor[2]
        location = cursor[3]
        owner = cursor[4]
        expiration = cursor[5]

        cidr = RegisteredCidr(cidr_str, description, owner, location, expiration)
        return cidr
