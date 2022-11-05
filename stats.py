from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from bestefforttable import BestEffortTable
from barchart import BarChart
from monthlytable import MonthlyTable

class Statistics(QWidget):

    def __init__(self, database):
        super(Statistics, self).__init__()

        self.database = database

        self.layout = QVBoxLayout()

        # Create Best Effort Table
        self.best_effort = BestEffortTable(self.database)
        self.layout.addWidget(self.best_effort)

        # Create a Bar Chart
        #self.bar_chart = BarChart(self.database)
        #self.layout.addWidget(self.bar_chart)

        # Create Monthly Table
        self.monthly_table = MonthlyTable(self.database)
        self.layout.addWidget(self.monthly_table)

        self.setLayout(self.layout)
        


    def refresh_stats(self):
        self.layout.removeWidget(self.best_effort)
        self.layout.removeWidget(self.monthly_table)
        self.best_effort = BestEffortTable(self.database)
        self.monthly_table = MonthlyTable(self.database)
        self.layout.addWidget(self.best_effort)
        self.layout.addWidget(self.monthly_table)


    def display(self, new_database):
        self.database = new_database
        self.refresh_stats()
        self.show()      
