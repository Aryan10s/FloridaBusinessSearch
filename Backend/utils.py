import requests
from bs4 import BeautifulSoup
import yaml
import os
import psycopg2
from generate_log import *
from dotenv import load_dotenv


load_dotenv()

POSTGRESQL_CONNECTION_STRING = os.getenv("POSTGRESQL_CONNECTION_STRING")


config_path = os.getcwd()
app_configurations = yaml.safe_load(
    open(config_path + "/config/app_configurations.yaml"))

first_level_html = app_configurations['first_level_html']


initial_path = app_configurations['initial_path']

def save_html_from_url(url, filename):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(response.text)
            logger.info(f"HTML content saved to {filename}")
            return True
        else:
            logger.exception(f"Failed to retrieve HTML content from {url}. Status code: {response.status_code}")
            return False
    except Exception as e:
        logger.exception(f"An error occurred: {e}")
        return False

def extract_url_from_html(filename, td_data):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('table')
        if table:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                print("data= " + td_data)
                if len(cells) >= 1 and cells[0].text.strip().startswith(td_data):
                    # print("Inside")
                    # print(cells[0])
                    link = cells[0].find('a')
                    if link:
                        url = link.get('href')
                        logger.info(f"URL associated with '{td_data}': {url}")
                        return url
        logger.exception(f"No URL found for '{td_data}'")
    except Exception as e:
        logger.exception(f"An error occurred: {e}")



def getURL(query):
    try:
        first_level = config_path + first_level_html
        url =f"https://search.sunbiz.org/Inquiry/CorporationSearch/SearchResults/EntityName/{query}/Page1?searchNameOrder={query}"
        filename = first_level
        save_html_from_url(url, filename)
        needed_path = extract_url_from_html(filename, query)
        final_url = initial_path + needed_path
        logger.info(final_url)
        return final_url, True
    except Exception as e:
        logger.exception("Error occured: " + str(e))
        return "", False

def insert_into_db(file,query):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            html = f.read()
        soup = BeautifulSoup(html, 'html.parser')

        filing_information_div = soup.find('div', class_='detailSection filingInformation')
        spans = filing_information_div.find_all('span')
        needed_spans = spans[1].find_all('span')
        document_number = needed_spans[0].text.strip().replace("'","''")
        date_of_registration = needed_spans[2].text.strip().replace("'","''")
        state_of_registration = needed_spans[3].text.strip().replace("'","''")
        main_div = soup.find('div',class_="searchResultDetail")
        inside_principal_div = main_div.find_all('div', class_= "detailSection")
        name_div = main_div.find_all('span')
        name = name_div[12].text.strip()
        query = query.replace("'","''")
        address = inside_principal_div[4].find_all('div')[0].text.strip()
        principal_name_and_address = f'{name} {address}'
        principal_name_and_address = principal_name_and_address.replace("'","''")
        tables = soup.find_all('table')
        req_table = tables[3]
        available_documents = ""
        if req_table:
            rows = req_table.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if len(cells)>=1 and cells[0].text.strip():
                    available_documents += cells[0].text.strip()
                    available_documents += ", "

        available_documents = available_documents.rstrip(', ').replace("'","''")
        logger.info("Business Name: " + query)
        logger.info("Document Number: " + document_number)
        logger.info("Date of Registration: " + date_of_registration)
        logger.info("State of Registration: " + state_of_registration)
        logger.info("Principal Name and Address: " + principal_name_and_address)
        logger.info("Available Documents: " + available_documents)
        # insert data to db
        conn = psycopg2.connect(POSTGRESQL_CONNECTION_STRING)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Businesses (
            business_name VARCHAR PRIMARY KEY,
            document_number VARCHAR,
            date_of_registration VARCHAR,
            state_of_registration VARCHAR,
            principal_name_and_address VARCHAR,           
            available_documents VARCHAR
        );
        """)
        conn.commit()
        cursor.execute(f"""
    INSERT INTO Businesses (business_name, document_number, date_of_registration,state_of_registration,principal_name_and_address,available_documents) VALUES ('{query}', '{document_number}', '{date_of_registration}', '{state_of_registration}', '{principal_name_and_address}' ,'{available_documents}');
        """)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        logger.error("Error occured: " + str(e))
        return False

def getFromDB(business_name):
    try:
        conn = psycopg2.connect(POSTGRESQL_CONNECTION_STRING)
        cursor = conn.cursor()
        business_name = business_name.replace("'","''")
        cursor.execute(f"SELECT * FROM Businesses where business_name='{business_name}';")
        output  = cursor.fetchall()
        columnNames = [column[0] for column in cursor.description]
        data = []
        for record in output:
            data.append(dict(zip(columnNames, record)))
        cursor.close()
        conn.close()
        return data,True

    except Exception as e:
        logger.error("Error occured: " + str(e))
        return [],False

def getBusinessNames():
    try:
        conn = psycopg2.connect(POSTGRESQL_CONNECTION_STRING)
        cursor = conn.cursor()
        cursor.execute(f"SELECT business_name FROM Businesses;")
        conn.commit()
        output  = cursor.fetchall()
        columnNames = [column[0] for column in cursor.description]
        data = []
        for record in output:
            data.append(dict(zip(columnNames, record)))

        cursor.close()
        conn.close()
        return data,True
    except Exception as e:
        logger.error("Error occured: " + str(e))
        return [],False