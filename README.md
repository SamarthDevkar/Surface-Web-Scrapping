# Surface-Web-Scrapping

This project is designed to scrape article data from specified news sites using automated scripts developed in Python with Selenium, BeautifulSoup, and Pandas. The scraped data includes article titles, publication dates, descriptions, URLs, and content. Data is stored in a structured database for further analysis or application usage.

**Features**
**Automated Web Scraping**: Uses Selenium for dynamic content scraping and BeautifulSoup for parsing HTML content.
**Data Management**: Stores scraped data in a structured format using a custom DataManager (DM) module to handle database operations.
**Filtering and Duplication Check**: Only new data is scraped based on the last entry date, ensuring no redundant entries.
**Scalability**: Supports multiple scrapers with similar configurations for various websites.
Project Structure
**main_scraper.py**: Main script that initializes Selenium, performs scraping, and processes the scraped data.
**DataManager.py**: Module responsible for database connection, fetching the latest date entry, and inserting new data.
**README.md**: Project documentation.

Requirements: Update the MongoDb Atlas connection string in Data Manager & CVE Manager. Install the required libraries and you are good to go.
