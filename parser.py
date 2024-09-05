import requests
from bs4 import BeautifulSoup

def parsing(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    references = []
    news = []

    for i, article in enumerate(soup.find_all('h2', class_='invisionNews_grid_item__title ipsResponsive_hidePhone ipsResponsive_hideTablet ipsResponsive_showDesktop ipsType_pageTitle')):
        if i>=5:
            break
        ref = article.a
        references.append(ref['href'])
        #print(references[i])

    for i in range(0, len(references)):
        #print("\n\nНовость\n\n")
        response = requests.get(references[i])
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.find('h1').text
        #print(title)
        new = [title]

        article = soup.find('section', class_='ipsType_richText')
        text = article.find_all('p')

        for p in text:
            new.append(p.text)
            #print(p.text)
        news.append(new)

    return news