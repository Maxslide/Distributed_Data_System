import sqlparse

query = "SELECT A,B,C FROM t1,t2,t3 WHERE t1.id == t2.id and t2.name == t3.name and (t1.col > 5 or t3.city == 'Bangalore')"

# conevrt this into query tree

parsed_query = sqlparse.parse(query)[0].tokens

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

for i in token_list:
    print(i)
    # if(type(i) == list):
    #     for j in i:
    #         print(j)


#  Where -> Joins, Condition
# [Select, From, Join, Join]
# [t1,t2,t3, join(t1,t2,condition),join(t3,codition), Condition(table_name,condition), Condition(table_name,condition)...., SELECT(Columns)]

tree_nodes = []
for i in range(len(token_list)):
    
    if(token_list[i] == 'WHERE'):
        pass 
    if(type(token_list[i+1]) == list):
        tree_nodes.append(
            {
                'Key' : token_list[i],
                'Identifiers' : token_list[i+1],
                'Condition' : '' 
            }
        )
    


# Create an array of dictionary
# Format could be
# {
#     'Key' : 'Select'
#     'Identifiers' : [A,B,C],
#     'Condition' : //Yet to decide,
# }
# print(token_list[-1].value())

