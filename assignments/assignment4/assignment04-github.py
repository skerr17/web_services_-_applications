# This prohram reads a file from a repository
# and replace all the instances of the text "Andrew" with "Stephen"
# the program commits the changes to the repository
# Autherd by Stephen Kerr

# imports
from github import Github
from github import Auth
import requests
from config import api_token as cfg

# api key from config.py
api_key = cfg["apikey"]

# authenticate with GitHub using the API key
g = Github(auth=Auth.Token(api_key))

# get the repository
repo = g.get_repo("skerr17/private_repo")

# get the file information
file_info = repo.get_contents("test.txt")

# get the download url of the file
url_of_file = file_info.download_url

# download the file content
response = requests.get(url_of_file)
print(response.status_code)

content_of_file = response.text

# replace all instances of "Andrew" with "Stephen"
new_content = content_of_file.replace("Andrew", "Stephen")

# update the file in the repository with the new content
github_response = repo.update_file(file_info.path, 
                                  "updated by program to replace Andrew with Stephen", 
                                  new_content, 
                                  file_info.sha
                                  )

