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
        query = "Select * FROM Tables Where Table_Id = " + str(frag_id) + ";"
        self.cursor.execute(query)
        for i in self.cursor:
            # print(i)
            print("Frag_Id = " + str(i[0]) + " allocated on site : " +str(i[1]))
    def Get_Table(self,table_name):
        query = "Select Table_name,Frag_Type, Frag_Id,Frag_Name,Frag_Conditon FROM Tables,Frag_Table Where Tables.Table_Id = Frag_Table.Table_Id AND Table_Name = " + str(table_name) + ";"
        self.cursor.execute(query)
        print("(Table_name,Frag_Type, Frag_Id,Frag_Name,Frag_Conditon)")
        for i in self.cursor:
            print(i)


obj = QuarantinedAgain("Maxslide", "iiit123","127.0.0.1","QuarantinedAgain")
# obj.Get_Fragments()

print("Input table name : ")

frag_id = input()

obj.Get_Allocation(frag_id)

