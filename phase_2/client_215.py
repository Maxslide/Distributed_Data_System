from os import curdir
import Pyro4
from mysql.connector import cursor
import sqlparse
import mysql.connector
from mysql.connector.constants import ServerFlag
import base64



@Pyro4.expose
class Client():

    def __init__(self, link1, link2):
        self.site_214 = Pyro4.Proxy(link1)
        self.site_213 = Pyro4.Proxy(link2)

    def execute_site_214(self,query):
        self.site_214.execute_query(query)

    def execute_site_213(self,query):
        self.site_213.execute_query(query)
        

link1 = "PYRO:Graph_1@10.3.5.214:9090"
link2 = "PYRO:Graph_1@10.3.5.213:9090"
obj = Client(link1,link2)
print(obj.site_213.check_connection())
print(obj.site_214.check_connection())


# while (1):
#     try:
#         a = input()
#         # print(a)
#         b = a.split()

#         if b[0] == 'add_graph':
#             casetester.add_graph(b[1],int(b[2]))

#         if b[0] == 'add_edge':
#             casetester.add_edge(b[1],int(b[2]),int(b[3]),int(b[4]))

#         if b[0] == 'get_mst':
#             print(casetester.get_mst(b[1]))
#     except:
#         break
