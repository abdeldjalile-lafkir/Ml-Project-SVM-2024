import csv
import sys
import mysql.connector


Connection_Key = mysql.connector.connect(host="localhost",user="root",password="",database="PROJECTAIdatabase")
SQL = Connection_Key.cursor()

#all datasets for our project imported from https://www.kaggle.com/

# import scv file with 5572 sample claim it all
'''
accepted = 0
untiteld = 0
with open('spam.csv', 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)
    for row in csv_reader:
        SQL.execute("INSERT INTO dataset1 (label ,email) VALUES (%s, %s)", ( row[0], row[1]))
        accepted+=1
print(accepted)
Connection_Key.commit()
SQL.close()
Connection_Key.close()
'''


# import scv file with 83k sample claim 82k sample from it ; the others not titeled
'''
accepted = 0
untiteld = 0
large_limit = 10**9
csv.field_size_limit(large_limit)
with open('combined_data.csv', 'r' , encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)
    for row in csv_reader:
        if len(row[1])<10000:
            if(row[0] == '0' ):
                SQL.execute("INSERT INTO dataset2 (label ,email) VALUES (%s, %s)", ( 'ham', row[1]))
                accepted+=1
            elif(row[0] == '1'):
                SQL.execute("INSERT INTO dataset2 (label ,email) VALUES (%s, %s)", ('spam', row[1]))
                accepted += 1
            else:
                untiteld += 1

print(untiteld)
print(accepted)
Connection_Key.commit()
SQL.close()
Connection_Key.close()
'''



# import scv file with 172 sample claim it all

'''''
accepted = 0
untiteld = 0
with open('email_classification.csv', 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  
    for row in csv_reader:
        SQL.execute("INSERT INTO dataset3 (label, email) VALUES (%s, %s)",(row[1], row[0]))
        accepted+=1

print(untiteld)
print(accepted)
Connection_Key.commit()
'''

# import scv file with 5913 ;
'''
untiteld = 0
accepted = 0
large_limit = 10**9
csv.field_size_limit(large_limit)
with open('completeSpamAssassin.csv', 'r' , encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)
    for row in csv_reader:
        if len(row[1])<10000:
            if(row[2] == '0' ):
                SQL.execute("INSERT INTO dataset4 (label ,email) VALUES (%s, %s)", ( 'spam', row[1]))
                accepted+=1
            elif(row[2] == '1'):
                SQL.execute("INSERT INTO dataset4 (label ,email) VALUES (%s, %s)", ('spam', row[1]))
                accepted += 1
            else:
                untiteld += 1

print(untiteld)
print(accepted)
Connection_Key.commit()
SQL.close()
Connection_Key.close()
'''

# fill all 4 dataset data into my final dataset : 94k sample
'''
totaldatasetsamples=0
for k in range(1,5):
    SQL.execute(f" SELECT * From dataset{k} ")
    SQL_DATASET = SQL.fetchall()
    for row in SQL_DATASET:
        SQL.execute("INSERT INTO FINALEDATASETTABLE (LABEL ,EMAIL) VALUES (%s, %s)", (row[0], row[1]))
        totaldatasetsamples+=1


print(totaldatasetsamples)
Connection_Key.commit()
SQL.close()
Connection_Key.close()
'''

'''
hamcount=0
spamcount=0
SQL.execute(f" SELECT * From FINALEDATASETTABLE ")
SQL_DATASET = SQL.fetchall()
for row in SQL_DATASET:
    if row[0] == 'ham':
        hamcount+=1
    elif row[0] == 'spam':
        spamcount+=1
    else:
        print(row[0])

print(f"ham count : {hamcount}")
print(f"spam count : {spamcount}")
'''