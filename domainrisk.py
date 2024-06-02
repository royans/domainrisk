#!/usr/bin/env python3

# Domain Risk counts total number of unique hosts in a webpage - higher is worse - ideal is under 5.
# Royans K Tharakan - 2024 May 26

import requests
import sys
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from fake_useragent import UserAgent
import re

# Function to remove special characters
def remove_special_chars(domain_name):
  """Removes special characters from a domain name."""
  return re.sub(r'[^a-zA-Z0-9.-]', '', domain_name)

def extract_domain(fqdn):
  """
  Extracts the top-level domain (TLD) from a fully qualified domain name (FQDN).

  Args:
    fqdn: The fully qualified domain name (e.g., "www.abc.com").

  Returns:
    The top-level domain (e.g., "abc.com").
  """

  parts = fqdn.split('.')
  # If there's only a subdomain and a TLD, return the entire domain name
  if len(parts) == 2:
    return '.'.join(parts)
  else:
    # Check if the TLD is a two-letter country code
    if len(parts[-1]) == 2:
      # Check if the second-to-last part is a generic TLD
      generic_tlds = ["com", "net", "org", "edu", "gov", "mil"]
      if parts[-2] in generic_tlds:
        # If it is, return the last three parts
        return '.'.join(parts[-3:])
      else:
        # Otherwise, return the last two parts (country code TLD)
        return '.'.join(parts[-2:])
    else:
      # Standard case, return the last two parts (generic TLD)
      return '.'.join(parts[-2:])

# Function to remove special characters
def remove_special_chars(domain_name):
  """Removes special characters from a domain name."""
  return re.sub(r'[^a-zA-Z0-9.-]', '', domain_name)

def tld(fqdn):
    output=extract_domain(remove_special_chars(fqdn))
    return output

def get_homepage(domain):
    """Tries different URLs to get the homepage of a domain."""
    urls = [
        f"https://{domain}",
        f"http://{domain}",
        f"https://www.{domain}",
        f"http://www.{domain}"
    ]

    ua = UserAgent()
    headers = {'User-Agent': ua.chrome}  # Set Chrome User-Agent

    for url in urls:
        try:
            response = requests.get(url,  headers=headers, timeout=3)
            response.raise_for_status()  # Raise an exception for bad status codes
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            continue

    print(f"Could not find a valid homepage for {domain}")
    return None

def extract_javascript_hosts(response):
    """Extracts JavaScript hosts from a web page, including any HTTP URLs within <script> tags."""
    soup = BeautifulSoup(response.content, "html.parser")
    scripts = soup.find_all("script")  # Get all <script> tags, regardless of attributes
    hosts = []
    domains = []
    for script in scripts:
        # Check for 'src' attribute (for external JavaScript files)
        if script.get('src'):
            url = script['src']
            hostname = urlparse(url).hostname
            if hostname:
                hosts.append(hostname)
        # Check for script content that might contain URLs
        else:
            for content in script.contents:
                if isinstance(content, str):
                    # Use regex to find URLs in the script content
                    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>\"']+|\(([^\s()<>\"']+|(\([^\s()<>\"']+\)))*\))+(?:\(([^\s()<>\"']+|(\([^\s()<>\"']+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
                    urls = re.findall(regex, content)
                    for url in urls:
                        hostname = urlparse(url[0]).hostname
                        if hostname:
                            if ("." in hostname):
                                hosts.append(hostname)
                                domains.append(tld(hostname))
    return (hosts,domains)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <domain_name>")
        sys.exit(1)

    domain = sys.argv[1]

    response = get_homepage(domain)
    #print(response.content )
    if response:
        (javascript_hosts, javascript_domains) = extract_javascript_hosts(response)
        unique_domains = set(javascript_domains)
        unique_hosts = set(javascript_hosts)
        print("Domain Namne - Unique hosts - Unique domains")
        print(domain+" "+str(len(unique_hosts))+","+str( len(unique_domains)))
        for host in unique_domains:
            print(host)
