import mysql.connector
import re
import os
import sys
import subprocess
from datetime import datetime
import domainrisk
import json

# Get database credentials from environment variables
db_user = os.environ.get("DBUSER")
db_password = os.environ.get("DBPASS")
db_server = os.environ.get("DBSERVER")

if db_server is None:
    db_server = "127.0.0.1"

# "host": db_server,
# Database connection details (replace placeholders with your host and database name)
config = {
    "user": db_user,
    "password": db_password,
    "host": db_server,
    "database": "domainrisk",
}

cnx = None
cursor = None

def db_start():
    global cnx, cursor
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

def db_close():
    global cnx, cursor
    cnx.commit()
    cursor.close()
    cnx.close()

def convert_date_to_datetime(date_string):
    """
    Converts a date string in dd/mm/yy format to a datetime object.

    Args:
      date_string: The date string in dd/mm/yy format.

    Returns:
      A datetime object representing the date.
    """
    try:
        # Parse the date string using strptime with the correct format
        date_object = datetime.strptime(date_string, "%Y/%m/%d")
        return date_object
    except ValueError:
        raise ValueError(f"Invalid date format: {date_string}")


def update_kv(rankdb_id,k,v):
    try:
        # Prepare the insert query
        check_kv = "select row_key, row_value from kv_store where rankdb_id = %s"
        cursor.execute(
            check_kv, (rankdb_id,)
        )
        data = cursor.fetchall()
        found = False

        for row_key, row_value in data:
            if row_key == k and row_value == v:
                found = True
                continue
            if row_key == k:
                if row_value != v:
                    update_kv = "update kv_store set row_value=%s where rankdb_id=%d"
                    cursor.execute(update_kv,(k, v[0:100],rankdb_id))
                    #cnx.commit()
                    found=True
        if found == False:
            insert_kv = "insert into kv_store (row_key,row_value, rankdb_id) values (%s,%s,%s)"
            cursor.execute(insert_kv,(k,v[0:100],rankdb_id))
            #cnx.commit()

    except ValueError as e:
        print(e)
        
# Function to insert data into the database
def updatePageRankFailTimestamp(rankdb_id):
    try:
        # Prepare the insert query
        add_domain = "update rankdb set last_checked=CURDATE() where id = %s"
        cursor.execute(
            add_domain, (rankdb_id,)
        )
        # Commit the changes
        cnx.commit()

    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")


# Function to insert data into the database
def updateIndexPage(rankdb_id, domain_data,index_page_exists):
    try:
        title=domain_data["title"]
        headers=json.dumps(domain_data["headers"],indent=2)[0:1000]
        contents=""
        content_size=len(domain_data["contents"])
        cert_expiry=domain_data["not_after_date"]
        cert_issuer=domain_data["issuer_organization"]

        # Prepare the insert query
        check_kv = "select rankdb_id from index_page where rankdb_id = %s limit 1"
        cursor.execute(
            check_kv, (rankdb_id,)
        )
        data = cursor.fetchall()
        if len(data)>0:
            index_page_exists = True
        else:
            index_page_exists = False

        if 'Server' in domain_data["headers"]:
            update_kv(rankdb_id,"Server",domain_data["headers"]["Server"])
        else:
            if 'server' in domain_data["headers"]:
                update_kv(rankdb_id,"Server",domain_data["headers"]["server"])

        if 'Server' in domain_data["headers"]:
            update_kv(rankdb_id,"Server",domain_data["headers"]["Server"])

        if title != None:
            update_kv(rankdb_id,"title",title)

        if cert_issuer != None:
            update_kv(rankdb_id,"crt_issuer",cert_issuer)

        if cert_expiry != None:
            update_kv(rankdb_id,"crt_expiry",cert_expiry)

        # Prepare the insert query
        if index_page_exists:
            update_domain = "update index_page set title=%s, content_size=%s, headers=%s, cert_issuer=%s, cert_expiry=%s, last_updated=CURDATE() where rankdb_id = %s"
            cursor.execute(
                update_domain, (title,content_size,headers,cert_issuer,cert_expiry,rankdb_id,)
            )
        else:
            add_domain = "insert into index_page (title, content_size, headers, cert_issuer, cert_expiry, last_updated, rankdb_id) values (%s,%s,%s,%s,%s,CURDATE(),%s) "
            cursor.execute(
                add_domain, (title,content_size,headers,cert_issuer,cert_expiry,rankdb_id,)
            )
        cnx.commit()

    except mysql.connector.Error as err:
        print(f"Error inserting data (1): {err}")

# Function to insert data into the database
def updatePageRank(rankdb_id):
    try:
        # Prepare the insert query
        add_domain = "update rankdb set last_checked=CURDATE(), last_updated=CURDATE() where id = %s"
        cursor.execute(
            add_domain, (rankdb_id,)
        )

        # Commit the changes
        cnx.commit()
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")


# Function to insert data into the database
def updateDomainPage(rankdb_id, tohost, todomain):
    try:
        # Prepare the insert query
        add_domain = (
            "INSERT INTO domainpage (rankdb_id, tohost, todomain) VALUES (%s, %s, %s)"
        )

        # Insert the data
        cursor.execute(add_domain, (rankdb_id, tohost, todomain))

        # Commit the changes
        #cnx.commit()
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")

# Process the script output
def update(rankdb_id,domain,index_page_exists):
    domain_data = {}
    try:
        domain_data = domainrisk.getDomainRisk(domain)
    except:
        domain_data = {}

    if "domain" in domain_data:
        delete_domain = "DELETE FROM domainpage where rankdb_id = %s"
        cursor.execute(delete_domain, (rankdb_id,))
        cnx.commit()
        # Process the remaining lines
        for tohost in domain_data["unique_hosts"]:
            todomain = domainrisk.extract_domain(tohost)
            updateDomainPage(rankdb_id, tohost, todomain)

        updatePageRank(
            rankdb_id
        )

        if 'not_after_date' in domain_data:
            updateIndexPage(
                rankdb_id,
                domain_data,
                index_page_exists
            )
        else:
            print(domain_data)
    else:
        updatePageRankFailTimestamp(rankdb_id)

def update_top_domains(limit=100,prime=1):
    """
    Retrieves the top `limit` domains from the `rankdb` table, ordered by rank.

    Args:
      limit: The maximum number of domains to retrieve (default: 100).

    Returns:
      A list of tuples containing the domain and its rank.
    """

    global cnx

    try:
        # Prepared statement for efficient retrieval
        query = "SELECT id, domain, rank, max(if(index_page.rankdb_id is null,false, true)) index_page_exists FROM rankdb left join index_page on index_page.rankdb_id=rankdb.id where (rankdb.last_checked is null or rankdb.last_checked < CURRENT_DATE()) and retry_attempt=0 and (last_attempted is null or last_attempted < DATE_SUB(NOW(), INTERVAL 20 MINUTE)) and round(rank/%s)*%s=rank group by 1, 2, 3 ORDER BY rank ASC LIMIT %s"
        cursor.execute(query, (prime,prime,limit,))

        # Fetch all results as a list of tuples
        top_domains = cursor.fetchall()

        for rankdb_id, domain, rank, index_page_exists in top_domains:
            query = "update rankdb set last_attempted=CURRENT_TIMESTAMP() where id=%s"
            cursor.execute(query, (rankdb_id,))

        cnx.commit()

        # Print the domain and rank for each entry
        for rankdb_id, domain, rank, index_page_exists in top_domains:
            print(f"Updating: {domain}, Rank: {rank}")
            update(rankdb_id,domain, index_page_exists)

    except mysql.connector.Error as err:
        print(f"Error retrieving top domains: {err}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        prime = 1
    else:
        prime = sys.argv[1]

    db_start()

    update_top_domains(500,prime)

    db_close()


    
