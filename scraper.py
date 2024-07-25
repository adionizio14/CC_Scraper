import requests
import sys
from bs4 import BeautifulSoup
import re
import json
from selenium import webdriver
import webbrowser
from PyQt5.QtWidgets import QApplication
import startup



class Scraper:

    def __init__(self) -> None:
        start = startup.Startup()
        self.driver = start.start_driver()

    def load_page(self, id):

        project_url = 'https://insight.cmdgroup.com/Project/Home/ProjectInformation/' + id
        self.driver.get(project_url)
        self.driver.implicitly_wait(10)
        page_source = self.driver.page_source
        self.parsed_html = BeautifulSoup(page_source, 'html.parser')

    def get_title(self):
        
        # Project Title
        project_title_element = self.parsed_html.find('h3', class_='project-header-color')
        if project_title_element:
            project_title = project_title_element.text.strip()
            return project_title
        else:
            print("Project title not found.")

    def get_value(self):
    # Estimate Value
        value_element = self.parsed_html.find('span', id='spnValue')
        if value_element:
            project_value = value_element.text.strip()
            return project_value
        else:
            print("Project value not found.")

    def get_stage(self):
        # Stage
        stage_element = self.parsed_html.find('li', class_='updated-project')
        if stage_element:
            stage_info = stage_element.find('a', class_='material-col-label-med').text.strip()
            return stage_info
        else:
            print("Stage information not found.")

    def get_category(self):
        # Category
        category_element = self.parsed_html.find('div', class_='comapny-list')
        if category_element:
            category_text = category_element.text.strip().split(' ', 1)[-1].strip()
            return category_text
        else:
            print("Category not found")
    
    def get_address(self):
        # Address
        address_element = self.parsed_html.find('span', class_="company-detail-addr-right")
        if address_element:
            address_text = address_element.text.strip()
            return address_text
        else:
            print("Address not found")

    def get_listed(self):
        # Listed on CC
        listed_element = self.parsed_html.find('td', class_="add-details-table-block3")
        if listed_element:
            listed_text = listed_element.text.strip()
            return listed_text
        else:
            print("Listed date not found")
    
    def get_start(self):
        # Start Date
        addition_details = self.parsed_html.find("div", id="box-adddetail")
        start_date_row = addition_details.find('td', string='Start Date:')
        start_date = start_date_row.find_next_sibling('td')
        if start_date:
            return start_date.text
        else:
            print("Start date not found")
        

    #Notes

    def get_notes(self):
        notes_element = self.parsed_html.find("td", class_="x-grid-td x-grid-cell-rowbody")
        notes = notes_element.find("div", class_="x-grid-rowbody")
        if notes:
            notes_text = notes.text.strip()
            return notes_text
        else:
            print("Notes not found")
    
    def get_id(self):
        # Project ID
        id_element = self.parsed_html.find('p', class_="project-id")
        if id_element:
            id_value = id_element.text.strip()
            project_id = re.search(r'\d+', id_value)
            
            if project_id:
                project_id_number = project_id.group()
                return project_id_number
            else:
                print("No project ID number found.")
        else:
            print("ID not found")

    def get_export(self, id):
        data = {
        'exportIdArray': id,
        'exportDataSourceIdArray': id+'|US',
        'exportType': 'PDF',
        'pageName': 'ProjectInformation',
        'sortProperty': '',
        'sortDirection': '',
        'selectedUserId': '00000000-0000-0000-0000-000000000000',
        }

        session = requests.Session()
        for cookie in self.driver.get_cookies():
            session.cookies.set(cookie['name'], cookie['value'])
        
        # Send the POST request
        response = session.post('https://insight.cmdgroup.com/Export/ExportProjectData', data=data)
        
        # Print the response (or handle it as needed)
        response_json = response.content.decode('utf-8')

        # Parse the JSON response
        response_dict = json.loads(response_json)

        # Extract the URL from the response
        pdf_url = response_dict['Uri']

        # Open the URL in a web browser
        webbrowser.open_new_tab(pdf_url)

scrape = Scraper()
while(True):
    id = input("Enter ID or exit: ")
    if id != "exit":
        scrape.load_page(id)
        scrape.get_title()
        scrape.get_value()
        scrape.get_stage()
        scrape.get_category()
        scrape.get_address()
        scrape.get_listed()
        scrape.get_start()
        scrape.get_id()
        export = input("Would you like to see the pdf? (y/n): ")
        if export == "y":
            scrape.get_export()
    else:
        exit()
