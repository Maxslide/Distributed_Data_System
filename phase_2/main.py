from typing import NoReturn
import sqlparse
import mysql.connector
from mysql.connector.constants import ServerFlag
import pprint


class HomeDatabase():

    def __init__(self):
        self.home = mysql.connector.connect(
            user="Maxslide", password="iiit123", host="localhost", database="QuarantinedAgain")
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
            insert_into_table = "INSERT INTO " + table_name+" VALUES"
        # At this point we have a temporary table created
        return

    def execute_query(self, query):
        self.cursor.execute(query)
        # print(self.cursor)
        output_list = []
        for i in self.cursor:
            output_list.append(i)
        return output_list


obj = HomeDatabase()
# obj.execute_query('Select * From Frag_Table')
print("Enter Query : ")
query = input()
query = query.strip(';')
# conevrt this into query tree


parsed_query = sqlparse.parse(sqlparse.format(
    query, keyword_case='upper'))[0].tokens
print('\n\n\nPARSED QUERY : ')
print(sqlparse.format(query, reindent=True, keyword_case='upper'))
print('\n\n-----------------------------------------------------------------------------------------\n\n')

print("Note : In all of the query tree below, the root node will be the highest numbered node, the tree is built using bottom up approach. \n Please node the Condition key in each of the node (which is a dictionary), defines the selection statements for that node.")
print("note that the select statements which are pushed down the tree (in our case up the indexing, since built via bottom up), will go into the list of this condition.")
print("Refer to a detailed example of a big query mentioned in the pdf.\n\n")

token_list = []
for i in parsed_query:
    if not i.is_whitespace:
        try:
            token = []
            for j in i.get_identifiers():
                token.append(j)
            token_list.append(token)
        except:
            token_list.append(i)
# pprint.pprint(token_list)
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
global_where_tokens = []


def get_table_names(token_list):
    for i in range(len(token_list)):
        if str(token_list[i]) == 'FROM':
            for j in token_list[i+1]:
                hash_table[str(j)] = len(tree_nodes)
                tree_nodes.append({
                    'Key': 'Table',
                    'Value': str(j),
                    'Condition': []
                })
            break


def check_join(token):
    if ('=' in token and '.' in token):
        conditions = token.strip().split('=')
        join = []
        for i in conditions:
            check = i.strip().split('.')
            # print(check)
            try:
                table = hash_table[check[0].strip()]
                table = check[0].strip()
                column = check[1].strip()
                join.append([table, column])
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
            _, condition = i.strip().split('WHERE')
            condition = condition.strip()
            where_tokens = condition.split('AND')
            # global_where_tokens = where_tokens
            for bleh in where_tokens:
                global_where_tokens.append(bleh)
            for j in where_tokens:
                join = check_join(j.strip())
                if len(join) == 2:
                    # print('here')
                    flag = 0
                    for l in range(len(tree_nodes)):
                        k = tree_nodes[l]
                        if(k['Key'] == 'Join'):
                            for j in k['Condition']:
                                # print(j,join)
                                if(join[0][0] == j[0] or join[1][0] == j[0]):
                                    flag = 1
                                    edges.append([len(tree_nodes), l])
                                    if (join[0][0] != j[0]):
                                        edges.append(
                                            [len(tree_nodes), hash_table[join[0][0]]])
                                    else:
                                        edges.append(
                                            [len(tree_nodes), hash_table[join[1][0]]])
                                    tree_nodes.append({
                                        'Key': 'Join',
                                        'Value': str(join[0][0]) + '_' + str(join[1][0]),
                                        'Condition': join
                                    })
                        if flag == 1:
                            break
                    if flag == 0:
                        # print(join)
                        edges.append([len(tree_nodes), hash_table[join[0][0]]])
                        edges.append([len(tree_nodes), hash_table[join[1][0]]])
                        tree_nodes.append({
                            'Key': 'Join',
                            'Value': str(join[0][0]) + '_' + str(join[1][0]),
                            'Condition': join
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
            if type(token_list[l+1]) != list:
                project_list.append(str(token_list[l+1]))
                return project_list
            else:
                for j in token_list[l+1]:
                    project_list.append(str(j))
                return project_list


get_table_names(token_list)
join_flag = len(tree_nodes)
conditions_left = get_conditions(token_list)
edges.append([len(tree_nodes) - 1, len(tree_nodes)])
tree_nodes.append({
    'Key': 'Select',
    'Condition': conditions_left
})
flag = 0
# print(token_list)
i = 0
while i < len(token_list):
    # print(token_list[i].get_type())
    if (flag == 1 and i + 1 < len(token_list)) or 'GROUP BY' in str(token_list[i]) or 'HAVING' in str(token_list[i]):
        condition = []
        if type(token_list[i+1]) != list:
            condition.append(str(token_list[i+1]))
        else:
            for j in token_list[i+1]:
                condition.append(str(j))
        edges.append([len(tree_nodes) - 1, len(tree_nodes)])
        tree_nodes.append({
            'Key': str(token_list[i]),
            'Condition': condition
        })
        i = i+1
    try:
        # print(token_list[i])
        if 'WHERE' in str(token_list[i]):
            flag = 1
    except:
        pass
    i += 1
edges.append([len(tree_nodes) - 1, len(tree_nodes)])

tree_nodes.append({
    'Key': 'Project',
    'Condition': get_Project(token_list)
})

# pprint.pprint(tree_nodes)
print('Decomposed Query Tree\n')
for i in range(len(tree_nodes)):
    print(str(i), "->", tree_nodes[i])

print('Edge List -> ')

print(edges)


#  Need to move the select statements down

delete_list = []
for i in tree_nodes:
    if i['Key'] == 'Select':
        for j in range(len(i['Condition'])):
            if 'OR' in i['Condition'][j]:
                continue
            # operator_list = ['=','>=','<=','>','<']
            tok = i['Condition'][j].strip().split()
            # print(tok)
            for k in tok:
                if('.' in k):
                    try:
                        table, column = k.strip().split('.')
                        ind = hash_table[table]
                        tree_nodes[ind]['Condition'].append(i['Condition'][j])
                        delete_list.append(i['Condition'][j])
                    except:
                        print('Incorrect Query')
                        exit()
        break

for i in range(len(tree_nodes)):
    if(tree_nodes[i]['Key'] == 'Select'):
        for j in delete_list:
            tree_nodes[i]['Condition'].remove(j)
        break

print('\n\n-----------------------------------------------------------------------------------------\n\n')

print('Decomposed Query Tree with Heuristic optimisations\n')

for i in range(len(tree_nodes)):
    print(str(i), "->", tree_nodes[i])

print('Edge List -> ')

print(edges)

# Rewritten Query tree

# Localisation
# {
#     'Key'
#     'Condition'
#     'Value'
# }


# [{'Condition': [], 'Key': 'Table', 'Value': 't1'},
#  {'Condition': ["t2.name == 'Manas'"], 'Key': 'Table', 'Value': 't2'},
#  {'Condition': [], 'Key': 'Table', 'Value': 't3'},
#  {'Condition': [['t1', 'id'], ['t2', 'id']], 'Key': 'Join', 'Value': 't1_t2'},
#  {'Condition': [['t2', 'name'], ['t3', 'name']],
#   'Key': 'Join',
#   'Value': 'To_Another_Join'},
#  {'Condition': ["(t1.col > 5 OR t3.city == 'Bangalore')"], 'Key': 'Select'},
#  {'Condition': ['A', 'B', 'C'], 'Key': 'Project'}]

# +----------+------------+------------+-----------+----------+---------+-----------+------------------------+----------+
# | Table_Id | Table_Name | Columns_No | Frag_Type | Frags_No | Frag_Id | Frag_Name | Frag_Condition         | Table_Id |
# +----------+------------+------------+-----------+----------+---------+-----------+------------------------+----------+
# |        3 | Course     |          4 | HF        |        3 |       7 | Course1   |  Course_Type = "CSE"   |        3 |
# |        3 | Course     |          4 | HF        |        3 |       8 | Course2   |  Course_Type = "ECE"   |        3 |
# |        3 | Course     |          4 | HF        |        3 |       9 | Course3   |  Course_Type = "HSME"  |        3 |
# +----------+------------+------------+-----------+----------+---------+-----------+------------------------+----------+

if(join_flag == 1):
    pass

localised_tree_nodes = []
localised_edges = []


def Check_Anti(value, check_val, op, op_check):
    if op == '=':
        # print(check_val, value)
        try:
            v = float(value)
            if op_check == '=':
                if check_val == value:
                    return 0
                else:
                    return 1
            else:
                mini = -1000000000
                maxi = 1000000000
                if op_check == '>':
                    mini = float(check_val) + 1
                elif op_check == '>=':
                    mini = float(check_val)
                elif op_check == '<':
                    maxi = float(check_val) - 1
                else:
                    maxi = float(check_val)
                if (v >= mini and v <= maxi):
                    return 0
                else:
                    return 1

        except:
            # print("Here in the except block",check_val.strip('"').strip('"'), value.strip('"').strip('"'))
            if check_val.strip('"').strip("'") == value.strip('"').strip("'"):
                # print("CHECKED HERE")
                return 0
            else:
                # print("Check here for anti true")
                return 1
    else:
        mini_v = -1000000000
        maxi_v = 1000000000
        if op == '>':
            mini_v = float(value) + 1
        elif op == '>=':
            mini_v = float(value)
        elif op == '<':
            maxi_v = float(value) - 1
        else:
            maxi_v = float(value)

        mini = -1000000000
        maxi = 1000000000
        if op_check == '>':
            mini = float(check_val) + 1
        elif op_check == '>=':
            mini = float(check_val)
        elif op_check == '<':
            maxi = float(check_val) - 1
        elif op_check == '<=':
            maxi = float(check_val)
        else:
            mini = float(check_val)
            maxi = float(check_val)

        if(maxi_v < mini or mini_v > maxi):
            return 1
        else:
            return 0


project_columns = []
for i in tree_nodes:
    if i['Key'] == 'Project':
        project_columns = i['Condition']

# print(project_columns)


def Assign_frag():
    hash_frag = {}
    for i in tree_nodes:
        if i['Key'] == 'Table':
            # print(i['Value'])
            hash_frag[i['Value']] = []
            frag_list = obj.execute_query(
                "select * From Tables , Frag_Table Where Tables.Table_Id = Frag_Table.Table_Id AND Table_Name = '" + i['Value'].strip()+"';")
            for j in frag_list:
                frag_type = j[3]
                conditions = j[7]
                # print(frag_type,conditions)
                flag = 0
                if frag_type == 'HF':
                    conditions = conditions.split('AND')
                    for k in conditions:
                        l = k.split('OR')
                        op_list = ['>=', '<=', '>', '<', '=']
                        or_flag_anti = 0
                        for con in l:
                            pre_flag = 0
                            op = ""
                            for operator in op_list:
                                if con.find(operator) != -1:
                                    op = operator
                                    break
                            column, value = con.split(op)
                            column = column.strip()
                            value = value.strip()
                            # print("HERE", i['Condition'])
                            col_check_flag = 1
                            for check_con in i['Condition']:
                                check = check_con.split('.')[1].strip()
                                # print("Check_Cond", check)
                                op_check = ""
                                for operator in op_list:
                                    if check.find(operator) != -1:
                                        op_check = operator
                                        break
                                check_col, check_val = check.split(op_check)
                                check_col = check_col.strip()
                                check_val = check_val.strip()
                                if check_col == column:
                                    # print("Equal_Column_Check ",column,value,check_val)
                                    v = Check_Anti(
                                        value, check_val, op, op_check)
                                    if v == 1:
                                        pre_flag = 1
                            # print("Checking pre flag -> -> ", con, pre_flag, i['Condition'])
                            or_flag_anti += pre_flag
                        # print("checking or flag", k, or_flag_anti)
                        # sum of or flagt
                        if or_flag_anti == len(l):
                            flag = 1
                    if flag == 0:
                        hash_frag[i['Value']].append(len(localised_tree_nodes))
                        localised_tree_nodes.append({
                            'Key': 'Table_Fragment',
                            'Value': j[6],
                            'Table_Name': i['Value'],
                            'Condition': i['Condition']
                        })

                elif frag_type == 'DHF':
                    pass
                else:
                    columns_vf = conditions.strip().split()
                    flag = 1
                    for col in project_columns:
                        if col in columns_vf:
                            flag = 0
                    if flag == 0:
                        hash_frag[i['Value']].append(len(localised_tree_nodes))
                        localised_tree_nodes.append({
                            'Key': 'Table_Fragment',
                            'Value': j[6],
                            'Table_Name': i['Value'],
                            'Condition': i['Condition']
                        })

    to_remove = []
    for i in tree_nodes:
        if i['Key'] == 'Table':
            # print(i['Value'])
            frag_list = obj.execute_query(
                "select * From Tables , Frag_Table Where Tables.Table_Id = Frag_Table.Table_Id AND Table_Name = '" + i['Value'].strip()+"';")
            union_list = []
            union_con = set()
            for j in frag_list:
                frag_type = j[3]
                conditions = j[7]
                # print(frag_type,conditions)
                flag = 0
                if frag_type == 'DHF':
                    _, _, parent = conditions.strip().split()
                    p_flag = 0
                    # print("JOIN PARENT DHF -> ",parent)
                    for k in range(len(localised_tree_nodes)):
                        # print(localised_tree_nodes[k])
                        if(localised_tree_nodes[k]['Value'] == parent):
                            p_flag = 1
                            hash_frag[i['Value']].append(
                                len(localised_tree_nodes))
                            localised_tree_nodes.append({
                                'Key': 'Table_Fragment',
                                'Value': j[6],
                                'Table_Name': i['Value'],
                                'Condition': i['Condition']
                            })
                            localised_edges.append(
                                [len(localised_tree_nodes), len(localised_tree_nodes) - 1])
                            localised_edges.append(
                                [len(localised_tree_nodes), k])
                            union_list.append(len(localised_tree_nodes))
                            union_con.add(
                                localised_tree_nodes[k]['Table_Name'])
                            union_con.add(i['Value'])
                            j_con = ""
                            value_join = ""
                            # print("Global where tokens",global_where_tokens)

                            for tok in global_where_tokens:
                                joins = check_join(tok)
                                if(len(joins) == 2):
                                    t1 = joins[0][0]
                                    t2 = joins[1][0]
                                    # print("HERE PRINTING -> ",i['Value'],localised_tree_nodes[k]['Table_Name'])
                                    if((t1 == i['Value'] or t2 == i['Value']) and (t2 == localised_tree_nodes[k]['Table_Name'] or t1 == localised_tree_nodes[k]['Table_Name'])):
                                        to_remove.append(tok)
                                        j_con = localised_tree_nodes[k]['Value'] + "."
                                        value_join = localised_tree_nodes[k]['Value'] + "_" + j[6]
                                        if(localised_tree_nodes[k]['Table_Name'] == t1):
                                            j_con += joins[0][1]
                                        else:
                                            j_con += joins[1][1]
                                        j_con += " = " + j[6] + "."
                                        if(i['Value'] == t1):
                                            j_con += joins[0][1]
                                        else:
                                            j_con += joins[1][1]
                                        break

                            localised_tree_nodes.append({
                                'Key': 'Join',
                                'Value': value_join,
                                'Condition': j_con,
                                'Union_Con': []
                            })
                    if(p_flag == 0):
                        hash_frag[i['Value']].append(len(localised_tree_nodes))
                        localised_tree_nodes.append({
                            'Key': 'Table_Fragment',
                            'Value': j[6],
                            'Table_Name': i['Value'],
                            'Condition': i['Condition']
                        })

                else:
                    if(len(union_list) != 0):
                        for un in union_list:
                            localised_edges.append([len(localised_edges), un])
                        localised_tree_nodes.append({
                            'Key': 'Union',
                            'Value': "",
                            'Condition': list(union_con)
                        })
                        union_list = []
                        union_con = set()

            if(len(union_list) != 0):
                for un in union_list:
                    localised_edges.append([len(localised_tree_nodes), un])
                localised_tree_nodes.append({
                    'Key': 'Union',
                    'Value': "",
                    'Condition': list(union_con),
                })
                union_list = []
                union_con = set()

    # print(hash_frag)
    for i in global_where_tokens:
        if i not in to_remove:
            joins = check_join(i)
            if len(joins) == 2:
                # print('Printing the join condition', i)
                t1 = -1
                t2 = -1
                join_con = []
                for k in range(len(localised_tree_nodes)):
                    if localised_tree_nodes[k]['Key'] == 'Union':
                        if joins[0][0] in localised_tree_nodes[k]['Condition']:
                            t1 = k
                            for loc in localised_tree_nodes[k]['Condition']:
                                join_con.append(loc)
                        if joins[1][0] in localised_tree_nodes[k]['Condition']:
                            t2 = k
                            for loc in localised_tree_nodes[k]['Condition']:
                                join_con.append(loc)
                    if localised_tree_nodes[k]['Key'] == 'Join':
                        if joins[0][0] in localised_tree_nodes[k]['Union_Con']:
                            t1 = k
                            for loc in localised_tree_nodes[k]['Union_Con']:
                                join_con.append(loc)
                        if joins[1][0] in localised_tree_nodes[k]['Union_Con']:
                            t2 = k
                            for loc in localised_tree_nodes[k]['Union_Con']:
                                join_con.append(loc)
                if(t1 == -1):
                    condition_tab = []
                    join_con.append(joins[0][0])
                    for tab in tree_nodes:
                        if tab['Key'] == 'Table' and tab['Value'] == joins[0][0]:
                            condition_tab = tab['Condition']
                            break
                    for k in hash_frag[joins[0][0]]:
                        localised_edges.append([len(localised_tree_nodes), k])
                    t1 = len(localised_tree_nodes)
                    localised_tree_nodes.append({
                        'Key': 'Union_Frag',
                        'Value': "",
                        'Condition': condition_tab
                    })
                if(t2 == -1):
                    condition_tab = []
                    join_con.append(joins[1][0])
                    for tab in tree_nodes:
                        if tab['Key'] == 'Table' and tab['Value'] == joins[1][0]:
                            condition_tab = tab['Condition']
                            break
                    for k in hash_frag[joins[1][0]]:
                        localised_edges.append([len(localised_tree_nodes), k])
                    t2 = len(localised_tree_nodes)
                    localised_tree_nodes.append({
                        'Key': 'Union_Frag',
                        'Value': "",
                        'Condition': condition_tab
                    })
                localised_edges.append([len(localised_tree_nodes), t1])
                localised_edges.append([len(localised_tree_nodes), t2])
                localised_tree_nodes.append({
                    'Key': 'Join',
                    'Value': joins[0][0] + '_' + joins[1][0],
                    'Condition': i,
                    'Union_Con': join_con
                })
    return


Assign_frag()
flag = 0
if(join_flag == 1):
    for i in range(len(tree_nodes)):
        localised_edges.append([i,len(tree_nodes)])
    
    localised_tree_nodes.append({
        'Key': 'Union_Frag',
        'Value': "",
        'Condition': []
    })

for i in tree_nodes:
    if i['Key'] == 'Select' or flag == 1:
        flag = 1
        localised_edges.append(
            [len(localised_tree_nodes), len(localised_tree_nodes) - 1])
        localised_tree_nodes.append(i)
print('\n\n-----------------------------------------------------------------------------------------\n\n')

print('Final Optimised Localised Query Tree\n')

for i in range(len(localised_tree_nodes)):
    print(str(i), "->", localised_tree_nodes[i])

print('Edge List -> ')
print(localised_edges)


# Select reserve_id,name,city,price,sum(price) from Room, Guest, Reserve Where Room.reserve_id = Reserve.reserve_id and Room.reserve_id = Guest.reserve_id and Room.city = 'Mumbai' and Guest.guest_id < 20 and Room.reserve_id > 2 Group by name,price Having price > 3
