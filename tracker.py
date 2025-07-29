import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9"
}

def get_product_price(url):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        title_elem = soup.find("div", class_="product_main").find("h1")
        price_elem = soup.find("p", class_="price_color")

        if not title_elem or not price_elem:
            return {"error": "Elemento non trovato"}

        title = title_elem.get_text(strip=True)
        price_text = price_elem.get_text(strip=True).replace("£", "")
        price = float(price_text)

        return {
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'title': title,
            'price': price
        }

    except Exception as e:
        return {"error": str(e)}

def save_price_data(data, folder="data"):
    os.makedirs(folder, exist_ok=True)
    filename = f"{data['title'].replace(' ', '_')}.csv"
    path = os.path.join(folder, filename)
    df = pd.DataFrame([data])
    df.to_csv(path, mode='a', header=not os.path.exists(path), index=False, quoting=1)
    return filename
