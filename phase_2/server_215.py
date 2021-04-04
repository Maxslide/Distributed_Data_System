# python3 -m Pyro4.naming
# Main site
import Pyro4
import sqlparse
import mysql.connector
from mysql.connector.constants import ServerFlag

@Pyro4.expose
class HomeDatabase():

    def __init__(self):
        self.home = mysql.connector.connect(
            user="Maxslide", password="iiit123", host="localhost", database="QuarantinedAgain")
        self.cursor = self.home.cursor()

    def Create_temp_table(self, table_name, columns):
        # Need to decide how to name the joins etc
        # complete the syntax for create table
        creat_table = "CREATE TABLE "+table_name+" ( "
        for i in columns[:-1]:
            creat_table += i + " ,"
        creat_table += columns[-1] + " );"
        print(creat_table)
        self.cursor.execute(creat_table)
        # At this point we have a temporary table created
        return

    def insert_to_table(self,table_name,values):

        insert = "INSERT INTO "+ table_name+ " VALUES ( "
        for i in values[:-1]:
            insert += values + ", "
        insert += values[-1] + " );"
        print(insert)
        self.cursor.execute(insert)

    def execute_query(self, query):
        self.cursor.execute(query)
        # print(self.cursor)
        # output_list = []
        # for i in self.cursor:
        #     output_list.append(i)
        # return output_list
    
    def check_connection(self):
        print("215 connection")
        return "Connected successfully"


obj = HomeDatabase()    
print(obj.check_connection(),"self")
# Pyro4.Daemon.serveSimple({obj : 'Graph'},host='10.3.5.215', port=9090)
Pyro4.Daemon.serveSimple({obj : 'Graph'},host='127.0.0.1', port=9090, ns=False)
print("Loaded")
