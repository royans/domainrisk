import pandas as pd
import mysql.connector
import os

# CSV file path
csv_file = 'top10milliondomains.csv'

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv(csv_file)

# Rename columns to match database schema
df.columns = ['rank', 'domain', 'pagerank']

# Get database credentials from environment variables
db_user = os.environ.get('DBUSER')
db_password = os.environ.get('DBPASS')

# Database connection details (replace placeholders with your host and database name)
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

# Insert data into the database
for index, row in df.iterrows():
    i=i+1
    sql = "INSERT IGNORE INTO rankdb (rank, domain, pagerank) VALUES (%s, %s, %s)"
    values = (row['rank'], row['domain'], row['pagerank'])
    cursor.execute(sql, values)
    if i > 100000:
        i=0
        cnx.commit()
        print ("commiting")

# Commit changes to the database
cnx.commit()

# Close the connection
cursor.close()
cnx.close()

print("Data loaded successfully!")
