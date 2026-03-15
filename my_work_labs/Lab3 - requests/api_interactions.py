# API interactions code for Lab 3 
# Authered by: Stephen Kerr

import requests
url = "https://andrewbeatty1.pythonanywhere.com/books"
response = requests.get(url)
# print (response.text)

# print(response.json())

def read_books(id):
    url = "https://andrewbeatty1.pythonanywhere.com/books"
    geturl = url + "/" + str(id)
    response = requests.get(geturl)
    return response.json()

if __name__ == "__main__":
    books = read_books(1697)
    print(books)