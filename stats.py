from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from bestefforttable import BestEffortTable
from barchart import BarChartWidget
from monthlytable import MonthlyTable

class Statistics(QWidget):

    def __init__(self, database):
        super(Statistics, self).__init__()

        self.database = database

        self.layout = QVBoxLayout()

        self.hori_layout = QHBoxLayout()

        # Create Best Effort Table
        self.best_effort = BestEffortTable(self.database)
        self.hori_layout.addWidget(self.best_effort)

        # Create Monthly Table
        self.monthly_table = MonthlyTable(self.database)
        self.hori_layout.addWidget(self.monthly_table)

        self.layout.addLayout(self.hori_layout)

        # Create a Bar Chart
        self.bar_chart  = BarChartWidget(self.database)
        self.layout.addWidget(self.bar_chart )


        self.setLayout(self.layout)
        


    def refresh_stats(self):
        self.hori_layout.removeWidget(self.best_effort)
        self.hori_layout.removeWidget(self.monthly_table)
        self.best_effort = BestEffortTable(self.database)
        self.monthly_table = MonthlyTable(self.database)
        self.hori_layout.addWidget(self.best_effort)
        self.hori_layout.addWidget(self.monthly_table)

        self.layout.removeWidget(self.bar_chart)
        self.bar_chart = BarChartWidget(self.database)
        self.layout.addWidget(self.bar_chart)


    def display(self, new_database):
        self.database = new_database
        self.refresh_stats()
        self.show()      
