from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from subwidgets.activitytable import ActivityTable
from subwidgets.filterbox import Filter
from subwidgets.sortbox import Sorter

class Overview(QWidget):
    """
    A widget which shows a complete list of activities on the database

    ...

    Attributes
    ----------
    database : DatabaseHandler
        Current database handler
    
    Methods
    -------
    refresh_table()
        Redefines the list of activities and recreates the table 
        with the current database handler
    display(new_database)
        Shows widget using new_database as the current database handler

    """

    def __init__(self, database):
        """
        Parameters
        ----------
        database : DatabaseHandler
            Current database handler
        """
        super(Overview, self).__init__()

        # Define database handler
        self.database = database

        # Create Filter Widget
        self.filter = Filter(self.refresh_table)

        # Create Sorter Widget
        self.sorter = Sorter(self.refresh_table)

        # Horizontal Layout: Filter & Sorter
        fr_lyt = QHBoxLayout()
        fr_lyt.addLayout(self.filter.filter_lyt)
        fr_lyt.addLayout(self.sorter.sorter_lyt)
        fr_lyt.addStretch()

        # Load activities from database
        self.activities = self.database.get_activities("All", "date", "DESC")

        # Create Table Widget
        self.table = ActivityTable(self.activities, self.database.latest_activity, self)
        self.table_lyt = QVBoxLayout()
        self.table_lyt.addWidget(self.table)
 
        # Main Layout
        self.layout = QVBoxLayout()
        self.layout.addLayout(fr_lyt)
        self.layout.addLayout(self.table_lyt)
        self.setLayout(self.layout)
        

    def refresh_table(self):
        """
        Redefines the list of activities and recreates the table 
        with the current database handler
        """
        self.activities = self.database.get_activities(self.filter.filter_distance(self.filter.filter_cb.currentText()), 
            self.sorter.sorter_cb.currentText(), self.sorter.order_btn_string())

        self.table_lyt.removeWidget(self.table)
        self.table = ActivityTable(self.activities, self.database.latest_activity, self)
        self.table_lyt.addWidget(self.table)
    
    def remove_activity(self, activity):
        self.database.remove_activity(activity)
        self.refresh_table()


    def display(self, new_database):
        """
        Shows widget using new_database as the current database handler
        
        Parameters
        ----------
        new_database : DatabaseHandler
            New database handler
        """
        self.database = new_database
        self.refresh_table()
        self.show()

    
