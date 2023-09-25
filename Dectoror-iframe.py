import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

# Function to extract all iframe sources from a URL
def extract_all_iframe_srcs(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        if urlparse(url).netloc == "www.hindimovies.to" and re.match(r'^/movie/', urlparse(url).path):
            st.write("IFrame Sources are not applicable for this URL.")
            return [find_custom_url(url)]

        iframes = soup.find_all('iframe')
        if not iframes:
            return ["No iframes found on this page."]
        
        iframe_srcs = [iframe.get('src') for iframe in iframes if iframe.get('src')]
        return iframe_srcs
    except Exception as e:
        return [f"Error: {e}"]

# Function to find the custom URL for "www.hindimovies.to" domain and specific URL pattern
def find_custom_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Add code to find the custom URL for "www.hindimovies.to" domain and specific URL pattern
        # Here's a placeholder code to extract the URL from a div with id "iframe-screen":
        div = soup.find('div', id="iframe-screen")
        if div:
            a = div.find('a', href=True)
            if a:
                return a['href']
            else:
                return "No custom URL found on this page."
        else:
            return "No custom URL found on this page."
    except Exception as e:
        return f"Error: {e}"

# Function to extract links 01, 03, and 04 from the provided URL pattern
def extract_links_010304(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        link_pattern = re.compile(r'Link\s+(\d{2})')
        link_elements = soup.find_all(text=link_pattern)

        links = {}
        for link_element in link_elements:
            match = link_pattern.search(link_element)
            if match:
                link_number = match.group(1)
                link_container = link_element.find_next('div', class_='OptionBx on')
                if link_container:
                    link_url = link_container.find('a', href=True)
                    if link_url:
                        links[f"Link {link_number}"] = link_url['href']
        
        return links
    except Exception as e:
        return {}

# Streamlit UI
st.title("IFrame SRC Extractor for Streaming Websites")

st.write("Enter the URLs of streaming websites (one per line) to extract iframe sources:")
user_input = st.text_area("Enter URLs", "")

if st.button("Extract"):
    urls = user_input.split('\n')
    for url in urls:
        if url.strip():
            iframe_srcs = extract_all_iframe_srcs(url.strip())
            st.write(f"URL: {url.strip()}")
            if iframe_srcs:
                st.write("IFrame Sources:")
                for i, src in enumerate(iframe_srcs):
                    st.write(f"{i + 1}. {src}")
            else:
                st.write("No IFrame Sources found.")
            
            st.write("Link 01, Link 03, Link 04:")
            links = extract_links_010304(url.strip())
            for link, href in links.items():
                st.write(f"{link}: {href}")
            st.write("-" * 50)
