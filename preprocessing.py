import pandas as pd
import psycopg2
from psycopg2 import Error
import annotation

class Authentication:
    def __init__(self, db, user, passcode, host = 'localhost', port =5432):
        self.database = db
        self.username = user
        self.password = passcode
        self.host = host
        self.port = port

def connect_sql(login):
    try:
        connection = psycopg2.connect(user = login.username,
                                  password = login.password,
                                  host = login.host,
                                  port = login.port,
                                 database= login.database)

        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")
        return True 

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
        return False

def connect_pandas_sql(login):
    
    POSTGRES_ADDRESS = login.host
    POSTGRES_PORT = login.port
    POSTGRES_USERNAME = login.username
    POSTGRES_PASSWORD = login.password
    POSTGRES_DBNAME = login.database
    postgres_str = ('postgresql://{username}:{password}@{ipaddress}:{port}/{dbname}'.format(username=POSTGRES_USERNAME,
                                                                                            password=POSTGRES_PASSWORD, ipaddress=POSTGRES_ADDRESS, port=POSTGRES_PORT, dbname=POSTGRES_DBNAME))
    return postgres_str

def read_query(query,login):
    query_explain = "explain " + query.replace("\n", " ")
    try:
        connection = psycopg2.connect(user = login.username,
                                  password = login.password,
                                  host = login.host,
                                  port = login.port,
                                 database= login.database)

        cursor = connection.cursor()
        cursor.execute(query_explain)
        qep = cursor.fetchall()
        query_plan  = annotation.store_qep_in_tree(qep)
        string_plan = annotation.print_steps(query_plan)
        


    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
        return False


    return string_plan, query_plan 