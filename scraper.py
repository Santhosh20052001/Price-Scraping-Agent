import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def get_bestbuy_prices(product_code):
    """
    Fetch sale and original prices for a given Best Buy product code.
    """
    url = f"https://www.bestbuy.com/product/apple-macbook-air-13-inch-laptop-apple-m2-chip-built-for-apple-intelligence-16gb-memory-256gb-ssd-midnight/{product_code}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            print(f"⚠️ Failed to fetch {product_code} (status: {response.status_code})")
            return None, None

        soup = BeautifulSoup(response.text, "html.parser")

        sale_tag = soup.select_one('[data-testid="price-block-customer-price"] span')
        sale_price = sale_tag.text.strip() if sale_tag else None

        original_tag = soup.select_one('[data-lu-target="comp_value"]')
        original_price = original_tag.text.strip() if original_tag else None

        return sale_price, original_price

    except Exception as e:
        print(f" Error fetching {product_code}: {e}")
        return None, None


def scrape_prices_once(input_csv):
    """
    Perform a single scrape pass for all products in the input CSV.
    Returns a DataFrame of the latest prices.
    """
    df_input = pd.read_csv(input_csv)
    df_input = df_input.iloc[:3]

    if "ProductCode" not in df_input.columns:
        raise ValueError("Input CSV must have a column named 'ProductCode'.")

    run_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sale_prices, original_prices = [], []

    for i, code in enumerate(df_input["ProductCode"], start=1):
        print(f"[{i}/{len(df_input)}] Fetching {code}...")
        sale, original = get_bestbuy_prices(code)
        sale_prices.append(sale)
        original_prices.append(original)

    df_run = pd.DataFrame({
        "ProductCode": df_input["ProductCode"],
        "DFN" : df_input["DFN"],
        "SalePrice": sale_prices,
        "OriginalPrice": original_prices,
        "ScrapedAt": run_timestamp
    })
    return df_run




def append_to_csv(df, output_csv):
    """
    Append new scraped data to an output CSV file.
    """
    try:
        df_existing = pd.read_csv(output_csv)
        df_combined = pd.concat([df_existing, df], ignore_index=True)
    except FileNotFoundError:
        df_combined = df

    df_combined.to_csv(output_csv, index=False)
    return df_combined
