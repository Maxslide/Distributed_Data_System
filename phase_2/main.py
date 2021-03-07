from typing import NoReturn
import sqlparse
import mysql.connector
from mysql.connector.constants import ServerFlag
import pprint

class HomeDatabase():

    def __init__(self):
        self.home = mysql.connector.connect(user="Maxslide",password = "iiit123",host = "localhost",database = "QuarantinedAgain")
        self.cursor = self.home.cursor()

    def Create_temp_table(self, table_name, final_output, columns):
        # Need to decide how to name the joins etc
        table_name = "temp_something"
        # complete the syntax for create table
        creat_table = "CREATE TABLE "+table_name+" "
        self.cursor.execute(creat_table)
        for i in final_output:
            # complete as required by modifying the function a bit, we need to know the column names also which i dont think comes in the execute query output
            # need to figure this out
            insert_into_table = "INSERT INTO " +table_name+" VALUES"
        # At this point we have a temporary table created 
        return
    def execute_query(self,query):
        self.cursor.execute(query)
        output_list = []
        for i in self.cursor:
            output_list.append(i)
        return output_list

obj = HomeDatabase()
# obj.execute_query('Select * From Frag_Table')

query = "SELECT A,B,C FROM t1,t2,t3 WHERE t1.id == t2.id and t2.name == t3.name and (t1.col > 5 or t3.city == 'Bangalore') and t2.name == 'Manas'"

# conevrt this into query tree

parsed_query = sqlparse.parse(sqlparse.format(query,keyword_case='upper'))[0].tokens

token_list = []
for i in parsed_query:
    if not i.is_whitespace:
        try :
            token = []
            for j in i.get_identifiers():
                token.append(j)
            token_list.append(token)
        except:
            token_list.append(i)

# for i in token_list:
#     print(str(i))
    # if(type(i) == list):
    #     for j in i:
    #         print(j)


# Where -> Joins, Condition
# [Select, From, Join, Join]
# [t1,t2,t3, join(t1,t2,condition),join(t3,codition), Condition(table_name,condition), Condition(table_name,condition)...., SELECT(Columns)]
hash_table = {}
tree_nodes = []
edges = []
def get_table_names(token_list):
    for i in range(len(token_list)):
        if str(token_list[i]) == 'FROM':
            for j in token_list[i+1]:
                hash_table[str(j)] = len(tree_nodes)
                tree_nodes.append({
                    'Key' : 'Table',
                    'Value' : str(j),
                    'Condition' : []
                })
            break
def check_join(token) :
    if ('==' in token and '.' in token):
        conditions = token.strip().split('==')
        join = []
        for i in conditions:
            check = i.strip().split('.')
            # print(check)
            try:
                table = hash_table[check[0].strip()]
                table = check[0].strip()
                column = check[1].strip()
                join.append([table,column])
            except:
                pass
        # print(join)
        if len(join) == 2:
            return join
    return []
def get_conditions(token_list):
    # join = []
    others = []
    # if len(hash_table) > 1:
        # we need to get the join conditions now, this can happen from the where wala clause:
    for i in token_list:
        if 'WHERE' in str(i):
            i = str(i)
            _,condition = i.strip().split('WHERE')
            condition = condition.strip()
            where_tokens = condition.split('AND')
            for j in where_tokens:
                join = check_join(j.strip())
                if len(join) == 2:
                    # print('here')
                    flag = 0
                    for l in range(len(tree_nodes)):
                        k = tree_nodes[l]
                        if(k['Key'] == 'Join'):
                            for j in k['Condition']:
                                print(j,join)
                                if(join[0][0] == j[0] or join[1][0] == j[0]):
                                    flag = 1
                                    edges.append([len(tree_nodes),l])
                                    if (join[0][0] != j[0]):
                                        edges.append([len(tree_nodes),hash_table[join[0][0]]])
                                    else:
                                        edges.append([len(tree_nodes),hash_table[join[1][0]]])
                                    tree_nodes.append({
                                        'Key' : 'Join',
                                        'Value' : 'To_Another_Join',
                                        'Condition' : join
                                    })
                        if flag == 1:
                            break
                    if flag == 0:
                        # print(join)
                        edges.append([len(tree_nodes),hash_table[join[0][0]]])
                        edges.append([len(tree_nodes),hash_table[join[1][0]]])
                        tree_nodes.append({
                            'Key' : 'Join',
                            'Value' : str(join[0][0]) + '_' + str(join[1][0]),
                            'Condition' : join
                        })
                else:
                    others.append(j.strip())  
            break
    return others

def get_Project(token_list):
    for l in range(len(token_list)):
        i = token_list[l]
        if str(i) == 'SELECT':
            project_list = []
            for j in token_list[l+1]:
                project_list.append(str(j))
            return project_list
    
get_table_names(token_list)
conditions_left = get_conditions(token_list)
edges.append([len(tree_nodes) -1 , len(tree_nodes)])
tree_nodes.append({
    'Key' : 'Select',
    'Condition' : conditions_left
})
edges.append([len(tree_nodes) -1 , len(tree_nodes)])

tree_nodes.append({
    'Key' : 'Project',
    'Condition' : get_Project(token_list)
})

# pprint.pprint(tree_nodes)
for i in range(len(tree_nodes)):
    print(str(i),"->",tree_nodes[i])
print(edges)


#  Need to move the select statements down

delete_list = []
for i in tree_nodes:
    if i['Key'] == 'Select':
        for j in range(len(i['Condition'])):
            if 'OR' in i['Condition'][j]:
                continue
            # operator_list = ['==','>=','<=','>','<']
            tok = i['Condition'][j].strip().split()
            # print(tok)
            for k in tok:
                if('.' in k):
                    try :
                        table,column = k.strip().split('.')
                        ind = hash_table[table]
                        tree_nodes[ind]['Condition'].append(i['Condition'][j])
                        delete_list.append(j)
                    except:
                        print('Incorrect Query')
                        exit()
        break

for i in range(len(tree_nodes)):
    if(tree_nodes[i]['Key'] == 'Select'):
        for j in delete_list:
            del tree_nodes[i]['Condition'][j]
        break

print('-----------------------------------------------------------------------------------------')

pprint.pprint(tree_nodes)


# print(hash_table)
# for i in range(len(token_list)):
    
#     if(token_list[i] == 'WHERE'):
#         pass 
#     if(type(token_list[i+1]) == list):
#         tree_nodes.append(
#             {
#                 'Key' : token_list[i],
#                 'Identifiers' : token_list[i+1],
#                 'Condition' : '' 
#             }
#         )
    


# Create an array of dictionary
# Format could be
# {
#     'Key' : 'Select'
#     'Identifiers' : [A,B,C],
#     'Condition' : //Yet to decide,
# }
# print(token_list[-1].value())

