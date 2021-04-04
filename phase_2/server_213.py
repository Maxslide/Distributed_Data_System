from os import curdir
import Pyro4
from mysql.connector import cursor
# import sqlparse
import mysql.connector
from mysql.connector.constants import ServerFlag
import base64

@Pyro4.expose
class Execute():

    def __init__(self, link):
        # self.ns = Pyro4.locateNS()
        self.casetester = Pyro4.Proxy(link)
        self.home = mysql.connector.connect(
            user="Maxslide", password="iiit123", host="localhost", database="QuarantinedAgain")
        self.cursor = self.home.cursor()

    def Send_Create_Table(self, Table_Name):
        self.cursor.execute("Describe " + Table_Name + ";")
        columns = []
        for i in self.cursor:
            col = ""
            for j in range(len(i)):
                if(j == 1):
                    # print(str(i[j]))
                    col += " " + str(i[j]).strip('b').strip("'")
                    break
                col += i[j]
            columns.append(col)
        print(columns)
        self.casetester.Create_temp_table(Table_Name, columns)
        self.cursor.execute("Select * From "+Table_Name+" ;")
        check = 0
        values = []
        for i in self.cursor:
            values.append(i)
            check += 1
            if check == 100:
                self.casetester.insert_to_table(Table_Name, values)
                check = 0
                values = []
        if len(values) > 0:
            self.casetester.insert_to_table(Table_Name, values)
            check = 0
            values = []
    def execute_query(self, query):
        self.cursor.execute(query)
        # print(self.cursor)
        return
    
    def check_connection(self):

        return "Connected successfully"

link = input()
obj = Execute(link)
Pyro4.Daemon.serveSimple({obj : 'Graph_1'},host='10.3.5.213', port=9090)

