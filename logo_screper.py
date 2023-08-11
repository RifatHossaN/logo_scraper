from bs4 import BeautifulSoup
import os
import requests
from requests.exceptions import RequestException
from urllib.parse import urlparse, urljoin

def polisher_primary(url):
    removes = ["https://","http://"]
    for i in removes :
        if i in url:
            url = url.replace (i,"")
    while " " in url:
        url.replace(" ","")
    return url

def polisher_ultimate(url):
    removes = ["https://","www.",".com","http://","/"]
    for i in removes :
        if i in url:
            url = url.replace (i,"")
    return url

def change_logo_name (save_path,url):

    # Specify the current file path and name
    current_file_path = save_path+'.ico'

    # Specify the new file name
    new_file_name = polisher_ultimate(url)+'.ico'
    print(new_file_name)

    # Get the directory path of the current file
    directory = os.path.dirname(current_file_path)

    # Get the new file path by joining the directory path and the new file name
    new_file_path = os.path.join(directory, new_file_name)

    # Rename the file
    os.rename(current_file_path, new_file_path)


def download_favicon(url, save_path):
    try:
        parsed_url = urlparse(polisher_primary(url))
        if not parsed_url.scheme:
            # If the scheme is missing, assume 'https' as the default scheme
            url = f'https://{url}'
      
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        soup = BeautifulSoup(response.text, 'lxml')
        favicon_link = soup.find("link", rel="shortcut icon")

        if favicon_link is None:
            favicon_link = soup.find("link", rel="icon")
      
        if favicon_link is not None:      
            favicon = favicon_link.get('href')
            # - If favicon link is relative, make it absolute by appending to base URL
            if not bool(urlparse(favicon).netloc):
                favicon = urljoin(url, favicon)

            favicon_content = requests.get(favicon).content
      
          # - Save favicon to a file in the provided directory
            with open(os.path.join(save_path, parsed_url.netloc +'.ico'), 'wb') as f:
                f.write(favicon_content)
        change_logo_name (save_path, url) 

    except RequestException as e:
        print(f"Failed to download favicon from {url}: {str(e)}")
    

def main():
    link_file = 'url/text/file/path'
    save_path = 'save/logo/location/path'

    print(os.path.abspath(link_file))  # Print the absolute path

    with open(link_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            download_favicon(line.strip(), save_path)

if __name__ == '__main__':
    main()
