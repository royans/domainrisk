#!/usr/bin/env python3

# Domain Risk counts total number of unique hosts in a webpage - higher is worse - ideal is under 5.
# Royans K Tharakan - 2024 May 26

import requests
import sys
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from fake_useragent import UserAgent
import re

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
    return hosts


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <domain_name>")
        sys.exit(1)

    domain = sys.argv[1]

    response = get_homepage(domain)
    #print(response.content )
    if response:
        javascript_hosts = extract_javascript_hosts(response)
        unique_hosts = set(javascript_hosts)
        for host in unique_hosts:
            print(host)
