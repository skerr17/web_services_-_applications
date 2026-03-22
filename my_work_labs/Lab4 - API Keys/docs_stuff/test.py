import requests

url = "https://en.wikipedia.org"
apiKey = "HNBXFTB3EBTdSG2m8H0rrolHZPJUZfXeYxYhhGzrezCCgyMzyY4CSrtb7qFC69mp"
linkRequests = "https://api.html2pdf.app/v1/generate?html={0}&apiKey={1}".format(url, apiKey)

result = requests.get(linkRequests).content

with open("document.pdf", "wb") as handler:
    handler.write(result)
