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
		# url = "http://www.ygdy8.net/html/gndy/dyzz/20150904/48932.html"
		# test url
		try:
			response = urllib.request.urlopen(url).read()
			soup = BeautifulSoup(response, 'html.parser', from_encoding='gbk')
			# print("Starting DYTT Name: " + soup.title.text + " at " + url)
			# Get all fields
			content_text = soup.find(class_='co_content8').find('ul')

			# DYTT Name
			dytt_name = soup.title.text

			# Publish Date at DYTT, Date
			publish_date = content_text.next.strip().replace("发布时间：", "").strip()
			# print("Publish Date at DYTT: " + publish_date)
			# Poster URL, URL
			poster_url = content_text.find(id="Zoom").find_all('p')[0].find('img').get('src')
			# print("Poster URL: " + poster_url)
			# Context List
			context_list = content_text.find(id="Zoom").find('p').get_text('\n', strip=True).split('◎')
			for context in context_list:
				if '译　　名' in context:
					movie_title_translated = context.replace("译　　名", "").strip()
					# print("Mobie Title Translated: " + movie_title_translated)
				elif '片　　名' in context:
					movie_title = context.replace("片　　名", "").strip()
					# print("Mobie Title: " + movie_title)
				elif '年　　代' in context:
					release_year = context.replace("年　　代", "").strip()
					# print("Release Year: " + release_year)
				elif '国　　家' in context:
					country = context.replace("国　　家", "").strip()
					# print("Country: " + country)
				elif '类　　别' in context:
					genres = context.replace("类　　别", "").strip()
					# print("Genres: " + genres)
				elif '语　　言' in context:
					language = context.replace("语　　言", "").strip()
					# print("Language: " + language)
				elif 'IMDb评分' in context:
					imdb_rate_text = context.replace("IMDb评分", "").strip()
					imdb_rate = float(imdb_rate_text.split("/")[0].strip())
					# print("IMDb Rate: " + str(imdb_rate))
				elif '片　　长' in context:
					runtime = context.replace("片　　长", "").strip()
					# print("Runtime: " + runtime)
				elif '导　　演' in context:
					director = context.replace("导　　演", "").strip()
					# print("Director: " + director)
				elif '主　　演' in context:
					if '简　　介' in context:
						cast = context.split("简　　介", 1)[0].strip()
						# print("Cast: \n" + cast)
						storyline = context.split("简　　介", 1)[1].strip()
						# print("Storyline: " + storyline)
					else:
						cast = context.replace("主　　演", "").strip()
						# print("Cast: \n" + cast)
				elif '简　　介' in context:
					storyline = context.replace("简　　介", "").strip()
					# print("Storyline: " + storyline)
				elif '幕后花絮' in context:
					trivia = context.replace("幕后花絮", "").strip()
					# print("Trivia: " + trivia)
				elif '花　　絮' in context:
					trivia = context.replace("花　　絮", "").strip()
					# print("Trivia: " + trivia)
				elif '影片评价' in context:
					reviews = context.replace("影片评价", "").strip()
					# print("Reviews: " + reviews)
				elif '简　　评' in context:
					reviews = context.replace("简　　评", "").strip()
					# print("Reviews: " + reviews)
				elif '获奖情况' in context:
					awards = context.replace("获奖情况", "").strip()
					# print("Awards: " + awards)

			# Download URL, URL
			download_url = str(content_text.find(id="Zoom").find('table').find('a').get('href')).strip();
			# print("Download URL: " + download_url)

			# # Thunder URL, URL
			# # thunder_url = str(content_text.find(id="Zoom").find('table').find('a').get('gxmywwto')).strip();
			# # print("Thunder URL: " + thunder_url)

			number_of_success = number_of_success + 1

			# write list
			movie = [dytt_name, dytt_url, publish_date, poster_url, movie_title_translated, movie_title, release_year, country, genres, language, imdb_rate, runtime, director, cast, storyline, trivia, reviews, awards, download_url]
			movie_list.append(movie)
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