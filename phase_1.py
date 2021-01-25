import mysql.connector


class QuarantinedAgain():

    def __init__(self,user,password,host,database):
        self.cnx = mysql.connector.connect(user=user, password=password,host=host,database=database)
        self.cursor = self.cnx.cursor()   
    def Get_Fragments(self):
        query = "SELECT * FROM Frag_Table;" 
        self.cursor.execute(query)
        for (i,j,k,l) in self.cursor:
            print(i,j)
    
    def Get_Allocation(self,frag_id):
        query = "Select * FROM Allocation Where Frag_Id = " + str(frag_id) + ";"
        self.cursor.execute(query)
        for i in self.cursor:
            # print(i)
            print("Frag_Id = " + i[0] + " allocated on site : " +i[1])

