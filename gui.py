import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QGridLayout, QLineEdit, QMessageBox, QLabel, QTextEdit
from PyQt5.QtGui import QPalette, QColor
from scraper import Scraper
from pd import Pipedrive
from auth import Authentication


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.setWindowTitle("CC 2 PD")
        self.setGeometry(100, 100, 400, 100)
        self.id_input = QLineEdit()
        self.id_input.setReadOnly(True)
        self.id_input.setPlaceholderText("Enter the ID of the project")
        self.id_input.setMaxLength(10)

        self.authentication = Authentication()

        self.log_in_button = QPushButton("Log In")
        self.creds = QPushButton("Change Credentials")

        self.scrape = None
        self.log_in_button.clicked.connect(self.log_in)
        self.creds.clicked.connect(self.change_creds)
        self.id_input.returnPressed.connect(self.scrape_data)
        
        layout = QVBoxLayout()
        layout.addWidget(self.id_input)
        layout.addWidget(self.log_in_button)
        layout.addWidget(self.creds)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.setCentralWidget(container)

    def log_in(self):

        self.scrape = Scraper()
        if self.scrape.driver.current_url == 'https://insight.cmdgroup.com/SearchResult/ProjectSearchResult/Index':
            self.id_input.setReadOnly(False)
            self.log_in_button.setText('Logged In')
            self.log_in_button.setEnabled(False)
        else:
            QMessageBox.warning(self, 'Incorrect Credentials', 'The log in credentials were incorrect, please change')


    def scrape_data(self):
            self.id = self.id_input.text()
            if self.id and len(self.id) == 10:
                self.scrape.load_page(self.id)
                self.title = self.scrape.get_title()
                self.value = self.scrape.get_value()
                self.stage = self.scrape.get_stage()
                self.category = self.scrape.get_category()
                self.address = self.scrape.get_address()
                self.listed = self.scrape.get_listed()
                self.start = self.scrape.get_start()
                self.notes = self.scrape.get_notes()
                self.architect = self.scrape.get_architect()
                self.participants = self.scrape.get_participants()
                self.last_update = self.scrape.get_latest_update()

                self.show_details()
            else:
                QMessageBox.warning(self, 'Invalid input', 'Please enter a valid ID number or log in')
    
    def change_creds(self):

        self.creds_window = CredsWindow()
        self.creds_window.show()

    def show_details(self):
        self.details_window = DetailsWindow(self.title, self.value, self.stage, self.category, self.address, self.listed, self.start, self.notes, self.id, self.scrape, self.architect, self.participants, self.last_update)
        self.details_window.show()

class CredsWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Change Credentials")
        self.setGeometry(100, 100, 300, 200)

        self.authentication = Authentication()
        self.pipedrive = Pipedrive()

        self.new_email = QLineEdit()
        self.new_password = QLineEdit()
        self.new_token = QLineEdit()

        self.new_email.setPlaceholderText("Enter new email")
        self.new_password.setPlaceholderText("Enter new password")
        self.new_token.setPlaceholderText("Enter new token")

        layout = QVBoxLayout()
        layout.addWidget(self.new_email)
        layout.addWidget(self.new_password)
        layout.addWidget(self.new_token)

        self.save_creds = QPushButton("Save Changes")
        self.save_creds.clicked.connect(self.save_changes)

        layout.addWidget(self.save_creds)

        self.setLayout(layout)

    def save_changes(self):
        
        new_email_text = self.new_email.text()
        new_password_text = self.new_password.text()
        new_token_text = self.new_token.text()

        reply = QMessageBox.question(self, 'Save Changes', 'Would you like to save these changes to the credentials?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            key_fields = None
            if new_token_text != '':
                self.pipedrive.client.set_api_token(new_token_text)
                key_fields = self.pipedrive.get_field_keys()
            self.authentication.changes_creds(new_email_text, new_password_text, new_token_text, key_fields)

class DetailsWindow(QWidget):

    def __init__(self, title, value, stage, category, address, listed, start, notes, id, scrape, architect, participants, last_update):
        super().__init__()

        self.pipedrive = Pipedrive()


        self.scrape = scrape
        self.id = id

        try:
            self.deal_id = self.pipedrive.get_deal_id(title)
        except:
            self.deal_id = None

        self.setWindowTitle("Scraped Details")
        self.setGeometry(100, 100, 600, 1200)
        self.setMaximumWidth(500)

        layout = QVBoxLayout()

        text_edit = QTextEdit()
        # text_edit.setReadOnly(True)
        text_edit.setWordWrapMode(True)

        design_team_formatted = ""
        for participant in participants:
            design_team_formatted += "\n".join([f"{key}: {value}" for key, value in participant.items()]) + "\n\n"

        details_text = (
            f"Title:  {title}\n"
            f"ID:  {id}\n"
            f"Architect:  {architect}\n\n"
            f"Estimate Value:  {value}\n"
            f"Stage:  {stage}\n"
            f"Category:  {category}\n"
            f"Address:  {address}\n"
            f"Listed on CC:  {listed}\n"
            f"Start Date:  {start}\n\n"
            f"Latest update: {last_update}\n\n"
            f"Notes:  {notes}\n\n"
            f"Design Team: \n\n"
            f"{design_team_formatted}"
        )

        text_edit.setText(details_text)

        layout.addWidget(text_edit)

        self.create_deal_button = QPushButton("Create New Deal")
        self.task_button = QPushButton("Create Task in Deal")
        self.note_button = QPushButton("Create Note in Deal")
        self.export_button = QPushButton("Export PDF")
        self.watchlist_button = QPushButton("Add to Watch List")

        if self.pipedrive.valid is False:
            self.create_deal_button.setEnabled(False)
            self.task_button.setEnabled(False)
            self.note_button.setEnabled(False)
        elif self.deal_id is None:
            self.task_button.setEnabled(False)
            self.note_button.setEnabled(False)
        
        is_checked = self.scrape.check_if_watchlist()
        if is_checked:
            self.watchlist_button.setEnabled(False)

        layout.addWidget(self.create_deal_button)
        layout.addWidget(self.task_button)
        layout.addWidget(self.note_button)
        layout.addWidget(self.export_button)
        layout.addWidget(self.watchlist_button)

        self.create_deal_button.clicked.connect(lambda: self.create_deal(title, participants, address, id, value, stage, category, listed, start, notes))
        self.task_button.clicked.connect(lambda: self.add_task(value, stage, category, address, listed, start))
        self.note_button.clicked.connect(lambda: self.add_note(notes))
        self.export_button.clicked.connect(self.export_pdf)
        self.watchlist_button.clicked.connect(self.watchlist_project)
        

        self.setLayout(layout)


    def create_deal(self, title, participants, address, id, value, stage, category, listed, start, notes):
        reply = QMessageBox.question(self, 'Create new deal', 'Would you like to make a new deal?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            task_text = (
                f"Estimate Value:  <b>{value}</b><br>"
                f"Stage:  <b>{stage}</b><br>"
                f"Category:  <b>{category}</b><br>"
                f"Address:  <b>{address}</b><br>"
                f"Listed on CC:  <b>{listed}</b><br>"
                f"Start Date:  <b>{start}</b>"
            )
            self.pipedrive.create_new_deal(title, participants, address, id, task_text, notes)
    def export_pdf(self):
        reply = QMessageBox.question(self, 'Export PDF', 'Would you like to see the pdf?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.scrape.get_export(self.id)

    def watchlist_project(self):
        reply = QMessageBox.question(self, 'Add to watch list', 'Would you like to add the project to the watchlist?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.scrape.add_to_watchlist()
            self.watchlist_button.setEnabled(False)

    def add_task(self, value, stage, category, address, listed, start):

        reply = QMessageBox.question(self, 'Create task in deal', 'Would you like to create a task in the deal?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            task_text = (
                f"Estimate Value:  <b>{value}</b><br>"
                f"Stage:  <b>{stage}</b><br>"
                f"Category:  <b>{category}</b><br>"
                f"Address:  <b>{address}</b><br>"
                f"Listed on CC:  <b>{listed}</b><br>"
                f"Start Date:  <b>{start}</b>"
            )

            self.pipedrive.post_task(task_text, self.deal_id)
    
    def add_note(self, notes):

        reply = QMessageBox.question(self, 'Create note in deal', 'Would you like to create a npte in the deal?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.pipedrive.post_note(notes, self.deal_id)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
