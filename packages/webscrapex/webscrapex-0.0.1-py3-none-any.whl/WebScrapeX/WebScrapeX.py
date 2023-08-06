# A collection of functions 
## Links exctraction
## Data extraction
## Data cleaning
## Data saving to DB

import requests #to send HTTP requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import re

# Modules to connect with postgress
import psycopg2
import psycopg2.extras
import csv

# Modules to run automatically
import schedule # To handle scheduling tasks.
import time as tm # For time-related operations

# To manage configurations
from decouple import config
from dotenv import load_dotenv

import os


run_count = 0  # Counter for tracking the number of times the script has run
def scrape_clean_save_data(url, filename):
    global run_count
    global current_time
    run_count += 1
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

    
    #function to extract links
    #.........................
    def get_real_estate_data(url):
        """ function to extract links

        Params:
        .......
        url: links

        Usage:
        ......
        >>> from web_data_extraction import scrape_clean_save_data
        scrape_clean_save_data("link/url", "filename")
        
        """
        # Empty list to store links
        Links = []
        #Looping through the pages
        for page in range(1,11):
            # Headers used to specify how the HTTP request should be processed by the server. 
            # i.e - User-Agent header specifying the user agent string that should be sent with the request,
            # - Accept header specifying the types of content that the client can handle.
            headers = {'Accept-Encoding': 'gzip, deflate, sdch','Accept-Language': 'en-US,en;q=0.8','Upgrade-Insecure-Requests': '1',
                       'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                       'Cache-Control': 'max-age=0','Connection': 'keep-alive',}      
        
            # Requesting desired URL
            try:
                response_text = requests.get(url + str(page), headers=headers, allow_redirects=False).text
                # Parse the HTML content
                soup = BeautifulSoup(response_text, 'html.parser')

                # Loop through every house's link
                for div in soup.findAll('div', {'class': 'item-list'}):
                    # Find the link for the current property
                    link = div.find('a').attrs['href']
                    # Keep the links in the Links list
                    Links.append("https://imali.biz" + link)  
            except requests.exceptions.RequestException as e:
                print(f"An error occurred while fetching data: {e}")
        # Create a DataFrame from the list
        imali_data = pd.DataFrame({f'{filename}_links': Links})
        imali_data.to_csv(f"{filename}_links.csv")

    
    #function to extract data from links
    #...................................
    def extract_data():
        links = pd.read_csv(f"{filename}_links.csv", usecols=[1])
        # List to store extracted data from all the links
        all_data_list = []
        # Iterating through links in the df
        for i in links[f'{filename}_links']:
            headers = {'accept': 'application/json',}
            # Requesting desired URL
            response_text = requests.get(i,headers=headers, allow_redirects=False).text 
            # Parsing the response text
            soup = BeautifulSoup(response_text, 'html.parser')

            # List to keep extracted data
            each_data_list = []
            # Loop through each div with class "col-md-4" (Price & Location)
            for i in soup.findAll('div', {'class':"col-md-4"}):
                # Find the price
                price = i.find('p').text.replace("\t","").strip()
                # Keep the price
                each_data_list.append(price)
                # Find the district
                district = i.findAll('p')
                # Keep the district name
                district = district if district else "None"
                each_data_list.append(district)
                # Find the sector name
                sector = i.findAll('p')
                # Keep the sector name
                each_data_list.append(sector)

            # Loop through each span with class "date" (Date) & to find date posted
            for div in soup.findAll('span', {"class":"date"}):
                Date = div
                # Keep the date posted
                each_data_list.append(Date.text.strip())
            # Iterating through each div with class "media-body"
            for div in soup.findAll('div', {'class': "media-body"}):
                # Find the specifications
                specifications_element = div.find('span', {'class': "media-heading"})
                # Check if specifications are empty
                if specifications_element is not None:
                    # Keep the specifications
                    specifications = specifications_element.text.strip()
                else:
                   # Append zero if no data is extracted
                    specifications = "0"
                # Add specifications to each_data_list
                each_data_list.append(specifications)
            # Keep details of all data    
            all_data_list.append(each_data_list)
            
        #Create dataframe to keep details
        columns = ["Price", "District","Sector","Date", "Ref_number","Build_Year","Floors","Sitting_Rooms","Dining_Rooms","Bedrooms","Wardrobes","Bathrooms","Car_Parking","Ancillary","Plot_number","LandSize"]
        all_data_df = pd.DataFrame(all_data_list, columns = columns)
        # Replace empty fields with "0"
        all_data_df.fillna("0", inplace=True)
        # Reorder columns
        all_data_df = all_data_df[["Ref_number","Build_Year","Floors","Sitting_Rooms","Dining_Rooms","Bedrooms","Wardrobes","Bathrooms","Car_Parking","Ancillary","Plot_number","LandSize", "Price", "District","Sector","Date"]]

        # Save the dataframe to csv file
        all_data_df.to_csv(f"{filename}_Details.csv") 
    

    # Function to clean and save properties' data
    #............................................
    def clean_and_save_data():
        properties = pd.read_csv(f"{filename}_Details.csv")
        # Set the 'Date' column as the index & convert it to datetime format
        properties = properties.set_index(pd.to_datetime(properties['Date']))

        # Drop unwanted cols from the df
        properties = properties.drop(['Ref_number', 'Plot_number', "Unnamed: 0", "Date"], axis =1)
        
        # Clean respective columns accordingy
        properties['LandSize'] = [int(area.replace("m2","").replace(",","")) for area in properties['LandSize']]
        properties['District'] = properties['District'].str.split('District:</strong>').str[1].str.split('<').str[0]
        properties['Sector'] = properties['Sector'].str.split('Sector:</strong>').str[1].str.split('<').str[0]
        properties['Price'] = properties['Price'].str.replace(r'[^0-9]', '', regex=True)

        # Save the clean df to a CSV file
        properties.to_csv(f"{filename}_Clean_data.csv")
        
        
    # Function to create table to postgres
    #..................................
    current_directory = os.getcwd()
    csv_file_path = os.path.join(current_directory, f'{filename}_Clean_data.csv')
    def infer_column_types(csv_file_path):
        # Read data from CSV file and infer column types
        with open(csv_file_path, 'r') as csv_file:
            reader = csv.reader(csv_file)
            header = next(reader)  # Get the header row
            data_sample = next(reader)  # Get a sample row of data

        column_types = []
        for column, value in zip(header, data_sample):
            # Check for specific column names
            if column == "LandSize" or column == "Price":
                column_types.append('BIGINT')
            # Check for specific column names
            elif value.isdigit():
                column_types.append('INTEGER')
            elif value.replace('.', '', 1).isdigit():
                column_types.append('DECIMAL')
            elif value.strip():
                try:
                    datetime.strptime(value, '%Y-%m-%d')  # Check for date values
                    column_types.append('DATE')
                except ValueError:
                    column_types.append('VARCHAR(100)')
            else:
                column_types.append('VARCHAR(100)')

        return header, column_types 


    # Function to create DB and insert data to the created table in DB
    #................................................................. 
    def insert_data_from_csv_to_imali_table(csv_file_path):
        # Load the .env file
        env_path = os.path.abspath('.env')
        load_dotenv(env_path)
        database_host = config("DATABASE_HOST")
        database_name = config("DATABASE_NAME")
        database_user = config("DATABASE_USER")
        database_password = config("DATABASE_PASSWORD")
        # Establish a connection to the PostgreSQL database
        conn = psycopg2.connect(
            host=database_host,
            user=database_user,
            password=database_password
        )

        # Create a cursor object to interact with the database
        cur = conn.cursor()

        # Create the database if it doesn't exist
        cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname= '{database_name}'")
        database_exists = cur.fetchone()

        if not database_exists:
            cur.execute(f"CREATE DATABASE {database_name}")
            conn.commit()
            print(f"Database {database_name} created successfully.")

        # Close the cursor and current connection
        cur.close()
        conn.close()

        # Connect to the Trial database
        conn = psycopg2.connect(
            host=database_host,
            database=database_name,
            user=database_user,
            password=database_password
        )

        # Create a new cursor object to interact with the Trial database
        cur = conn.cursor()

        # Check if the table exists
        cur.execute(f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = %s)", (filename,))
        table_exists = cur.fetchone()[0]

        # Create the table if it doesn't exist
        if not table_exists:
            header, column_types = infer_column_types(csv_file_path)

            # Construct the CREATE TABLE query
            create_table_query = f"CREATE TABLE {filename} ("
            for column_name, column_type in zip(header, column_types):
                create_table_query += f"{column_name} {column_type}, "
            create_table_query = create_table_query.rstrip(", ") + ")"

            cur.execute(create_table_query)
            conn.commit()
            print(f"Table {filename} created successfully.")
        else:
            print(f"Table {filename} already exists. Skipping table creation.")
            # Update the table if it exists
            with open(csv_file_path, 'r') as csv_file:
                reader = csv.reader(csv_file)
                next(reader)  # Skip header row
                imali_data = list(reader)
            # Sort the data by date
            sorted_data = sorted(imali_data, key=lambda x: x[0], reverse=True)

            # Insert new rows into the table if they don't already exist
            insert_query = f"""
                        INSERT INTO {filename} (Date, Build_Year, Floors, Sitting_Rooms, Dining_Rooms, Bedrooms, Wardrobes, Bathrooms, Car_Parking, Ancillary, LandSize, Price, District, Sector)
                        SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                        WHERE NOT EXISTS (
                            SELECT 1 FROM {filename} WHERE Date = %s AND Build_Year = %s AND Floors = %s AND Sitting_Rooms = %s
                            AND Dining_Rooms = %s AND Bedrooms = %s AND Wardrobes = %s AND Bathrooms = %s
                            AND Car_Parking = %s AND Ancillary = %s AND LandSize = %s AND Price = %s
                            AND District = %s AND Sector = %s
                        )
                    """
            data_inserted = False  # Flag variable to track new row insertion
            for data in sorted_data:
                cur.execute(insert_query, [*data, *data])
                if cur.rowcount > 0:
                    conn.commit()
                    if not data_inserted:
                        print("New row(s) inserted:\n")
                        data_inserted = True
                    print(data)
            if not data_inserted:
                print("No new data was inserted.")

            conn.commit()
            print(f"Table {filename} is up to date.\n")
            # Close the cursor and connection
        cur.close()
        conn.close()

        
    # Automation
    # ..........
    # ..........
    def automation():
        scrape_clean_save_data(url, filename)

        # Schedule to run every 5 seconds
        schedule.every(5).seconds.do(automation)

        # Run the scheduler loop
        while True:
            schedule.run_pending()
            tm.sleep(30)  # Optional delay between iterations
        
  
    # Function to combine all the functions into one
    #...............................................
    def combined_function():
        # URL of the real estate listings page on 'imali.biz', with the page number left blank 
        imali_data = get_real_estate_data(url)
        extract_data()
        clean_and_save_data()
        # Path to the CSV file
        insert_data_from_csv_to_imali_table(csv_file_path)
        automation()
    
    # Determine the appropriate plural form for the word "time"
    times_word = "times" if run_count > 1 else "time"
    print("\033[1mExecution count: {}\033[0m {} | \033[1mCurrent time: {}\033[0m".format(run_count, times_word, current_time))
    # Call the combined function
    combined_function()      