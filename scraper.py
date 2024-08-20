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

        """
        Initalizes scraper by starting and returning the web driver.
        """

        start = startup.Startup()
        self.driver = start.start_driver()

    def load_page(self, id):
        
        """
        Method to retrieve the parsed html of the desired project page.
        """

        project_url = 'https://insight.cmdgroup.com/Project/Home/ProjectInformation/' + id
        self.driver.get(project_url)
        self.driver.implicitly_wait(10)
        page_source = self.driver.page_source
        self.parsed_html = BeautifulSoup(page_source, 'html.parser')

    def get_title(self):

        """
        Method to get the title of the project.
        """

        project_title_element = self.parsed_html.find('h3', class_='project-header-color')
        if project_title_element:
            project_title = project_title_element.text.strip()
            return project_title
        else:
            print("Project title not found.")

    def get_value(self):

        """
        Method to get the value of the project.
        """

        value_element = self.parsed_html.find('span', id='spnValue')
        if value_element:
            project_value = value_element.text.strip()
            return project_value
        else:
            print("Project value not found.")

    def get_stage(self):

        """
        Method to get the stage of the project.
        """
                
        stage_element = self.parsed_html.find('li', class_='updated-project')
        if stage_element:
            stage_info = stage_element.find('a', class_='material-col-label-med').text.strip()
            return stage_info
        else:
            print("Stage information not found.")

    def get_category(self):

        """
        Method to get the category of the project.
        """

        category_element = self.parsed_html.find('div', class_='comapny-list')
        if category_element:
            category_text = category_element.text.strip().split(' ', 1)[-1].strip()
            return category_text
        else:
            print("Category not found")
    
    def get_address(self):

        """
        Method to get the address of the project.
        """

        address_element = self.parsed_html.find('span', class_="company-detail-addr-right")
        if address_element:
            address_text = address_element.text.strip()
            return address_text
        else:
            print("Address not found")

    def get_listed(self):

        """
        Method to get the listed date of the project.
        """

        listed_element = self.parsed_html.find('td', class_="add-details-table-block3")
        if listed_element:
            listed_text = listed_element.text.strip()
            return listed_text
        else:
            print("Listed date not found")
    
    def get_start(self):

        """
        Method to get the start date of the project.
        """

        addition_details = self.parsed_html.find("div", id="box-adddetail")
        start_date_row = addition_details.find('td', string='Start Date:')
        start_date = start_date_row.find_next_sibling('td')
        if start_date:
            return start_date.text
        else:
            print("Start date not found")

    def get_notes(self):

        """
        Method to get the notes of the project.
        """

        notes_element = self.parsed_html.find("td", class_="x-grid-td x-grid-cell-rowbody")
        notes = notes_element.find("div", class_="x-grid-rowbody")
        if notes:
            notes_text = notes.text.strip()
            return notes_text
        else:
            print("Notes not found")
    
    def get_id(self):

        """
        Method to get the ID of the project.
        """

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
    
    def get_architect(self):

        """
        Method to get the architect of the project.
        """

        architect_element = self.parsed_html.find_all('span', class_="company-detail-addr-right")[2]
        
        if architect_element:
            architect = architect_element.text
            if len(architect) > 0:
                return architect
            else:
                return "N/A"
        else:
            print("No architect found")

    def get_participants(self):

        """
        Method to get all of the partcipants of the project.
        """

        design_team = self.parsed_html.find('div', id='grdProjectParticipants-body')
        tables = design_team.find_all('table')
        extracted_data = []
        for table in tables:
            headers = []
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['th', 'td'])
                cell_text = [cell.get_text(strip=True) for cell in cells]
                extracted_data.append(cell_text)
        keys = ["Company Role", "Company Name", "Contact Name", "Contact Status", "Street Address", "Phone", "Email", "Fax Number"]
        dict_list = [dict(zip(keys, entry)) for entry in extracted_data]
        return dict_list

    def get_export(self, id):

        """
        Method to get the pdf file of the project.
        """

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

    def add_to_watchlist(self,id):

        print("idk")