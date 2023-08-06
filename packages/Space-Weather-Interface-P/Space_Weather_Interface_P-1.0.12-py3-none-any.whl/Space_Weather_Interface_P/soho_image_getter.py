import urllib.request
import os
import re

#on some computers there seems to be an error with SSL handling, this should ensure secure connections over SSL
import ssl; ssl._create_default_https_context = ssl._create_stdlib_context

# get current date
from datetime import date
today = date.today()
year = today.strftime("%Y")
month = today.strftime("%m")
day = today.strftime("%d")
path = './images/soho'
date = f"{year}{month}{day}"

image_list = []

for filename in os.listdir(path):
    # check if the file extension is an image extension
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        # if it is, add the filename to the list
        image_list.append(filename)

# specify url and download directory
url = f"https://umbra.nascom.nasa.gov/pub/incoming/lasco/rtmovie_png/"
download_directory = "./images/soho/"

# create download directory if it doesn't exist
if not os.path.exists(download_directory):
    os.makedirs(download_directory)

# download images with filenames containing "date" and "c2"
with urllib.request.urlopen(url) as response:
    html = response.read().decode()
    pattern = re.compile(r'href="(.*?\.png)"')
    for match in pattern.finditer(html):
        filename = match.group(1)
        if date in filename and "c2" in filename and filename not in image_list:
            image_url = url + filename
            urllib.request.urlretrieve(image_url, download_directory + filename)
            print(f"Downloaded {filename}")
