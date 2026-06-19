import requests
from bs4 import BeautifulSoup
import pandas as pd

pd.set_option('display.max_columns', None)       # Показывать все колонки
pd.set_option('display.max_colwidth', None)      # Не обрезать текст внутри ячеек
pd.set_option('display.width', 1000)

base_url = "https://quotes.toscrape.com"
current_url = "https://quotes.toscrape.com"

response = requests.get(base_url)
all_data = []

while current_url:
    print(f"Парсим страницу: {current_url}")
    response = requests.get(current_url)
    if response.status_code != 200:
        print(f"Ошибка загрузки страницы: {response.status_code}")
    elif response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        quote_blocks = soup.find_all('div', class_='quote')
        for quote in quote_blocks:
            text = quote.find('span', class_='text')
            author = quote.find('small', class_='author')
            tag_list = quote.find_all('a', class_='tag')
            clean_tags = [tag.text for tag in tag_list]
            all_data.append({
                "quote": text.text,
                "author": author.text,
                "tags": " ".join(clean_tags),
            })
            next_button = soup.find('li', class_='next')
            if next_button:
                next_page_url = next_button.find('a')['href']
                current_url = base_url + next_page_url
            else:
                current_url = None

df = pd.DataFrame(all_data)
df.to_csv('quotes.csv', index=False, encoding='utf-8-sig')
print("Data saved successfully!")