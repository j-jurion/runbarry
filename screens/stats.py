from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from subwidgets.bestefforttable import BestEffortTable
from subwidgets.barchart import BarChartWidget
from subwidgets.monthlytable import MonthlyTable

class Statistics(QWidget):
    """
    A widget which shows a statistics using the database

    ...

    Attributes
    ----------
    database : DatabaseHandler
        Current database handler
    
    Methods
    -------
    refresh_stats()
        Redefines the statistics with the current database handler
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
        super(Statistics, self).__init__()

        # Defines database handler
        self.database = database
        
        # Create Best Effort Table
        self.best_effort = BestEffortTable(self.database)

        # Create Monthly Table
        self.monthly_table = MonthlyTable(self.database)

        # Create a Bar Chart
        self.bar_chart  = BarChartWidget(self.database)

        # Horizontal Layout: Best Effort + Monthly
        self.hori_layout = QHBoxLayout()
        self.hori_layout.addWidget(self.best_effort)
        self.hori_layout.addWidget(self.monthly_table)

        month_refresh_btn = QToolButton()
        icon = QIcon()
        icon.addPixmap(QPixmap("images/refresh.png"))
        month_refresh_btn.setIcon(icon)
        month_refresh_btn.clicked.connect(self.recreate_monthly)
        btn_lyt = QHBoxLayout()
        btn_lyt.addWidget(month_refresh_btn)
        btn_lyt.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Main layout 
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.hori_layout)
        self.layout.addLayout(btn_lyt)
        self.layout.addWidget(self.bar_chart )
        self.setLayout(self.layout)
    
    def recreate_monthly(self):
        self.database.recreate_monthly()
        self.refresh_stats()

    def refresh_stats(self):
        """
        Redefines the statistics and recreates the widgets 
        with the current database handler
        """
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
        """
        Shows widget using new_database as the current database handler
        
        Parameters
        ----------
        new_database : DatabaseHandler
            New database handler
        """
        self.database = new_database
        self.refresh_stats()
        self.show()      
