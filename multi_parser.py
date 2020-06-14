import requests
import datetime
import csv
from bs4 import BeautifulSoup
from multiprocessing import Pool
#Парсит за 2.4 минуты


URL = 'https://ekniga.org/'
books_list = []


def main():
    genres_html = get_html(URL + '/zhanry-knig.html')
    all_links = get_all_links(genres_html)
    time, books = parse_books(all_links[0])
    print(books_list, time)


def write_csv(data):
    with open('ekniga.csv', 'a') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow( (data['author'], data['title']))


def get_html(url):
    r = requests.get(url)
    return r.text


def add_book(link):
    item = {}
    print(link)
    page = get_html(link)
    books_soup = BeautifulSoup(page, 'lxml')
    books = books_soup.find_all('div', class_='book-item')
    for book in books:
        item['author'] = book.find(
            'div', class_='author-title'
        ).find('a').string
        item['title'] = book.find(
            'a', class_='book-title'
        ).string
        write_csv(item)


def parse_books(link):
    first = datetime.datetime.now()
    html = get_html(URL + link)
    soup = BeautifulSoup(html, 'lxml')
    last_page = soup.find(
        'span', class_='navigation'
    ).find_all('a')[-1].string
    links = [URL + 'poeziya/' + 'page/' + str(i) + '/'
             for i in range(1, int(last_page) + 1)]
    with Pool(3) as p:
        p.map(add_book, links)
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
