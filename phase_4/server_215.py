# python3 -m Pyro4.naming
# Main site
import Pyro4
# import sqlparse
import mysql.connector
from mysql.connector.constants import ServerFlag


@Pyro4.expose
class HomeDatabase():

    def __init__(self):
        self.home = mysql.connector.connect(
            user="Maxslide", password="iiit123", host="localhost", database="QuarantinedAgain")
        self.cursor = self.home.cursor()

    def two_phase_message(self,message,query):
        ready_state = 1
        print(message,query)
        if(message == "prepare"):
            if ready_state == 0:
                print("abort")
                return "vote-abort"
            else :
                print("ready")
                try :
                    for i in query:
                        self.cursor.execute(i)
                    return "vote-commit"
                except :
                    return "vote-abbort"
        elif(message == "COMMIT"):
            self.home.commit()
            print("COMMITED")
            return ("Site 215 commited successfully")
        else:
            self.home.rollback()
            print("ABORTED")
            return ("Site 215 Aborted")


    def check_connection(self):
        print("215 connection")
        return "Connected successfully 215"


obj = HomeDatabase()
print(obj.check_connection(), "self")
Pyro4.Daemon.serveSimple(
    {obj: 'Graph'}, host='10.3.5.215', port=9090, ns=False)
# Pyro4.Daemon.serveSimple({obj : 'Graph'},host='127.0.0.1', port=9090, ns=False)
