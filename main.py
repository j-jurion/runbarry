import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from home import Home 
from insert import Insert 
from overview import Overview
from stats import Statistics
from databasehandler import DatabaseHandler





class MainWindow(QMainWindow):
    def __init__(self, db_file):
        super(MainWindow, self).__init__()
        self.setWindowTitle("RunBarry")
        self.resize(800, 600)

        self.db_file = db_file
        self.refresh_db()

        # Button definition
        self.button_home = QPushButton("Home")
        self.button_home.setStyleSheet('font : bold ; background-color: lightblue')
        self.button_insert = QPushButton("Insert")
        self.button_view_all = QPushButton("Activities")
        self.button_stats = QPushButton("Statistics")

        # Button layout
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.button_home)
        self.button_layout.addWidget(self.button_insert)
        self.button_layout.addWidget(self.button_view_all)
        self.button_layout.addWidget(self.button_stats)

        # Initialize widgets
        self.home_widget = Home()
        self.insert_widget = Insert(self.database)
        self.overview_widget = Overview(self.database)
        self.stats_widget = Statistics(self.database)
        self.insert_widget.hide()
        self.overview_widget.hide()
        self.stats_widget.hide()

        # Data layout
        self.data_layout = QVBoxLayout()
        self.data_layout.addWidget(self.home_widget)
        self.data_layout.addWidget(self.insert_widget)
        self.data_layout.addWidget(self.overview_widget)
        self.data_layout.addWidget(self.stats_widget)

        # Screen layout
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.button_layout)
        self.layout.addLayout(self.data_layout)
        

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

        # Button actions
        self.button_home.clicked.connect(self.load_home)
        self.button_insert.clicked.connect(self.load_insert)
        self.button_view_all.clicked.connect(self.load_view_all)
        self.button_stats.clicked.connect(self.load_stats)
        
    def load_home(self):
        self.button_style_selected(self.button_home)
        self.overview_widget.hide()
        self.insert_widget.hide()
        self.stats_widget.hide()
        self.home_widget.show()

    def load_insert(self):
        self.button_style_selected(self.button_insert)
        self.home_widget.hide()
        self.overview_widget.hide()
        self.stats_widget.hide()
        self.insert_widget.display()

    def load_view_all(self):
        self.button_style_selected(self.button_view_all)
        self.refresh_db()
        self.home_widget.hide()
        self.insert_widget.hide()
        self.stats_widget.hide()
        self.overview_widget.display(self.database)

    def load_stats(self):
        self.button_style_selected(self.button_stats)
        self.refresh_db()
        self.home_widget.hide()
        self.overview_widget.hide()
        self.insert_widget.hide()
        self.stats_widget.display(self.database)
    
    def button_style_selected(self, button):
        self.button_home.setStyleSheet('')
        self.button_insert.setStyleSheet('')
        self.button_view_all.setStyleSheet('')
        self.button_stats.setStyleSheet('')
        
        button.setStyleSheet('font : bold ; background-color: lightblue')

    def refresh_db(self):
        self.database = DatabaseHandler(self.db_file)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = MainWindow("activities.db")
    window.show()

    sys.exit(app.exec())