import mysql.connector
import re
import os
import sys
import subprocess
from datetime import datetime
import domainrisk

# Get database credentials from environment variables
db_user = os.environ.get("DBUSER")
db_password = os.environ.get("DBPASS")

# Database connection details (replace placeholders with your host and database name)
config = {
    "user": db_user,
    "password": db_password,
    "host": "localhost",
    "database": "domainrisk",
}


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


# Function to insert data into the database
def updatePageRankFailTimestamp(rankdb_id):
    try:
        # Connect to the database
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        # Prepare the insert query
        add_domain = "update rankdb set last_checked=CURDATE() where id = %s"

        # Insert the data 
        # convert_date_to_datetime
        cursor.execute(
            add_domain, (rankdb_id,)
        )

        # Commit the changes
        cnx.commit()

        # Close the cursor and connection
        cursor.close()
        cnx.close()

        # print(f"Data inserted for domain: {domain}")

    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")


# Function to insert data into the database
def updateIndexPage(rankdb_id, domain_data,index_page_exists):
    try:
        title=domain_data["title"]
        headers=domain_data["headers"][0:1000]
        contents=""
        content_size=len(domain_data["contents"])
        cert_expiry=domain_data["not_after_date"]
        cert_issuer=domain_data["issuer_organization"]
        # Connect to the database
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        #print("test 5 - index page")

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

        #print("test 5.1")
        # Commit the changes
        cnx.commit()

        # Close the cursor and connection
        cursor.close()
        cnx.close()

        # print(f"Data inserted for domain: {domain}")

    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")

# Function to insert data into the database
def updatePageRank(rankdb_id):
    try:
        # Connect to the database
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        #print("test 5")

        # Prepare the insert query
        add_domain = "update rankdb set last_checked=CURDATE(), last_updated=CURDATE() where id = %s"

        # Insert the data 
        # convert_date_to_datetime
        cursor.execute(
            add_domain, (rankdb_id,)
        )

        #print("test 5.1")
        # Commit the changes
        cnx.commit()

        # Close the cursor and connection
        cursor.close()
        cnx.close()

        # print(f"Data inserted for domain: {domain}")

    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")


# Function to insert data into the database
def updateDomainPage(rankdb_id, tohost, todomain):
    try:
        # Connect to the database
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        #print("test 4")
        # Prepare the insert query
        add_domain = (
            "INSERT INTO domainpage (rankdb_id, tohost, todomain) VALUES (%s, %s, %s)"
        )

        # Insert the data
        cursor.execute(add_domain, (rankdb_id, tohost, todomain))
        #print("test 4.1")

        # Commit the changes
        cnx.commit()

        # Close the cursor and connection
        cursor.close()
        cnx.close()

        # print(f"Data inserted for domain: {domain}")

    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")


# Process the script output
def update(rankdb_id,domain,index_page_exists):
    # //(_domain,unique_hosts,unique_domains,not_after_date,issuer_organization) = domainrisk.getDomainRisk(domain)
    domain_data = {}
    try:
        domain_data = domainrisk.getDomainRisk(domain)
    except:
        domain_data = {}

    if "domain" in domain_data:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        delete_domain = "DELETE FROM domainpage where rankdb_id = %s"
        #print(rankdb_id)

        cursor.execute(delete_domain, (rankdb_id,))
        cnx.commit()
        cnx.close()

        # Process the remaining lines
        for tohost in domain_data["unique_hosts"]:
            todomain = domainrisk.extract_domain(tohost)
            updateDomainPage(rankdb_id, tohost, todomain)

        # updatePageRank(domain, cert_expiry, cert_issuer):
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

    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        # Prepared statement for efficient retrieval
        query = "SELECT id, domain, rank, if(index_page.rankdb_id is null,false, true) index_page_exists FROM rankdb left join index_page on index_page.rankdb_id=rankdb.id where (rankdb.last_checked is null and rankdb.last_updated is null) and retry_attempt=0 and round(rank/%s)*%s=rank ORDER BY rank ASC LIMIT %s"
        cursor.execute(query, (prime,prime,limit,))


        # Fetch all results as a list of tuples
        top_domains = cursor.fetchall()

        # Print the domain and rank for each entry
        for rankdb_id, domain, rank, index_page_exists in top_domains:
            print(f"Updating: {domain}, Rank: {rank}")
            update(rankdb_id,domain, index_page_exists)

    except mysql.connector.Error as err:
        print(f"Error retrieving top domains: {err}")

    finally:
        if cnx:
            cnx.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        prime = 1
    else:
        prime = sys.argv[1]
    update_top_domains(10000,prime)
