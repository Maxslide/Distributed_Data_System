import mysql.connector


class QuarantinedAgain():

    def __init__(self,user,password,host,database):
        self.cnx = mysql.connector.connect(user=user, password=password,host=host,database=database)
        self.cursor = self.cnx.cursor()   
    def Get_Fragments(self):
        query = "SELECT * FROM Frag_Table;" 
        self.cursor.execute(query)
        print("id Fragment_name Condition")
        for (i,j,k,l) in self.cursor:
            print(i,j,k)
    
    def Get_Allocation(self,frag_id):
        query = "Select * FROM Allocation Where Frag_Id = " + str(frag_id) + ";"
        self.cursor.execute(query)
        for i in self.cursor:
            # print(i)
            print("Frag_Id = " + str(i[0]) + " allocated on site : " +str(i[1]))


obj = QuarantinedAgain("Maxslide", "iiit123","127.0.0.1","QuarantinedAgain")
obj.Get_Fragments()

print("Enter Fragment id for which the Allocation schema is required : ")

frag_id = input()

obj.Get_Allocation(frag_id)

