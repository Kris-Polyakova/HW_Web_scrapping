import requests
import bs4
from fake_headers import Headers
import re
from tqdm import tqdm
from pprint import pprint

KEYWORDS = ['дизайн', 'фото', 'web', 'python']

def get_keywods_list(date, title, link, text, KEYWORDS, scpapp_habr):
    for word in tqdm(KEYWORDS):
        if word in title.lower() or text.lower():
            article_info = f'<{date}> – <{title}> – <{link}>'
            if article_info not in scpapp_habr:
                scpapp_habr.append(article_info)

def get_link_text(link, headers):
    response = requests.get(link, headers=headers)
    soup = bs4.BeautifulSoup(response.text, features='lxml')
    article_body = soup.find('div', class_='article-formatted-body article-'
                             'formatted-body article-formatted-body_version-2')
    text = re.sub('<.*?>','', str(article_body))
    return text 
               
def get_scpapp_habr():
    headers = Headers(browser='chrome', os='win').generate()
    url = 'https://habr.com/ru/articles/'
    response = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(response.text, features='lxml')
    articles_list = soup.find_all(class_='tm-articles-list__item')

    scpapp_habr = []
    for article in tqdm(articles_list):
        link = 'https://habr.com' + article.find(class_=
                                                 'tm-title__link')['href']
        date = article.find(class_='tm-article-datetime-published tm-article-'
                            'datetime-published_link').find('time')['title']
        title = article.find(class_='tm-title tm-title_h2').text
        text = get_link_text(link, headers)
        get_keywods_list(date, title, link, text, KEYWORDS, scpapp_habr)
    return scpapp_habr

if __name__ == '__main__':
    pprint(get_scpapp_habr())   





