from bs4 import BeautifulSoup
import aiohttp


async def retrieve_news() -> list:
    url = 'https://ct.ufc.br/pt/category/noticias/'

    async with aiohttp.ClientSession() as session:
        res = await session.get(url)
        html_page = await res.text()

        soup = BeautifulSoup(html_page, 'html.parser')
        cards_headers = soup.find_all('div', class_='card-header')

        news = []
        for header in cards_headers:
            publish_date = header.find('span', class_='date')
            news.append({
                'title': header.h1.a.contents[0],
                'url': header.h1.a['href'],
                'publish_date': publish_date.contents[0]
            })
    
        return news