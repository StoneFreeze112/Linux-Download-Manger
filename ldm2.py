import os
import re
import requests
import subprocess
from urllib.parse import unquote, urlsplit

def get_filename_from_url(url):
    """
    Try to get the filename from the HTTP headers or URL.
    """
    try:
        # Send a HEAD request to get headers
        response = requests.head(url, allow_redirects=True)
        
        # Check if 'Content-Disposition' header is present
        if 'Content-Disposition' in response.headers:
            # Extract filename from Content-Disposition header
            filename_match = re.findall(r'filename\*=UTF-8\'\'(.+)', response.headers['Content-Disposition'])
            if not filename_match:
                filename_match = re.findall(r'filename="(.+)"', response.headers['Content-Disposition'])
                
            if filename_match:
                return unquote(filename_match[0])

        # If no filename found from headers, fall back to a GET request to inspect response
        response = requests.get(url, stream=True, allow_redirects=True)
        if 'Content-Disposition' in response.headers:
            filename_match = re.findall(r'filename\*=UTF-8\'\'(.+)', response.headers['Content-Disposition'])
            if not filename_match:
                filename_match = re.findall(r'filename="(.+)"', response.headers['Content-Disposition'])
            
            if filename_match:
                return unquote(filename_match[0])

        # If no filename from headers, try to get it from URL path
        path = urlsplit(response.url).path
        filename = os.path.basename(path)
        if filename:
            return unquote(filename)

    except requests.RequestException as e:
        print(f"Error fetching filename: {e}")
    
    return "downloaded_file"  # Default name if filename can't be determined

def download_with_aria2c(url, download_path):
    """
    Download file using aria2c.
    """
    filename = get_filename_from_url(url)
    if not filename:
        print("Could not determine the filename. Using default: downloaded_file.")
        filename = "downloaded_file"

    # Ensure download path exists
    os.makedirs(download_path, exist_ok=True)

    # Combine the download path and filename
    file_path = os.path.join(download_path, filename)

    # Command for downloading using aria2c
    command = [
        "aria2c",
        url,
        "--out", filename,
        "--dir", download_path
    ]

    # Run the aria2c command
    try:
        print(f"Starting download with aria2c...\nCommand: {' '.join(command)}")
        subprocess.run(command, check=True)
        print(f"Download completed: {file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Download failed: {e}")

if __name__ == "__main__":
    download_url = input("Enter the download URL: ").strip()
    download_location = input("Enter the download location path (default: current directory): ").strip() or "."

    download_with_aria2c(download_url, download_location)
