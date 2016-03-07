import urllib.request
 
url = "http://www.ygdy8.net/html/gndy/dyzz/list_23_1.html"
data = urllib.request.urlopen(url).read()
data = data.decode('UTF-8')
print(data)