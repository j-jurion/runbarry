import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from screens.insert import Insert 
from screens.overview import Overview
from screens.stats import Statistics
from helperclasses.databasehandler import DatabaseHandler
from helperclasses.constants import Constants


class MainWindow(QMainWindow):
    """
    A class which shows the main window of the application
    
    ...

    Attributes
    ----------
    db_file : str
        File name of the database used in the application

    Methods
    -------
    load_insert()
        Shows insert widget and hides all others
    load_view_all()
        Shows overview widget and hides all others
    load_view_stats()
        Shows stats widget and hides all others
    button_style_selected(button)
        Indicates which screen button is selected
    refresh_db()
        Reloads the database into the application to account for new data
    
    """

    def __init__(self, db_file):
        """
        Parameters
        ----------
        db_file : str
            The database used in the application
        """

        # Intializing window
        super(MainWindow, self).__init__()
        self.setWindowIcon(QIcon(Constants.LOGO_FILENAME))
        self.setWindowTitle(Constants.APP_NAME)
        self.resize(850, 700)

        # Initialize database
        self.db_file = db_file
        self.refresh_db()

        # Button definition
        self.button_insert = QPushButton("Insert")
        self.button_insert.setStyleSheet(f'font : bold ; background-color: {Constants.COLOR_PRIM}')
        self.button_view_all = QPushButton("Activities")
        self.button_stats = QPushButton("Statistics")

        # Button layout
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.button_insert)
        self.button_layout.addWidget(self.button_view_all)
        self.button_layout.addWidget(self.button_stats)

        # Initialize screen widgets
        self.insert_widget = Insert(self.database)
        self.overview_widget = Overview(self.database)
        self.stats_widget = Statistics(self.database)
        self.overview_widget.hide()
        self.stats_widget.hide()

        # Data layout
        self.data_layout = QVBoxLayout()
        self.data_layout.addWidget(self.insert_widget)
        self.data_layout.addWidget(self.overview_widget)
        self.data_layout.addWidget(self.stats_widget)

        # Set main layout
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.button_layout)
        self.layout.addLayout(self.data_layout)
        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

        # Button actions
        self.button_insert.clicked.connect(self.load_insert)
        self.button_view_all.clicked.connect(self.load_view_all)
        self.button_stats.clicked.connect(self.load_stats)
        
    def load_insert(self):
        """
        Shows insert widget and hides all others. 
        Changes screen button styles.
        """
        self.button_style_selected(self.button_insert)
        self.overview_widget.hide()
        self.stats_widget.hide()
        self.insert_widget.display()

    def load_view_all(self):
        """
        Shows overview widget and hides all others. 
        Changes screen button styles.
        """
        self.button_style_selected(self.button_view_all)
        self.refresh_db()
        self.insert_widget.hide()
        self.stats_widget.hide()
        self.overview_widget.display(self.database)

    def load_stats(self):
        """
        Shows stats widget and hides all others. 
        Changes screen button styles.
        """
        self.button_style_selected(self.button_stats)
        self.refresh_db()
        self.overview_widget.hide()
        self.insert_widget.hide()
        self.stats_widget.display(self.database)
    
    def button_style_selected(self, button):
        """ Indicates which screen button is selected """
        self.button_insert.setStyleSheet('')
        self.button_view_all.setStyleSheet('')
        self.button_stats.setStyleSheet('')
        
        button.setStyleSheet(f'font : bold ; background-color: {Constants.COLOR_PRIM}')

    def refresh_db(self):
        """ Reloads the database into the application to account for new data """
        self.database = DatabaseHandler(self.db_file)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = MainWindow(Constants.DB_FILENAME)
    window.show()

    sys.exit(app.exec())