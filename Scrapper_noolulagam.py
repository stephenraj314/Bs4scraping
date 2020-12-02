import requests
import csv
from bs4 import BeautifulSoup

base_Url = search_Url = "http://www.noolulagam.com/books/"
book_details = []
all_book_details = []
header=['நூல் பெயர்','வகை','எழுத்தாளர்','பதிப்பகம்', 'Year', 'விலை']
year=''
page = 1
file = open("noolulagam.csv", 'w',encoding='utf-8', newline='')
writer = csv.writer(file)
writer.writerow(header)
while True:
    # fetching source file using requests module
    result = requests.get(search_Url)
    if result.status_code != 200 or page == 1:  # checking if webpage is reachable or page==3771
        print("webpage is unreachable")
        break
    src = result.content
    soup = BeautifulSoup(src, 'lxml')  # converting result.content to soup object parsing using lxml

    # extracting each book details
    for table in soup.findAll('table',
                              attrs={'style': 'border-collapse: collapse; border: 0px solid orange; width :100%'}):
        title = table.find('h4').text
        for row in table.find_all('td', attrs={'valign': 'middle', 'width': '370px'}):
            # extracting each row of book details from previous extraction
            for tr in row.find_all('tr'):
                if (tr.find(text='வகை')) == 'வகை':
                    genre = tr.find('a').text
                elif (tr.find(text='எழுத்தாளர்')) == 'எழுத்தாளர்':
                    author = tr.find('a').text
                elif (tr.find(text='பதிப்பகம்')) == 'பதிப்பகம்':
                    publisher = tr.find('a').text
                elif (tr.find(text=' Year')) == ' Year':
                    year = tr.find('a').text
                elif (tr.find(text='விலை')) == 'விலை':
                    price_td = tr.find_all('td')
                    price = price_td[2].text
                    book_details = [title, genre, author, publisher, year, price]  # storing book details in list
        all_book_details.append(book_details)
    # creating and writing all_book_details into a csv file
    # print(all_book_details)
    with open('noolulagam.csv', 'a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(all_book_details)
        print("{} {} {}".format("page", page, "scraped"))
    page += 1  # incrementing page index for next page
    search_Url = "{}{}".format(base_Url, page)  # joining page index on baseurl
    all_book_details.clear()
    book_details.clear()  # clearing list for next iteration
