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
			if '译　　名' in context:
				movie_title_translated = context.replace("译　　名", "").strip()
				print("Mobie Title Translated: " + movie_title_translated)
			elif '片　　名' in context:
				movie_title = context.replace("片　　名", "").strip()
				print("Mobie Title: " + movie_title)
			elif '年　　代' in context:
				release_year = context.replace("年　　代", "").strip()
				print("Release Year: " + release_year)
			elif '国　　家' in context:
				country = context.replace("国　　家", "").strip()
				print("Country: " + country)
			elif '类　　别' in context:
				genres = context.replace("类　　别", "").strip()
				print("Genres: " + genres)
			elif '语　　言' in context:
				language = context.replace("语　　言", "").strip()
				print("Language: " + language)
			elif 'IMDb评分' in context:
				imdb_rate = context.replace("IMDb评分", "").strip()
				print("IMDb Rate: " + imdb_rate)
			elif '片　　长' in context:
				runtime = context.replace("片　　长", "").strip()
				print("Runtime: " + runtime)
			elif '导　　演' in context:
				director = context.replace("导　　演", "").strip()
				print("Director: " + director)
			elif '主　　演' in context:
				cast = context.replace("主　　演", "").strip()
				print("Cast: " + cast)
			elif '简　　介' in context:
				storyline = context.replace("简　　介", "").strip()
				print("Storyline: " + storyline)

		# # Trivia, Text Area(Long)
		# # Reviews, Text Area(Long)
		# # Awards, Text Area(Long)

		
		# Download URL, URL
		download_url = str(content_text.find(id="Zoom").find('table').find('a').get('href')).strip();
		print("Download URL: " + download_url)

		# # Thunder URL, URL
		# # thunder_url = str(content_text.find(id="Zoom").find('table').find('a').get('gxmywwto')).strip();
		# # print("Thunder URL: " + thunder_url)

		print("\n")
		# break