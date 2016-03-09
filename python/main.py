import sys
# print(sys.getdefaultencoding())
if sys.version[0] == '2':
    reload(sys)
    sys.setdefaultencoding("utf-8")

import logging
import csv
import traceback
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
print('Total Page: ' + str(number_of_pages))
print('Total Movies: ' + str(number_of_movies))

number_of_success = 0
number_of_failure = 0
movie_list = [["DYTT Name", "DYTT URL", "Publish Date at DYTT", "Poster URL", "Movie Title Translated", "Movie Title", "Release Year", "Country", "Genres", "Language", "IMDb Rate", "Runtime", "Director", "Cast", "Storyline", "Trivia", "Reviews", "Awards", "Download URL"]]

error_list = [["Location", "Error Message"]]

for i in range(number_of_pages):
	url = "http://www.ygdy8.net/html/gndy/dyzz/list_23_" + str(i+1) + ".html"
	print("Starting Page " + str(i+1) + "/" + str(number_of_pages) + ", at "+ url)
	response = urllib.request.urlopen(url).read()
	soup = BeautifulSoup(response, 'html.parser', from_encoding='gbk')
	for link in soup.findAll(class_='ulink'):
		url = "http://www.ygdy8.net" + link.get('href')

		dytt_name = ""
		dytt_url = url
		publish_date = ""
		poster_url = ""
		movie_title_translated = ""
		movie_title = ""
		release_year = ""
		country = ""
		genres = ""
		language = ""
		imdb_rate = 0
		runtime = ""
		director = ""
		cast = ""
		storyline = ""
		trivia = ""
		reviews = ""
		awards = ""
		download_url = ""
		# test url
		# url = "http://www.ygdy8.net/html/gndy/dyzz/20121122/40310.html"
		# test url
		try:
			response = urllib.request.urlopen(url).read()
			soup = BeautifulSoup(response, 'html.parser', from_encoding='gbk')

			# Get all fields
			content_text = soup.find(class_='co_content8').find('ul')

			dytt_name = soup.title.text
			publish_date = content_text.find(text=re.compile("发布时间：")).strip().replace("发布时间：", "").strip()
			poster_url = content_text.find(id="Zoom").find('img').get('src')

			# content List
			content_list = content_text.find(id="Zoom").find(text=re.compile("导　　演")).parent.parent.get_text('\n', strip=True).split("【下载地址】", 1)[0].split('◎')

			for content in content_list:
				if '译　　名' in content:
					movie_title_translated = content.replace("译　　名", "").strip()
				elif '中 文 名' in content:
					movie_title_translated = content.replace("中 文 名", "").strip()
				elif '又　　名' in content:
					movie_title_translated = content.replace("又　　名", "").strip()

				elif '片　　名' in content:
					movie_title = content.replace("片　　名", "").strip()
				elif '英 文 名' in content:
					movie_title = content.replace("英 文 名", "").strip()
				elif '原　　名' in content:
					movie_title = content.replace("原　　名", "").strip()
				elif '名　　称' in content:
					movie_title = content.replace("名　　称", "").strip()
				
				elif '年　　代' in content:
					release_year = content.replace("年　　代", "").strip()
				elif '时　　间' in content:
					release_year = content.replace("时　　间", "").strip()

				elif '国　　家' in content:
					country = content.replace("国　　家", "").strip()
				elif '国　　别' in content:
					country = content.replace("国　　别", "").strip()
				elif '国家地区' in content:
					country = content.replace("国家地区", "").strip()

				elif '类　　别' in content:
					genres = content.replace("类　　别", "").strip()
				elif '分　　类' in content:
					genres = content.replace("分　　类", "").strip()

				elif '语　　言' in content:
					language = content.replace("语　　言", "").strip()
				elif 'IMDb评分' in content:
					imdb_rate_text = content.replace("IMDb评分", "").strip()
					try:
						imdb_rate = float(imdb_rate_text.split("/")[0].strip())
					except:
						imdb_rate = 0
						pass
				elif 'IMDB评分' in content:
					imdb_rate_text = content.replace("IMDB评分", "").strip()
					try:
						imdb_rate = float(imdb_rate_text.split("/")[0].strip())
					except:
						imdb_rate = 0
						pass
				elif '片　　长' in content:
					runtime = content.replace("片　　长", "").strip()
				elif '时　　长' in content:
					runtime = content.replace("时　　长", "").strip()

				elif '导　　演' in content:
					director = content.replace("导　　演", "").strip()
				elif '主　　演' in content:
					if '简　　介' in content:
						cast = content.split("简　　介", 1)[0].strip()
						storyline = content.split("简　　介", 1)[1].strip()
					else:
						cast = content.replace("主　　演", "").strip()
				elif '演　　员' in content:
					if '简　　介' in content:
						cast = content.split("简　　介", 1)[0].strip()
						storyline = content.split("简　　介", 1)[1].strip()
					else:
						cast = content.replace("演　　员", "").strip()

				elif '简　　介' in content:
					storyline = content.replace("简　　介", "").strip()
				elif '剧　　情' in content:
					storyline = content.replace("剧　　情", "").strip()
				elif '簡  介' in content:
					storyline = content.replace("簡  介", "").strip()

				elif '幕后花絮' in content:
					trivia = content.replace("幕后花絮", "").strip()
				elif '花　　絮' in content:
					trivia = content.replace("花　　絮", "").strip()
				elif '影片评价' in content:
					reviews = content.replace("影片评价", "").strip()
				elif '简　　评' in content:
					reviews = content.replace("简　　评", "").strip()
				elif '获奖情况' in content:
					awards = content.replace("获奖情况", "").strip()

			# Download URL, URL
			if content_text.find(id="Zoom").find('table').find('a').get('thunderrestitle') is not None:
				download_url = str(content_text.find(id="Zoom").find('table').find('a').get('thunderrestitle')).strip();
			else:
				download_url = str(content_text.find(id="Zoom").find('table').find('a').get('href')).strip();

			number_of_success = number_of_success + 1

			# write list
			movie = [dytt_name, dytt_url, publish_date, poster_url, movie_title_translated, movie_title, release_year, country, genres, language, imdb_rate, runtime, director, cast, storyline, trivia, reviews, awards, download_url]
			movie_list.append(movie)

			# # test printing
			# for test in movie:
			# 	print(str(test) + "\n")

		except:
			print("Unexpected error at: " + url)
			# print(sys.exc_info())
			# traceback.print_exc()
			# logging.exception("Error Message: ")
			number_of_failure = number_of_failure + 1
			error_list.append([url, sys.exc_info()])
			pass

		# break

print("Number of Success: " + str(number_of_success))
print("Number of Failure: " + str(number_of_failure))

# write list to csv
movie_list_file = open('dytt_movies.csv', 'w', newline='', encoding='utf-8')
movie_list_file = csv.writer(movie_list_file, quoting=csv.QUOTE_ALL)
movie_list_file.writerows(movie_list)

# write error list to csv
error_list_file = open('error_list.csv', 'w', newline='', encoding='utf-8')
error_list_file = csv.writer(error_list_file, quoting=csv.QUOTE_ALL)
error_list_file.writerows(error_list)