# Web-Scraping Macroeconomic Indicators for Future Investments
## Project Overview
This project automates the collection of macroeconomic indicators from various websites. The scraped data is saved in an HDF5 file and used for time series analysis and visualization.
## Motivation
In today's fast-paced economy, timely and accurate information is crucial for making informed decisions. While some organizations rely solely on past performance to predict future outcomes (Verstraete et al., 2020), those operating in dynamic markets benefit from considering key macroeconomic indicators. Research shows that these indicators can provide valuable insights into future company performance (Verstraete et al., 2020).

Macroeconomic factors play a particularly important role in investment and financing decisions (Mokhova & Zinecker, 2014). By leveraging up-to-date economic data, organizations can make better strategic choices about when and how to invest. This project aims to automate the collection of relevant economic indicators, enabling data-driven decision-making.

## Data and Features 
- Daily automated scraping of key indicators such as:
  - ECB 10-year AAA government bond yield
  - EUR/USD exchange rate
  - Various Euribor rates
- Data storage in HDF5 format for efficient retrieval and analysis 
- Time series visualization using matplotlib

## How to Use This Repository 
Install required Python libraries:

```pip install -r requirements.txt```

Run the file ```Main.py``` to start the web scraping script. Run the ```Analysis.py``` file for visualizing the indicators over time.

## References
- Verstraete, G., Aghezzaf, E. H., & Desmet, B. (2020). A leading macroeconomic indicators’ based framework to automatically generate tactical sales forecasts. Computers & Industrial Engineering, 139, 106169. 
- Mokhova, N., & Zinecker, M. (2014). Macroeconomic factors and corporate capital structure. Procedia - Social and Behavioral Sciences, 110, 530–540.