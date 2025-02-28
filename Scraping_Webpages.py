import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd


def scrape_from_csv(csv_path):
    df = pd.read_csv(csv_path, sep=';')

    website = None
    website1 = None
    website2 = None

    for i, row in df.iterrows():
        url = row["URL"]
        print(f"Scraping: {url}")

        if i == 0:
            website = url
        elif i == 1:
            website1 = url
        elif i == 2:
            website2 = url
        else:
            print("Warning: More than 3 URLs detected; ignoring extra rows.")
            break

    return website, website1, website2


def scrape_ecb_data(website):
    """
    Scraping function for the ECB 10-year AAA government bond yield.

    :return:dictionary with the indicator name, the date, and the yield
    """

    #Extracts and parses HTML of the ECB webpage
    page = requests.get(website)
    contents = page.content
    soup = BeautifulSoup(contents, 'html.parser')

    #Cearting Loop that looks for all Box classes in the HTML and extracts the yield and the corresponding date
    boxes = soup.find_all("div", class_="box")

    yield_value = None
    yield_date = None

    for box in boxes:
        first_div = box.find("div")
        if first_div and "10-year AAA government bond yield" in first_div.get_text(strip=True):
            value_div = box.find("div", class_="value")
            if value_div:
                yield_text = value_div.get_text(strip=True)
                yield_value = float(yield_text.replace("%", ""))

            all_divs = box.find_all("div")
            if len(all_divs) >= 3:
                yield_date_str = all_divs[2].get_text(strip=True)
                yield_date = datetime.strptime(yield_date_str, "%d %B %Y")

            return {
                "Date": yield_date,
                "ECB_10yr_AAA_Yield": yield_value
            }

    print("10-year AAA government bond yield:", yield_value)
    print("Date:", yield_date)


def scrape_exchange_rates(website1):
    """
    Scraping function for the Euro Dollar exchange rate.

    :return:dictionary with the indicator name, the date, and the EUR/USD exchange rate
    """

    #Extracts and parses HTML of the tagesschau webpage
    page1 = requests.get(website1)
    contents1 = page1.content
    soup1 = BeautifulSoup(contents1, 'html.parser')

    #Finds the main container for the exchange rate
    prices_div = soup1.find("div", class_="prices")
    if not prices_div:
        print("No 'prices' div found.")
        return None

    #Extracts the exchange rate
    rate_span = prices_div.find("span", class_="price")
    if rate_span:
        rate_text = rate_span.get_text(strip=True)
        rate_text = rate_text.replace("$", "").strip()
    else:
        rate_text = None

    #Extracts the change of the exchange rate
    change_span = prices_div.find("span", class_="change")
    if change_span:
        change_text = change_span.get_text(strip=True)
    else:
        change_text = None

    #Extracts the date
    date_span = prices_div.find("span", class_="date")
    if date_span:
        date_raw = date_span.get_text(strip=True)
        try:
            date_val = datetime.strptime(date_raw, "%d.%m.%Y, %H:%M:%S Uhr")
        except ValueError:
            date_val = date_raw
    else:
        date_val = None

    return {
        "Exchange_Rate": rate_text,
        "Change": change_text,
        "Date": date_val
    }


def scrape_euribor_rates(website2):
    """
    Scraping function for the Euribor interest rates.

    :return:dictionary with the indicator name and the Euribor interest rates for 1 week, 1 month, 3 months,
    6 months, and 12 months
    """

    #Extracts and parses HTML of the Euribor Rates webpage
    page = requests.get(website2)
    contents = page.content
    soup2 = BeautifulSoup(contents, 'html.parser')

    #Extracts the date
    date_div = soup2.find("div", class_="euribor-date")
    published_date = None
    if date_div:
        date_text = date_div.get_text(strip=True)
        date_text_clean = date_text.replace("Stand: ", "").strip()
        try:
            dt_obj = datetime.strptime(date_text_clean, "%d.%m.%Y")
            published_date = dt_obj.strftime("%Y-%m-%d")
        except ValueError:
            published_date = date_text_clean

    #Defines a mapping from the textual label to the desired dictionary key
    euribor_mapping = {
        "Euribor 1 Woche": "Euribor_1W",
        "Euribor 1 Monat": "Euribor_1M",
        "Euribor 3 Monate": "Euribor_3M",
        "Euribor 6 Monate": "Euribor_6M",
        "Euribor 12 Monate": "Euribor_12M"
    }

    euribor_data = {}

    #Extracts the Euribor interest rates
    rows = soup2.find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 2:
            continue

        label_text = cols[0].get_text(strip=True)

        rate_text = cols[1].get_text(strip=True)

        if label_text in euribor_mapping:
            rate_value_str = rate_text.replace("%", "").strip()
            rate_value_str = rate_value_str.replace(",", ".")
            rate_value = float(rate_value_str)

            key_name = euribor_mapping[label_text]
            euribor_data[key_name] = rate_value

    return euribor_data
