import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QGridLayout, QLineEdit, QMessageBox, QLabel, QTextEdit
from PyQt5.QtGui import QPalette, QColor
from scraper import Scraper


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.scrape = Scraper()
        self.setWindowTitle("My App")
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Enter the ID of the project")
        self.id_input.setMaxLength(10)
        self.id_input.returnPressed.connect(self.scrape_data)
        
        layout = QVBoxLayout()
        layout.addWidget(self.id_input)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.setCentralWidget(container)

    def scrape_data(self):
            self.id = self.id_input.text()
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

            self.show_details()

    def show_details(self):
        self.details_window = DetailsWindow(self.title, self.value, self.stage, self.category, self.address, self.listed, self.start, self.notes, self.id, self.scrape, self.architect, self.participants)
        self.details_window.show()

class DetailsWindow(QWidget):
    def __init__(self, title, value, stage, category, address, listed, start, notes, id, scrape, architect, participants):
        super().__init__()

        self.scrape = scrape
        self.id = id

        self.setWindowTitle("Scraped Details")
        self.setGeometry(100, 100, 400, 300)
        self.setMaximumWidth(500)

        layout = QVBoxLayout()

        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
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
            f"Notes:  {notes}\n\n"
            f"Design Team: \n"
            f"{design_team_formatted}"
        )

        text_edit.setText(details_text)

        layout.addWidget(text_edit)

        self.export_button = QPushButton("Export PDF")
        self.export_button.clicked.connect(self.export_pdf)
        layout.addWidget(self.export_button)

        self.setLayout(layout)
    def export_pdf(self):
        reply = QMessageBox.question(self, 'Export PDF', 'Would you like to see the pdf?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.scrape.get_export(self.id) 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
