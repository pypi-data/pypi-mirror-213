# Project description
A comprehensive web scraping pipeline for extracting and storing real estate data

### Purpose of the package
+ The primary objective of this package is to provide an efficient solution for web scraping tasks. It has essentially functionalities including link extraction, data extraction, data cleaning, and data storage to database.

### Features
    - Date                      - Bathrooms  
    - Build Year                - Car Parking
    - Floors                    - Ancillary
    - Sitting Rooms             - LandSize
    - Dining Rooms              - Price
    - Bedrooms                  - District
    - Wardrobes                 - Sector


#### Installation
To install the package, run the following command:
``` bash
!pip install WebScrapeX
```

#### Contribution
Contributions are welcome. If you encounter any bugs or have suggestions for improvements, please let me know at inyangel@yahoo.com. Thanks

#### Author
 + This package was developed by Lisa Yvette INYANGE (https://github.com/ILisa250) 

#### License
The package is released under the MIT license. (https://choosealicense.com/licenses/mit/)

#### Dependencies
The package has the following dependencies:

 + Python Decouple: Used for managing settings and configuration.
 + Python Dotenv: Used for loading environment variables from a .env file

#### Scraping URLs

The package supports scraping the following types of real estate listings from the Imali.biz website:

    Apartment for Sale: https://imali.biz/category/1/125/search?pg=
    Apartment for Rent: https://imali.biz/category/0/91/search?pg=
    House for Rent: https://imali.biz/category/0/27/search?pg=
    House for Sale: https://imali.biz/category/0/24/search?pg=

#### Usage example
Here's an example of how to use the WebScrapeX package to scrape, clean, and save real estate data:
``` bash
from WebScrapeX import scrape_clean_save_data

# Specify the link of the real estate type to scrape
url = "https://imali.biz/category/1/125/search?pg="

# Specify the name of the file to save the data (in lowercase)
file_name = "real_estate_data.csv"

# Scrape, clean, and save the data
scrape_clean_save_data(url, file_name)
```