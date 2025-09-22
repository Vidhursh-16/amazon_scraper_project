import requests
import time
from bs4 import BeautifulSoup
import json
import random

# Example Amazon search query
SEARCH_QUERY = "laptop"
URL = f"https://www.amazon.in/s?k={SEARCH_QUERY.replace(' ', '+')}"

# Rotate headers to mimic real browsers
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
]

headers = {
    "User-Agent": random.choice(USER_AGENTS),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

# Polite delay before making request
time.sleep(2)

# Try fetching Amazon
response = requests.get(URL, headers=headers)

products = []

if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    print("Page fetched successfully ✅")
    print("Page Title:", soup.title.text)

    ignore_keywords = ["Results", "Trending now", "Sponsored"]

    for product in soup.find_all("div", {"data-asin": True}):
        try:
            img_tag = product.find("img", class_="s-image")
            img_url = img_tag["src"] if img_tag else None

            title_tag = product.find("h2")
            title = title_tag.get_text(strip=True) if title_tag else None

            price_tag = product.find("span", class_="a-offscreen")
            price = price_tag.get_text(strip=True) if price_tag else None

            rating_tag = product.find("span", class_="a-icon-alt")
            rating = rating_tag.get_text(strip=True) if rating_tag else None

            review_tag = product.find("span", class_="a-size-base")
            reviews = review_tag.get_text(strip=True) if review_tag else None

            if title and price and len(title) > 5 and not any(kw in title for kw in ignore_keywords):
                products.append({
                    "title": title,
                    "price": price,
                    "rating": rating,
                    "reviews": reviews,
                    "image": img_url
                })

        except Exception as e:
            print(f"Skipping product due to error: {e}")

else:
    print(f"⚠️ Failed to fetch Amazon, status: {response.status_code}")
    print("➡️ Loading mock product data instead...")

    # Mock fallback data
    products = [
        {
            "title": "Mock Laptop Pro 14",
            "price": "₹79,999",
            "rating": "4.5 out of 5",
            "reviews": "120",
            "image": "https://via.placeholder.com/200x150.png?text=Laptop+1"
        },
        {
            "title": "Mock Gaming Laptop X",
            "price": "₹1,29,999",
            "rating": "4.7 out of 5",
            "reviews": "220",
            "image": "https://via.placeholder.com/200x150.png?text=Laptop+2"
        },
        {
            "title": "Mock Budget Laptop",
            "price": "₹39,999",
            "rating": "4.0 out of 5",
            "reviews": "95",
            "image": "https://via.placeholder.com/200x150.png?text=Laptop+3"
        }
    ]

# Save products to JSON
with open("products.json", "w", encoding="utf-8") as f:
    json.dump(products, f, indent=4, ensure_ascii=False)

print(f"✅ Saved {len(products)} products to products.json 🎉")

# Show first 3 products as test
for p in products[:3]:
    print(p)
