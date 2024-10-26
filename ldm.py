import os
import subprocess

# Create a main directory for downloads
main_directory = "Linux Download Manager"
os.makedirs(main_directory, exist_ok=True)

# Function to determine folder based on file extension
def get_folder_name(filename):
    if filename.endswith(('.mp3', '.wav', '.flac')):
        return "Music"
    elif filename.endswith(('.mp4', '.avi', '.mkv')):
        return "Videos"
    elif filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
        return "Images"
    elif filename.endswith(('.pdf', '.docx', '.txt')):
        return "Documents"
    else:
        return "Others"

# Function to download a file using aria2c
def download_file(url):
    try:
        # Get the filename from the URL
        filename = url.split("/")[-1]
        
        # Determine the file type and set the appropriate folder
        folder = get_folder_name(filename)
        
        # Create the specific folder if it doesn't exist
        folder_path = os.path.join(main_directory, folder)
        os.makedirs(folder_path, exist_ok=True)

        # Define the full file path
        file_path = os.path.join(folder_path, filename)

        # Construct the aria2c command
        command = ["aria2c", "-d", folder_path, "-o", filename, url]
        
        # Run the aria2c command
        subprocess.run(command, check=True)

        print(f"Downloaded: {filename} to {folder_path}")

    except subprocess.CalledProcessError as e:
        print(f"Failed to download {url}: {e}")

# Main loop to accept user input
def main():
    print("Welcome to the Linux Download Manager using aria2c!")
    while True:
        url = input("Enter a download link (or type 'exit' to quit): ")
        if url.lower() == 'exit':
            break
        download_file(url)

if __name__ == "__main__":
    main()

