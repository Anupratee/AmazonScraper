import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

base_url = 'https://www.amazon.in/s'
params = {
    "k": "bags",
    "crid": "2M096C61O4MLT",
    "qid": "1653308124",
    "sprefix": "ba,aps,283",
    "ref": "sr_pg_1",
}

all_product_data = []

for page_num in range(1, 21):
    params["page"] = page_num
    response = requests.get(base_url, params=params)
    soup = bs(response.content, 'html.parser')

    products = soup.find_all("div", class_="sg-col-inner")

    for product in products:
        product_data = {}

        product_name_elem = product.find("span", class_="a-size-medium")
        if product_name_elem:
            product_data["Product Name"] = product_name_elem.get_text(strip=True)

        product_price_elem = product.find("span", class_="a-price-whole")
        if product_price_elem:
            product_data["Product Price"] = product_price_elem.get_text(strip=True)

        rating_elem = product.find("span", class_="a-icon-alt")
        if rating_elem:
            product_data["Rating"] = rating_elem.get_text(strip=True)

        num_reviews_elem = product.find("span", class_="a-size-base")
        if num_reviews_elem:
            product_data["Number of Reviews"] = num_reviews_elem.get_text(strip=True)

        product_url_elem = product.find("a", class_="a-link-normal")
        if product_url_elem:
            product_data["Product URL"] = product_url_elem.get("href")

        if product_data:
            all_product_data.append(product_data)

for product in all_product_data:
    if "Product URL" in product:
        product_url = product["Product URL"]
        if not product_url.startswith('http'):
            product_url = 'https://www.amazon.in' + product_url
        
        response = requests.get(product_url)
        soup = bs(response.content, 'html.parser')
        
        product_description_elem = soup.find("meta", attrs={"name": "description"})
        if product_description_elem:
            product["Product Description"] = product_description_elem["content"]

        asin_elem = soup.find("th", string="ASIN")
        if asin_elem:
            product["ASIN"] = asin_elem.find_next("td").get_text()

        manufacturer_elem = soup.find("a", {"id": "bylineInfo"})
        if manufacturer_elem:
            product["Manufacturer"] = manufacturer_elem.get_text()

df = pd.DataFrame(all_product_data)
df.to_csv('product_details.csv')

print("CSV file saved successfully.")




