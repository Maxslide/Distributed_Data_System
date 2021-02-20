import sqlparse

query = "SELECT A,B,C FROM t1,t2,t3 WHERE t1.id == t2.id and t2.name = t3.name and (t1.col > 5 or t3.city == 'Bangalore')"

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

# print(token_list[-1].value())
