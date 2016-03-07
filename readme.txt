1. python read list of movies

number of pages
loop each page: http://www.ygdy8.net/html/gndy/dyzz/list_23_1.html
in each page, loop each link
in each link,
get: link, submitted date, picture, content by string handling, download link, thunder link
write into csv

2. data loader, load csv into salesforce

3. scheduled Apex job, running every week get latest movies into salesforce

4. new UI


Fields:

Publish Date at DYTT, Date
Poster URL, URL
Movie Title, Text(50)
Movie Title in Chinese, Text(50)
Release Year, Text(20)
Country, Text(50)
Genres, Text(50)
Language, Text(50)
IMBb Rate, Number(2, 1)
Runtime, Text(20)
Director, Text(50)
Cast, Text Area(Long)
Storyline, Text Area(Long)
Trivia, Text Area(Long)
Reviews, Text Area(Long)
Awards, Text Area(Long)
Download URL, URL
Thunder URL, URL