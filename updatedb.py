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
def updatePageRankFailTimestamp(domain):
    try:
        # Connect to the database
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        # Prepare the insert query
        add_domain = "update rankdb set last_checked=CURDATE() where domain = %s"

        # Insert the data 
        # convert_date_to_datetime
        cursor.execute(
            add_domain, (domain,)
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
def updatePageRank(domain, cert_expiry, cert_issuer):
    try:
        # Connect to the database
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        # Prepare the insert query
        add_domain = "update rankdb set cert_expiry=%s, cert_issuer=%s,last_checked=CURDATE(), last_updated=CURDATE() where domain = %s"

        # Insert the data 
        # convert_date_to_datetime
        cursor.execute(
            add_domain, ((cert_expiry), cert_issuer, domain)
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
def updateDomainPage(domain, tohost, todomain):
    try:
        # Connect to the database
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        # Prepare the insert query
        add_domain = (
            "INSERT INTO domainpage (domain, tohost, todomain) VALUES (%s, %s, %s)"
        )

        # Insert the data
        cursor.execute(add_domain, (domain, tohost, todomain))

        # Commit the changes
        cnx.commit()

        # Close the cursor and connection
        cursor.close()
        cnx.close()

        # print(f"Data inserted for domain: {domain}")

    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")


# Process the script output
def update(domain):
    # //(_domain,unique_hosts,unique_domains,not_after_date,issuer_organization) = domainrisk.getDomainRisk(domain)
    domain_data = domainrisk.getDomainRisk(domain)

    if "domain" in domain_data:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        delete_domain = "DELETE FROM domainpage where domain = %s"
        cursor.execute(delete_domain, (domain,))
        cnx.commit()
        cnx.close()

        # Process the remaining lines
        for tohost in domain_data["unique_hosts"]:
            todomain = domainrisk.extract_domain(tohost)
            updateDomainPage(domain, tohost, todomain)

        # updatePageRank(domain, cert_expiry, cert_issuer):
        updatePageRank(
            domain,
            (domain_data["not_after_date"]),
            domain_data["issuer_organization"],
        )
    else:
        updatePageRankFailTimestamp(domain)

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
        #query = "SELECT domain, rank FROM rankdb where cert_issuer is null ORDER BY last_checked, rank ASC LIMIT %s"
        #query = "SELECT domain, rank FROM rankdb where last_checked is null and ignorerow=false ORDER BY rank ASC LIMIT %s"
        query = "SELECT domain, rank FROM rankdb where last_checked is null and ignorerow=false and round(rank/%s)*%s=rank ORDER BY rank ASC LIMIT %s"
        cursor.execute(query, (prime,prime,limit,))

        # Fetch all results as a list of tuples
        top_domains = cursor.fetchall()

        # Print the domain and rank for each entry
        for domain, rank in top_domains:
            print(f"Updating: {domain}, Rank: {rank}")
            update(domain)

    except mysql.connector.Error as err:
        print(f"Error retrieving top domains: {err}")

    finally:
        if cnx:
            cnx.close()


if __name__ == "__main__":
    # import sys
    if len(sys.argv) != 2:
        prime = 1
    else:
        prime = sys.argv[1]
    #update("msn.com")
    update_top_domains(10000,prime)
