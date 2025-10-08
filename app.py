# import streamlit as st
# import pandas as pd
# import time
# from datetime import datetime
# from openai import AzureOpenAI
# from scraper import scrape_prices_once, append_to_csv

# # --- Streamlit Setup ---
# st.set_page_config(page_title="Best Buy Price Agent", layout="wide")
# st.title(" Real-Time Best Buy Price Agent")

# # Sidebar controls
# input_csv = st.sidebar.text_input(" Input CSV path", "bestbuy_uids.csv")
# output_csv = st.sidebar.text_input(" Output CSV path", "tracked_prices.csv")
# interval = st.sidebar.number_input("Scrape interval (seconds)", min_value=10, max_value=600, value=30)
# run_agent = st.sidebar.toggle(" Start AI Agent", value=False)

# # Placeholders for UI updates
# data_placeholder = st.empty()
# log_box = st.empty()

# # --- Azure OpenAI Client Setup ---
# client = AzureOpenAI(
#     api_key="4ZFVVpEKatcC56WUrOmTfrwOMOsrxcviTp4HJvAjEXTfSRGBvUR7JQQJ99AJACYeBjFXJ3w3AAABACOGZOFC",
#     azure_endpoint="https://fordmustang.openai.azure.com/",
#     api_version="2024-02-01",
# )
# DEPLOYMENT_NAME = "Brick"  # your Azure OpenAI deployment name

# # --- Function: Analyze with LLM ---
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

# # --- Main Agent Loop ---
# if run_agent:
#     st.sidebar.success("Agent is running...")
#     iteration = 1

#     while True:
#         try:
#             # Scrape Best Buy prices
#             df_latest = scrape_prices_once(input_csv)
#             append_to_csv(df_latest, output_csv)

#             # Display latest scraped data
#             data_placeholder.dataframe(df_latest, use_container_width=True)

#             # Analyze using LLM
#             analysis = analyze_with_llm(df_latest)
#             log_box.markdown(
#                 f"### LLM Analysis — Run #{iteration}\n"
#                 f"**Time:** {datetime.now().strftime('%H:%M:%S')}  \n"
#                 f"{analysis}"
#             )

#         except Exception as e:
#             log_box.error(f"Error: {e}")

#         iteration += 1
#         time.sleep(interval)
# else:
#     st.info("🟢 Toggle **Start AI Agent** to begin real-time scraping.")


# import streamlit as st
# import pandas as pd
# from datetime import datetime
# from openai import AzureOpenAI
# from scraper import scrape_prices_once, append_to_csv
# import altair as alt
# from streamlit_autorefresh import st_autorefresh

# # --- Streamlit Setup ---
# st.set_page_config(page_title="Best Buy Price Agent", layout="wide")
# st.title("📈 Real-Time Best Buy Price Agent")

# # --- Sidebar controls ---
# input_csv = st.sidebar.text_input("Input CSV path", "bestbuy_uids.csv", key="input_csv")
# output_csv = st.sidebar.text_input("Output CSV path", "tracked_prices.csv", key="output_csv")
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
#     st_autorefresh(interval=interval*1000, key="autorefresh")

#     try:
#         # Scrape
#         df_latest = scrape_prices_once(input_csv)
#         append_to_csv(df_latest, output_csv)

#         # --- Show table first ---
#         table_placeholder.dataframe(df_latest, use_container_width=True)

#         # --- Then show cards ---
#         display_cards(output_csv)

#         # --- Then show LLM analysis ---
#         analysis = analyze_with_llm(df_latest)
#         log_box.markdown(
#             f"### LLM Analysis\n**Time:** {datetime.now().strftime('%H:%M:%S')}\n{analysis}"
#         )

#     except Exception as e:
#         log_box.error(f"Error: {e}")

# else:
#     st.info("🟢 Toggle **Start AI Agent** to begin real-time scraping.")

import streamlit as st
import pandas as pd
import time
from datetime import datetime
from openai import AzureOpenAI
from scraper import scrape_prices_once, append_to_csv
import altair as alt

# --- Streamlit Setup ---
st.set_page_config(page_title="Best Buy Price Agent", layout="wide")
st.title("📈 Real-Time Best Buy Price Agent")

# --- Sidebar controls ---
input_csv = st.sidebar.text_input("Input file path", "bestbuy_uids.txt", key="input_csv")
output_csv = st.sidebar.text_input("Output CSV path", "tracked_prices.csv", key="output_csv")
interval = st.sidebar.number_input("Scrape interval (seconds)", min_value=10, max_value=600, value=30, key="interval")
run_agent = st.sidebar.toggle("Start AI Agent", value=False, key="run_agent")

# Placeholders
table_placeholder = st.empty()
cards_placeholder = st.empty()
log_box = st.empty()

# --- Azure OpenAI Setup ---
client = AzureOpenAI(
    api_key="4ZFVVpEKatcC56WUrOmTfrwOMOsrxcviTp4HJvAjEXTfSRGBvUR7JQQJ99AJACYeBjFXJ3w3AAABACOGZOFC",
    azure_endpoint="https://fordmustang.openai.azure.com/",
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



