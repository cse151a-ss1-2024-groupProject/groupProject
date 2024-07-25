import os
import requests
import gzip
import shutil
from bs4 import BeautifulSoup

# URL of the website to scrape
url = "https://insideairbnb.com/get-the-data/"

# Directory to save the downloaded files
download_dir = "data/raw"

# Create the directory if it doesn't exist
os.makedirs(download_dir, exist_ok=True)

# Function to download and convert a .csv.gz file
def download_and_convert_file(url, dest):
    response = requests.get(url)
    if response.status_code == 200:
        temp_gz_path = dest + '.gz'
        with open(temp_gz_path, 'wb') as f:
            f.write(response.content)
        with gzip.open(temp_gz_path, 'rb') as f_in:
            with open(dest, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove(temp_gz_path)
        print(f"Downloaded and converted: {dest}")
    else:
        print(f"Failed to download: {url}")

# Scrape the webpage to get the URLs of the .csv.gz files
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all .csv.gz links
links = soup.find_all('a', href=True)
csv_gz_links = [link['href'] for link in links if link['href'].endswith('listings.csv.gz')]

# Download and convert each .csv.gz file
for link in csv_gz_links:
    parts = link.split("/")
    country = parts[3]
    state = parts[4]
    city = parts[5]
    date = parts[6]
    if (country == 'united-states'):
        original_file_name = parts[-1].replace('.csv.gz', '.csv')
        new_file_name = f"{country}_{state}_{city}_{date}_{original_file_name}"
        download_and_convert_file(link, os.path.join(download_dir, new_file_name))

print("All files downloaded and converted.")
