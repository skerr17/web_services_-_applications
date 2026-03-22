# 

from github import Github 

from github import Auth

import requests

from config import api_token as cfg

api_key = cfg["apikey"]

g = Github(auth=Auth.Token(api_key))

# for repo in g.get_user().get_repos():
#    print(repo.name)

repo = g.get_repo("skerr17/private_repo")
# print(repo.clone_url)


file_info = repo.get_contents("test.txt")
url_of_file = file_info.download_url

# print(url_of_file)

response = requests.get(url_of_file)
print(response.status_code)
content_of_file = response.text
print(content_of_file)

new_content = content_of_file + "\nThis is a new line added to the file using the GitHub API and Python"

# print(new_content)

# update_file(path, message, content, sha, branch=NotSet, committer=NotSet, author=NotSet)

gitHubResponse=repo.update_file(file_info.path,"updated by prog",
new_content,file_info.sha)
print (gitHubResponse)