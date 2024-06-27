#!/usr/bin/env python3

# Domain Risk counts total number of unique hosts in a webpage - higher is worse - ideal is under 5.
# Royans K Tharakan - 2024 May 26
# Cert info extractor code from : https://github.com/qerty2006/domain_ssl_cert

import requests
import sys
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from fake_useragent import UserAgent
import re
import ssl
import socket
from datetime import datetime
from urllib3.util.ssl_ import create_urllib3_context

import errno
import os
import signal
import functools

class TimeoutError(Exception):
    pass

def fixstring(name):
    if name is None:
        return ""
    return name


def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wrapper

    return decorator


# Function to remove special characters
def remove_special_chars(domain_name):
    """Removes special characters from a domain name."""
    return re.sub(r"[^a-zA-Z0-9.-]", "", domain_name)


def convert_to_YYYY_MM_DD(date_time_str) -> str:
    """
    Converts a date and time string to the format YYYY/MM/DD.

    Args:
        date_time_str: The date and time string to convert.

    Returns:
        The converted date and time string in YYYY/MM/DD format, or None if the input string
        cannot be parsed.
    """

    try:
        # Define the input format with spaces separating elements
        input_format = "%b %d %H:%M:%S %Y %Z"
        # Parse the datetime string
        date_time_obj = datetime.strptime(date_time_str, input_format)
        # Define the desired output format
        output_format = "%Y/%m/%d"
        # Format the datetime object as a string in YYYY/MM/DD
        return date_time_obj.strftime(output_format)
    except ValueError:
        # Handle cases where the string cannot be parsed in the expected format
        return None


def get_certificate_details(url):
    """
    Retrieves the certificate details for a given URL.

    Args:
        url: The URL of the website.

    Returns:
        A dictionary containing the certificate details, or an error message if an error occurs.
    """

    try:
        # Ensure the URL starts with "https://"
        url = "https://" + url if not url.startswith("https://") else url
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname

        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=2) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                return cert
    except Exception as e:
        return f"Error# {e}"


def extract_domain(fqdn):
    """
    Extracts the top-level domain (TLD) from a fully qualified domain name (FQDN).

    Args:
      fqdn: The fully qualified domain name (e.g., "www.abc.com").

    Returns:
      The top-level domain (e.g., "abc.com").
    """

    parts = fqdn.split(".")
    # If there's only a subdomain and a TLD, return the entire domain name
    if len(parts) == 2:
        return ".".join(parts)
    else:
        # Check if the TLD is a two-letter country code
        if len(parts[-1]) == 2:
            # Check if the second-to-last part is a generic TLD
            generic_tlds = ["com", "net", "org", "edu", "gov", "mil", "co","ac"]
            if parts[-2] in generic_tlds:
                # If it is, return the last three parts
                return ".".join(parts[-3:])
            else:
                # Otherwise, return the last two parts (country code TLD)
                return ".".join(parts[-2:])
        else:
            # Standard case, return the last two parts (generic TLD)
            return ".".join(parts[-2:])


# Function to remove special characters
def remove_special_chars(domain_name):
    """Removes special characters from a domain name."""
    return re.sub(r"[^a-zA-Z0-9.-]", "", domain_name)


def tld(fqdn):
    output = extract_domain(remove_special_chars(fqdn))
    return output


@timeout(3)
def get_homepage(domain):
    """Tries different URLs to get the homepage of a domain."""
    urls = [
        f"https://{domain}",
        f"http://{domain}",
        f"https://www.{domain}",
        f"http://www.{domain}",
    ]

    ua = UserAgent()
    headers = {"User-Agent": ua.chrome}  # Set Chrome User-Agent

    ctx = create_urllib3_context()

    for url in urls:
        try:
            response = requests.get(url, headers=headers, timeout=3)
            response.raise_for_status()  # Raise an exception for bad status codes
            return response
        except requests.exceptions.RequestException as e:
            #print(f"Error fetching {url}: {e}")
            continue

    print(f"Could not find a valid homepage for {domain}")
    return None

@timeout(2)
def re_findall(regex, content):
    return re.findall(regex, content)

def extract_javascript_hosts(response):
    """Extracts JavaScript hosts from a web page, including any HTTP URLs within <script> tags."""
    soup = BeautifulSoup((response.content).lower(), "html.parser")
    scripts = soup.find_all("script")  # Get all <script> tags, regardless of attributes
    hosts = []
    domains = []
    for script in scripts:
        # Check for 'src' attribute (for external JavaScript files)
        if script.get("src"):
            url = script["src"]
            #print("--- SCRIPTS : "+url)
            hostname = urlparse(url).hostname
            if hostname:
                hosts.append(hostname)
                domains.append(tld(hostname))
        # Check for script content that might contain URLs
        else:
            if ( 1 == 2):
                for content in script.contents:
                    if isinstance(content, str):
                        # Use regex to find URLs in the script content
                        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>\"']+|\(([^\s()<>\"']+|(\([^\s()<>\"']+\)))*\))+(?:\(([^\s()<>\"']+|(\([^\s()<>\"']+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
                        urls = None
                        try: 
                            urls = re_findall(regex, content)
                        except:
                            urls = []
                        for url in urls:
                            try:
                                hostname = urlparse(url[0]).hostname
                                if hostname:
                                    if "." in hostname:
                                        hosts.append(remove_special_chars(hostname))
                                        domains.append(tld(hostname))
                            except:
                                urls = None
    return (hosts, domains)


def getDomainRisk(domain):
    domain_data = {}
    not_after_date = None
    issuer_organization = None
    response = get_homepage(domain)
    certinfo = get_certificate_details(domain)
    if isinstance(certinfo, dict):
        not_after_date = convert_to_YYYY_MM_DD(certinfo["notAfter"])
        for inner_tuple in certinfo["issuer"]:
            if inner_tuple[0][0] == "organizationName":
                issuer_organization = inner_tuple[0][1]
                break
    if response:
        (javascript_hosts, javascript_domains) = extract_javascript_hosts(response)
        unique_domains = set(javascript_domains)
        unique_hosts = set(javascript_hosts)
        domain_data = {
            "domain": domain,
            "unique_hosts": unique_hosts,
            "unique_domains": unique_domains,
            "not_after_date": not_after_date,
            "issuer_organization": issuer_organization,
        }
    return domain_data

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <domain_name>")
        sys.exit(1)

    domain = sys.argv[1]
    domain_data = getDomainRisk(domain)
    #    (_domain, unique_hosts, unique_domains, not_after_date, issuer_organization) = (
    #        getDomainRisk(domain)
    #    )

    if 'unique_hosts' in domain_data:
        #print(domain_data)
        print("Domain UniqueHosts,UniqueDomains,Cert expiry, Cert issuer")
        print(
            fixstring(domain)
            + ","
            + str(len(fixstring(domain_data['unique_hosts'])))
            + ","
            + str(len(fixstring(domain_data['unique_domains'])))
            + ","
            + fixstring(domain_data['not_after_date'])
            + ","
            + fixstring(domain_data['issuer_organization'])
        )
        for host in domain_data['unique_hosts']:
            print(host + " " + tld(host))
