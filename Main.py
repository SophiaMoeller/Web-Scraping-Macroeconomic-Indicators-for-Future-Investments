import schedule
import time
from datetime import datetime
import pandas as pd
from Scraping_Webpages import scrape_ecb_data, scrape_exchange_rates, scrape_euribor_rates, scrape_from_csv


def main():
    """
    Scrape data for the multiple indicators
    :return: Dataframe in a HDF5 file
    """
    csv_file = ("C:/Users/sophi/OneDrive - IU International University of Applied Sciences/IU/Data Quality and Data Wrangling/Websites.csv")
    scrape_from_csv(csv_file)
    website, website1, website2 = scrape_from_csv(csv_file)

    ecb_yield_data = scrape_ecb_data(website)
    exchange_rate_data = scrape_exchange_rates(website1)
    euribor_rates_data = scrape_euribor_rates(website2)

    if not ecb_yield_data:
        print("Warning: 10-year government bond yield data not found.")
        return

    if not exchange_rate_data:
        print("Warning: Exchange rate data not found.")
        return

    if not euribor_rates_data:
        print("Warning: Euribor rates data not found.")
        return


    combined_data = {
        "Scrape_TS": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        **ecb_yield_data,
        **exchange_rate_data,
        **euribor_rates_data,
    }
    print("Combined daily data:", combined_data)

    df_new = pd.DataFrame([combined_data])
    print(df_new)

    hdf_path = (r"C:/Users/sophi/OneDrive - IU International University of Applied Sciences/IU/Data Quality and Data "
                r"Wrangling/my_indicators.h5")
    key_name = "daily_indicators"

    try:
        df_existing = pd.read_hdf(hdf_path, key=key_name)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        print(f"Loaded existing data: {df_existing.shape[0]} rows. Appending new data.")
    except (FileNotFoundError, KeyError):
        df_combined = df_new
        print("No existing data found. Creating new HDF5 dataset.")

    df_combined.to_hdf(
        hdf_path,
        key=key_name,
        mode="w",
        format="table"
        )

    print(f"Appended daily data to {hdf_path} under key '{key_name}'.New total rows: {df_combined.shape[0]}")


if __name__ == "__main__":
    schedule.every().day.at("18:06").do(main)
    while True:
        schedule.run_pending()
        time.sleep(60)



