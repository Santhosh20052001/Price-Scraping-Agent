# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# from datetime import datetime

# def get_bestbuy_prices(product_code):
#     """
#     Fetch sale and original prices for a given Best Buy product code.
#     """
#     url = f"https://www.bestbuy.com/product/apple-macbook-air-13-inch-laptop-apple-m2-chip-built-for-apple-intelligence-16gb-memory-256gb-ssd-midnight/{product_code}"
#     headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

#     try:
#         response = requests.get(url, headers=headers, timeout=15)
#         if response.status_code != 200:
#             print(f"⚠️ Failed to fetch {product_code} (status: {response.status_code})")
#             return None, None

#         soup = BeautifulSoup(response.text, "html.parser")

#         sale_tag = soup.select_one('[data-testid="price-block-customer-price"] span')
#         sale_price = sale_tag.text.strip() if sale_tag else None

#         original_tag = soup.select_one('[data-lu-target="comp_value"]')
#         original_price = original_tag.text.strip() if original_tag else None

#         return sale_price, original_price

#     except Exception as e:
#         print(f" Error fetching {product_code}: {e}")
#         return None, None


# def scrape_prices_once(input_txt):
#     """
#     Perform a single scrape pass for all products in the input TXT file.
#     Returns a DataFrame of the latest prices.
#     """
#     df_input = pd.read_csv(input_txt, sep="\t")
#     df_input = df_input.iloc[:3]

#     if "ProductCode" not in df_input.columns:
#         raise ValueError("Input TXT must have a column named 'ProductCode'.")

#     run_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     sale_prices, original_prices = [], []

#     for i, code in enumerate(df_input["ProductCode"], start=1):
#         print(f"[{i}/{len(df_input)}] Fetching {code}...")
#         sale, original = get_bestbuy_prices(code)
#         sale_prices.append(sale)
#         original_prices.append(original)

#     df_run = pd.DataFrame({
#         "ProductCode": df_input["ProductCode"],
#         "DFN": df_input["DFN"],
#         "SalePrice": sale_prices,
#         "OriginalPrice": original_prices,
#         "ScrapedAt": run_timestamp
#     })
#     return df_run





# def append_to_csv(df, output_csv):
#     """
#     Append new scraped data to an output CSV file.
#     """
#     try:
#         df_existing = pd.read_csv(output_csv)
#         df_combined = pd.concat([df_existing, df], ignore_index=True)
#     except FileNotFoundError:
#         df_combined = df

#     df_combined.to_csv(output_csv, index=False)
#     return df_combined

# # import requests
# # from bs4 import BeautifulSoup
# # import pandas as pd
# # from datetime import datetime

# # def get_bestbuy_prices(product_code):
# #     """
# #     Fetch sale and original prices for a given Best Buy product code.
# #     """
# #     url = f"https://www.bestbuy.com/site/{product_code}"
# #     headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# #     try:
# #         response = requests.get(url, headers=headers, timeout=15)
# #         response.raise_for_status()

# #         soup = BeautifulSoup(response.text, "html.parser")
# #         sale_tag = soup.select_one('[data-testid="price-block-customer-price"] span')
# #         sale_price = sale_tag.text.strip() if sale_tag else None

# #         original_tag = soup.select_one('[data-lu-target="comp_value"]')
# #         original_price = original_tag.text.strip() if original_tag else None

# #         return sale_price, original_price

# #     except Exception as e:
# #         print(f"⚠️ Error fetching {product_code}: {e}")
# #         return None, None


# # def read_txt_to_df(input_txt):
# #     """
# #     Reads a text file with tab or comma-separated values:
# #     Example format:
# #     Apple MacBook Air 13, JJGCQ8RH7G
# #     HP OmniBook X, JJGQJRKGQ4
# #     Lenovo Yoga Slim 7i, JJGSHCGSCW
# #     """
# #     try:
# #         df = pd.read_csv(input_txt, sep=None, engine='python', header=None, names=["DFN", "ProductCode"])
# #         return df
# #     except Exception as e:
# #         raise ValueError(f"Error reading {input_txt}: {e}")


# # def scrape_prices_once(input_txt):
# #     """
# #     Perform a single scrape pass for all products listed in the TXT file.
# #     Returns a DataFrame of the latest prices.
# #     """
# #     df_input = read_txt_to_df(input_txt)

# #     run_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# #     sale_prices, original_prices = [], []

# #     for i, row in df_input.iterrows():
# #         code = row["ProductCode"]
# #         print(f"[{i+1}/{len(df_input)}] Fetching {code}...")
# #         sale, original = get_bestbuy_prices(code)
# #         sale_prices.append(sale)
# #         original_prices.append(original)

# #     df_run = pd.DataFrame({
# #         "DFN": df_input["DFN"],
# #         "ProductCode": df_input["ProductCode"],
# #         "SalePrice": sale_prices,
# #         "OriginalPrice": original_prices,
# #         "ScrapedAt": run_timestamp
# #     })
# #     return df_run


# # def append_to_txt(df, output_txt):
# #     """
# #     Append new scraped data to an output TXT file (tab-separated for readability).
# #     """
# #     try:
# #         df_existing = pd.read_csv(output_txt, sep="\t")
# #         df_combined = pd.concat([df_existing, df], ignore_index=True)
# #     except FileNotFoundError:
# #         df_combined = df

# #     df_combined.to_csv(output_txt, sep="\t", index=False)
# #     return df_combined
import pandas as pd
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def get_bestbuy_prices(product_code):
    """
    Fetch sale and original prices for a given Best Buy product code.
    """

    
    url = f"https://www.bestbuy.com/product/asus-vivobook-s-15-15-6-3k-oled-laptop-copilot-pc-snapdragon-x-elite-32gb-memory-1tb-ssd-cool-silver/{product_code}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        sale_tag = soup.select_one('[data-testid="price-block-customer-price"] span')
        sale_price = sale_tag.text.strip() if sale_tag else None

        original_tag = soup.select_one('[data-lu-target="comp_value"]')
        original_price = original_tag.text.strip() if original_tag else None

        return sale_price, original_price

    except Exception as e:
        print(f"⚠️ Error fetching {product_code}: {e}")
        return None, None


def scrape_prices_once(input_file):
    """
    Perform a single scrape pass for all products listed in a TXT or CSV file.
    TXT should have lines in the format: ProductCode,DFN
    CSV should have columns: ProductCode, DFN
    """
    # --- Detect file type ---
    if input_file.endswith(".csv"):
        df_input = pd.read_csv(input_file)
    elif input_file.endswith(".txt"):
        with open(input_file, "r") as f:
            lines = [line.strip() for line in f if line.strip()]
        if lines[0].lower().startswith("productcode"):
            lines = lines[1:]  # skip header if present

        codes, dfns = [], []
        for line in lines:
            parts = line.split(",", 1)
            if len(parts) == 2:
                codes.append(parts[0].strip())
                dfns.append(parts[1].strip())
            else:
                codes.append(parts[0].strip())
                dfns.append("Unknown")

        df_input = pd.DataFrame({"ProductCode": codes, "DFN": dfns})
    else:
        raise ValueError("Unsupported file type. Please use .csv or .txt")

    # --- Check required columns ---
    if "ProductCode" not in df_input.columns:
        raise ValueError("Input TXT must have a column named 'ProductCode'.")

    # --- Scrape ---
    run_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sale_prices, original_prices = [], []

    for i, row in df_input.iterrows():
        code = row["ProductCode"]
        print(f"[{i+1}/{len(df_input)}] Fetching {code}...")
        sale, original = get_bestbuy_prices(code)
        sale_prices.append(sale)
        original_prices.append(original)

    df_run = pd.DataFrame({
        "ProductCode": df_input["ProductCode"],
        "DFN": df_input["DFN"],
        "SalePrice": sale_prices,
        "OriginalPrice": original_prices,
        "ScrapedAt": run_timestamp
    })

    return df_run
