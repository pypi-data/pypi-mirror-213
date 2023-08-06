import os
import tempfile
import requests
import string
import random

def generate_random_folder_name(length=8):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def download_file(url):
    response = requests.get(url)
    if response.status_code == 200:
        temp_folder = tempfile.gettempdir()
        folder_name = generate_random_folder_name()
        folder_path = os.path.join(temp_folder, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        file_name = os.path.basename(url)
        file_path = os.path.join(folder_path, file_name)

        with open(file_path, 'wb') as file:
            file.write(response.content)

        print(f"File downloaded successfully: {file_path}")
    else:
        print(f"Failed to download file from: {url}")
