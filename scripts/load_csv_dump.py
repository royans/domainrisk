import pandas as pd
import mysql.connector
import os

# CSV file path
csv_file = 'top10000domains.csv'
csv_file = 'top10milliondomains.csv'

# Get database credentials from environment variables
db_user = os.environ.get('DBUSER')
db_password = os.environ.get('DBPASS')
db_config = {
    'user': db_user,
    'password': db_password,
    'host': 'localhost',
    'database': 'domainrisk'
}

# Create a MySQL connection
cnx = mysql.connector.connect(**db_config)
cursor = cnx.cursor()

i=0
ii=0

 # Prepare the insert query
check_last_rank = "select max(rank) from rankdb"
cursor.execute( check_last_rank)
data = cursor.fetchall()
if len(data)>0:
    skip_rank = data[0][0]
else:
    skip_rank = 0

print("====================")
print(skip_rank)
print("====================")


chunks = pd.read_csv(csv_file, chunksize=1000)
print("Starting the load...")
# Insert data into the database
for chunk in chunks:
  chunk.columns = ['rank', 'domain', 'pagerank']
  for index, row in chunk.iterrows():
    i=i+1
    ii=ii+1
    if row['rank'] > skip_rank:
        sql = "INSERT IGNORE INTO rankdb (rank, domain, pagerank) VALUES (%s, %s, %s)"
        values = (row['rank'], row['domain'], row['pagerank'])
        cursor.execute(sql, values)
        if i > 10000:
            i=0
            cnx.commit()
            print ("commiting - ")
            print (ii)

sql = "delete from rankdb where domain like '%doubleclick.net%'"
cursor.execute(sql)
# Commit changes to the database
cnx.commit()

# Close the connection
cursor.close()
cnx.close()

print("Data loaded successfully!")
