from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from subwidgets.activitytable import ActivityTable
from subwidgets.filterbox import Filter
from subwidgets.sortbox import Sorter

class Overview(QWidget):

    def __init__(self, database):
        super(Overview, self).__init__()

        self.database = database

        # Create Filter Widget
        self.filter = Filter(self.refresh_table)

        # Create Sorter Widget
        self.sorter = Sorter(self.refresh_table)

        # Horizontal Layout: Filter + Sorter
        fr_lyt = QHBoxLayout()
        fr_lyt.addLayout(self.filter.filter_lyt)
        fr_lyt.addLayout(self.sorter.sorter_lyt)
        fr_lyt.addStretch()

        # Load activities from database
        self.activities = self.database.get_activities("All", "date", "DESC")

        # Create Table Widget
        self.table = ActivityTable(self.activities, self.database.latest_activity)
        self.table_lyt = QVBoxLayout()
        self.table_lyt.addWidget(self.table)
 
        # Main Layout
        self.layout = QVBoxLayout()
        self.layout.addLayout(fr_lyt)
        self.layout.addLayout(self.table_lyt)
        self.setLayout(self.layout)
        

    def refresh_table(self):
        self.activities = self.database.get_activities(self.filter.filter_distance(self.filter.filter_cb.currentText()), 
            self.sorter.sorter_cb.currentText(), self.sorter.order_btn_string())

        self.table_lyt.removeWidget(self.table)
        self.table = ActivityTable(self.activities, self.database.latest_activity)
        self.table_lyt.addWidget(self.table)


    def display(self, new_database):
        self.database = new_database
        self.refresh_table()
        self.show()

    
