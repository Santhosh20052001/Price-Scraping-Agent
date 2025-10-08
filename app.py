# import streamlit as st
# import pandas as pd
# import time
# from datetime import datetime
# from openai import AzureOpenAI
# from scraper import scrape_prices_once, append_to_csv
# import altair as alt
# # --- Streamlit Setup ---
# st.set_page_config(page_title="Best Buy Price Agent", layout="wide")
# st.title("📈 Real-Time Best Buy Price Agent")
# # --- Sidebar controls ---
# # --- Static CSV paths ---
# input_csv = "bestbuy_uids.csv"    # Input CSV stored in your repo
# output_csv = "tracked_prices.csv"
# interval = st.sidebar.number_input("Scrape interval (seconds)", min_value=10, max_value=600, value=30, key="interval")
# run_agent = st.sidebar.toggle("Start AI Agent", value=False, key="run_agent")
# # Placeholders
# table_placeholder = st.empty()
# cards_placeholder = st.empty()
# log_box = st.empty()
# # --- Azure OpenAI Setup ---
# client = AzureOpenAI(
#     api_key="4ZFVVpEKatcC56WUrOmTfrwOMOsrxcviTp4HJvAjEXTfSRGBvUR7JQQJ99AJACYeBjFXJ3w3AAABACOGZOFC",
#     azure_endpoint="https://fordmustang.openai.azure.com/",
#     api_version="2024-02-01",
# )
# DEPLOYMENT_NAME = "Brick"
# # --- Function: LLM Analysis ---
# def analyze_with_llm(df: pd.DataFrame):
#     if df.empty:
#         return "No price data available for analysis."

#     csv_text = df.to_csv(index=False)
#     prompt = f"""
#     You are monitoring live laptop prices from Best Buy US.

#     Here are the latest scraped prices (USD):
#     {csv_text}

#     Provide a concise analysis:
#     - Average, lowest, and highest price
#     - Detect any major price changes or outliers
#     - Suggest the next ideal scrape interval (seconds)
#     """

#     response = client.chat.completions.create(
#         model=DEPLOYMENT_NAME,
#         messages=[
#             {"role": "system", "content": "You are a precise e-commerce price analyst."},
#             {"role": "user", "content": prompt},
#         ],
#         temperature=0.3,
#     )

#     return response.choices[0].message.content.strip()
# # --- Function: Display cards ---
# def display_cards(output_csv):
#     try:
#         df_combined = pd.read_csv(output_csv)
#     except FileNotFoundError:
#         cards_placeholder.info("No data yet. Wait for first scrape.")
#         return

#     if df_combined.empty:
#         cards_placeholder.info("No data available.")
#         return

#     # Last 2 timestamps per DFN
#     df_combined_sorted = df_combined.sort_values("ScrapedAt")
#     df_last_two = df_combined_sorted.groupby("DFN").tail(2)
#     df_unique = df_last_two["DFN"].unique()

#     cols_per_row = 3
#     for i, dfn in enumerate(df_unique):
#         if i % cols_per_row == 0:
#             cols = cards_placeholder.columns(cols_per_row)

#         df_dfn = df_last_two[df_last_two["DFN"] == dfn].sort_values("ScrapedAt")
#         current_price = df_dfn["SalePrice"].iloc[-1]

#         chart = alt.Chart(df_dfn).mark_line(point=True).encode(
#             x=alt.X("ScrapedAt", title="Time", axis=alt.Axis(labelAngle=-45)),
#             y=alt.Y("SalePrice", title="Price (USD)"),
#             tooltip=["ScrapedAt", "SalePrice"]
#         ).properties(width=200, height=150)

#         with cols[i % cols_per_row]:
#             st.markdown(f"**{dfn}**")
#             st.metric("Current Price", f"${current_price}")
#             st.altair_chart(chart)
# # --- Main Loop ---
# if run_agent:
#     st.sidebar.success("Agent is running...")
#     iteration = 1

#     while True:
#         try:
#             # Scrape
#             df_latest = scrape_prices_once(input_csv)
#             append_to_csv(df_latest, output_csv)

#             # --- Show table first ---
#             table_placeholder.dataframe(df_latest, use_container_width=True)

#             # --- Then show cards ---
#             display_cards(output_csv)

#             # --- Then show LLM analysis ---
#             analysis = analyze_with_llm(df_latest)
#             log_box.markdown(
#                 f"### LLM Analysis — Run #{iteration}\n**Time:** {datetime.now().strftime('%H:%M:%S')}\n{analysis}"
#             )

#         except Exception as e:
#             log_box.error(f"Error: {e}")

#         iteration += 1
#         time.sleep(interval)

# else:
#     st.info("🟢 Toggle **Start AI Agent** to begin real-time scraping.")





import streamlit as st
import pandas as pd
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import altair as alt
from openai import AzureOpenAI

# --- Streamlit Setup ---
st.set_page_config(page_title="Best Buy Price Agent", layout="wide")
st.title("📈 Real-Time Best Buy Price Agent")

# --- Sidebar controls ---
input_csv = "bestbuy_uids.csv"    # Input CSV stored in your repo
output_csv = "tracked_prices.csv"
interval = st.sidebar.number_input(
    "Scrape interval (seconds)", min_value=10, max_value=600, value=30, key="interval"
)
run_agent = st.sidebar.toggle("Start AI Agent", value=False, key="run_agent")

# Placeholders
table_placeholder = st.empty()
cards_placeholder = st.empty()
log_box = st.empty()

# --- Azure OpenAI Setup ---
client = AzureOpenAI(
    api_key="YOUR_AZURE_API_KEY",
    azure_endpoint="https://YOUR_AZURE_ENDPOINT/",
    api_version="2024-02-01",
)
DEPLOYMENT_NAME = "Brick"


# --- Function: LLM Analysis ---
def analyze_with_llm(df: pd.DataFrame):
    if df.empty:
        return "No price data available for analysis."

    csv_text = df.to_csv(index=False)
    prompt = f"""
    You are monitoring live laptop prices from Best Buy US.

    Here are the latest scraped prices (USD):
    {csv_text}

    Provide a concise analysis:
    - Average, lowest, and highest price
    - Detect any major price changes or outliers
    - Suggest the next ideal scrape interval (seconds)
    """

    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": "You are a precise e-commerce price analyst."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content.strip()


# --- Function: Display cards ---
def display_cards(output_csv):
    try:
        df_combined = pd.read_csv(output_csv)
    except FileNotFoundError:
        cards_placeholder.info("No data yet. Wait for first scrape.")
        return

    if df_combined.empty:
        cards_placeholder.info("No data available.")
        return

    # Last 2 timestamps per DFN
    df_combined_sorted = df_combined.sort_values("ScrapedAt")
    df_last_two = df_combined_sorted.groupby("DFN").tail(2)
    df_unique = df_last_two["DFN"].unique()

    cols_per_row = 3
    for i, dfn in enumerate(df_unique):
        if i % cols_per_row == 0:
            cols = cards_placeholder.columns(cols_per_row)

        df_dfn = df_last_two[df_last_two["DFN"] == dfn].sort_values("ScrapedAt")
        current_price = df_dfn["SalePrice"].iloc[-1]

        chart = alt.Chart(df_dfn).mark_line(point=True).encode(
            x=alt.X("ScrapedAt", title="Time", axis=alt.Axis(labelAngle=-45)),
            y=alt.Y("SalePrice", title="Price (USD)"),
            tooltip=["ScrapedAt", "SalePrice"]
        ).properties(width=200, height=150)

        with cols[i % cols_per_row]:
            st.markdown(f"**{dfn}**")
            st.metric("Current Price", f"${current_price}")
            st.altair_chart(chart)


# --- Function: Best Buy scraping ---
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
    df_input = df_input.iloc[:3]  # Limit for testing

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
        "DFN": df_input["DFN"],
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


# --- Main Loop ---
if run_agent:
    st.sidebar.success("Agent is running...")
    iteration = 1

    while True:
        try:
            # Scrape
            df_latest = scrape_prices_once(input_csv)
            append_to_csv(df_latest, output_csv)

            # --- Show table first ---
            table_placeholder.dataframe(df_latest, use_container_width=True)

            # --- Then show cards ---
            display_cards(output_csv)

            # --- Then show LLM analysis ---
            analysis = analyze_with_llm(df_latest)
            log_box.markdown(
                f"### LLM Analysis — Run #{iteration}\n**Time:** {datetime.now().strftime('%H:%M:%S')}\n{analysis}"
            )

        except Exception as e:
            log_box.error(f"Error: {e}")

        iteration += 1
        time.sleep(interval)

else:
    st.info("🟢 Toggle **Start AI Agent** to begin real-time scraping.")
