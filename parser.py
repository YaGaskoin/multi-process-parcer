import requests
import datetime
from bs4 import BeautifulSoup
#Парсит 7 минут


URL = 'https://ekniga.org/'


def main():
    genres_html = get_html(URL + '/zhanry-knig.html')
    all_links = get_all_links(genres_html)
    time, books = parse_books(all_links[0])
    print(books, time)


def get_html(url):
    r = requests.get(url)
    return r.text


def parse_books(link):
    first = datetime.datetime.now()
    books_list = []
    html = get_html(URL + link)
    soup = BeautifulSoup(html, 'lxml')
    last_page = soup.find(
        'span', class_='navigation'
    ).find_all('a')[-1].string
    for i in range(1, int(last_page) + 1):
        item = {}
        page = get_html(URL + link + 'page/' + str(i) + '/')
        print(i, URL + link + 'page/' + str(i) + '/')
        books_soup = BeautifulSoup(page, 'lxml')
        books = books_soup.find_all('div', class_='book-item')
        for book in books:
            item['author'] = book.find(
                'div', class_='author-title'
            ).find('a').string
            item['title'] = book.find(
                'a', class_='book-title'
            ).string
            books_list.append(item)
    time = datetime.datetime.now() - first
    return time, books_list


def get_all_links(html):
    soup = BeautifulSoup(html, 'lxml')
    genres = soup.find_all('div', class_='cat-title')
    links = []
    for genre in genres:
        a = genre.find('a')
        if a.string == 'Поэзия':
            links.append(a.get('href'))
            break


    return links


if __name__ == '__main__':
    main()
