# import sys
# print(sys.getdefaultencoding())
# if sys.version[0] == '2':
#     reload(sys)
#     sys.setdefaultencoding("utf-8")
    
import re
import urllib.request
from bs4 import BeautifulSoup

# proxy_support = urllib.request.ProxyHandler({"http":"http://iedub98:8080", "https":"https://iedub98:8080"})
# opener = urllib.request.build_opener(proxy_support)
# urllib.request.install_opener(opener)

def find_between(s, first, last):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

url = "http://www.ygdy8.net/html/gndy/dyzz/index.html"
response = urllib.request.urlopen(url).read()
soup = BeautifulSoup(response, 'html.parser', from_encoding='gbk')
pageText = str(soup.find(class_='co_content8').find('div').find('td').next)
number_of_pages = int(find_between(pageText, '共', '页'))
number_of_movies = int(find_between(pageText, '/', '条'))
print('共' + str(number_of_pages) + '页')
print('共' + str(number_of_movies) + '条')

for i in range(1):
	url = "http://www.ygdy8.net/html/gndy/dyzz/list_23_" + str(i+1) + ".html"
	print("Starting Page " + str(i+1) + "/" + str(number_of_pages) + ", at "+ url, end="\r")
	response = urllib.request.urlopen(url).read()
	soup = BeautifulSoup(response, 'html.parser', from_encoding='gbk')
	for link in soup.findAll(class_='ulink'):
		url = "http://www.ygdy8.net" + link.get('href')
		response = urllib.request.urlopen(url).read()
		soup = BeautifulSoup(response, 'html.parser', from_encoding='gbk')
		print("Starting DYTT Name: " + soup.title.text + " at " + url)
		# Get all fields
		content_text = soup.find(class_='co_content8').find('ul')

		# Publish Date at DYTT, Date
		publish_date = content_text.next.strip().replace("发布时间：", "").strip()
		print("Publish Date at DYTT: " + publish_date)

		# Poster URL, URL
		poster_url = content_text.find(id="Zoom").find_all('p')[0].find('img').get('src')
		print("Poster URL: " + poster_url)

		# Context List
		context_list = content_text.find(id="Zoom").get_text('\n', strip=True).split('◎')
		for context in context_list:
			if '片　　名' in context:
				movie_title = context.replace("片　　名", "").strip()
				print("Mobie Title: " + movie_title)
			elif '译　　名' in context:
				movie_title_in_chinese = context.replace("译　　名", "").strip()
				print("Mobie Title in Chinese: " + movie_title_in_chinese)



		# # Movie Title, Text(50)
		# movie_title = content_text.find(id="Zoom").find_all('p')[0].find_all('br')[2].next.replace("◎片　　名", "").strip()
		# print("Mobie Title: " + movie_title)

		# # Movie Title in Chinese, Text(50)
		# movie_title_in_chinese = content_text.find(id="Zoom").find_all('p')[0].find_all('br')[1].next.replace("◎译　　名", "").strip()
		# print("Mobie Title in Chinese: " + movie_title_in_chinese)

		# # Release Year, Text(20)
		# release_year = content_text.find(id="Zoom").find_all('p')[0].find_all('br')[3].next.replace("◎年　　代", "").strip()
		# print("Release Year: " + release_year)

		# # Country, Text(50)
		# country = content_text.find(id="Zoom").find_all('p')[0].find_all('br')[4].next.replace("◎国　　家", "").strip()
		# print("Country: " + country)

		# # Genres, Text(50)
		# genres = content_text.find(id="Zoom").find_all('p')[0].find_all('br')[5].next.replace("◎类　　别", "").strip()
		# print("Genres: " + genres)

		# # Language, Text(50)
		# language = content_text.find(id="Zoom").find_all('p')[0].find_all('br')[6].next.replace("◎语　　言", "").strip()
		# print("Language: " + language)

		# # IMDb Rate, Number(2, 1)
		# # Runtime, Text(20)
		# # Director, Text(50)
		# # Cast, Text Area(Long)
		# # Storyline, Text Area(Long)
		# # Trivia, Text Area(Long)
		# # Reviews, Text Area(Long)
		# # Awards, Text Area(Long)

		
		# Download URL, URL
		download_url = str(content_text.find(id="Zoom").find('table').find('a').get('href')).strip();
		print("Download URL: " + download_url)

		# # Thunder URL, URL
		# # thunder_url = str(content_text.find(id="Zoom").find('table').find('a').get('gxmywwto')).strip();
		# # print("Thunder URL: " + thunder_url)

		# break