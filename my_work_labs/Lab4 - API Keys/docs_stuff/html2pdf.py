# in this program we will 
# convert a website into a pdf
# using and API key from html2pdf.com
# Autherd by Stephen Kerr

# imports
import requests # for making the API request
import urllib.parse # for encoding the url

# api key from html2pdf.com
apikey = "HNBXFTB3EBTdSG2m8H0rrolHZPJUZfXeYxYhhGzrezCCgyMzyY4CSrtb7qFC69mp"

# target url to convert to pdf
target_url = "https://andrewbeatty1.pythonanywhere.com/bookviewer.html"


# API url for html2pdf.com
api_url = 'https://api.html2pdf.app/v1/generate'

# parameters for the API request
params = {
    'html': target_url,
    'apikey': apikey
}

# parse to encode the parameters for the API request
encoded_params = urllib.parse.urlencode(params)

# request url
request_url = api_url + "?" + encoded_params

# make the API request
response = requests.get(request_url)

# check if the request was successful
print(response.status_code)
print(response.text)

# save the pdf to a file
with open("sample.pdf", "wb") as pdf_file:
    pdf_file.write(response.content)


print(request_url)
