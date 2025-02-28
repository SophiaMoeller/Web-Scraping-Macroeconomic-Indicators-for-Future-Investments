import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_hdf(r"C:/Users/sophi/OneDrive - IU International University of Applied Sciences/IU/Data Quality and Data "
                 r"Wrangling/my_indicators.h5", key="daily_indicators")

print(df.to_string())

# Step 1: Remove duplicate entries for 2025-02-22
df = df.drop_duplicates(subset=['Date'], keep='first')

df['Scrape_TS'] = pd.to_datetime(df['Scrape_TS'], errors='coerce')
df = df.sort_values('Scrape_TS')
df.set_index('Scrape_TS', inplace=True)

d31f = df[df.index >= pd.Timestamp("2025-02-16")]

# Plot 1: ECB 10-year AAA government bond yield
plt.figure(figsize=(10, 5))
plt.plot(df.index, df['ECB_10yr_AAA_Yield'], label="ECB 10yr AAA Yield", color='blue')
plt.title("ECB 10-Year AAA Government Bond Yield")
plt.xlabel("Date")
plt.ylabel("Yield (%)")
plt.legend()
plt.tight_layout()
plt.show()

# Plot 2: Exchange Rate
plt.figure(figsize=(10, 5))
plt.plot(df.index, df['Exchange_Rate'], label="Exchange Rate (EUR/USD)", color='green')
plt.title("EUR/USD Exchange Rate")
plt.xlabel("Date")
plt.ylabel("Exchange Rate")
plt.legend()
plt.tight_layout()
plt.show()

# Plot 3: All Euribor rates together
plt.figure(figsize=(10, 5))
plt.plot(df.index, df['Euribor_1W'], label="Euribor 1W")
plt.plot(df.index, df['Euribor_1M'], label="Euribor 1M")
plt.plot(df.index, df['Euribor_3M'], label="Euribor 3M")
plt.plot(df.index, df['Euribor_6M'], label="Euribor 6M")
plt.plot(df.index, df['Euribor_12M'], label="Euribor 12M")
plt.title("Euribor Interest Rates")
plt.xlabel("Date")
plt.ylabel("Rate (%)")
plt.legend()
plt.tight_layout()
plt.show()


