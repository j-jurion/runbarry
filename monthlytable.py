from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from constants import Constants


class MonthlyTable(QWidget):

    def __init__(self, database):
        super(MonthlyTable, self).__init__()

        months = database.get_months()

        monthly_lyt = QGridLayout()
        
        # Horizontal Headers
        for d in range(len(Constants.MONTH_DATA_TYPES)):
            label = QLabel(Constants.MONTH_DATA_TYPES[d] + Constants.MONTH_DATA_UNITS[d])
            label.setStyleSheet('''font-weight: bold;''')
            monthly_lyt.addWidget(label, 0, d)

        # Add Activities
        row = 1
        for m in months:
            for i in range(1, len(m)):
                l = QLabel(str(m[i]))

                monthly_lyt.addWidget(l, row, i-1)
            row=row+1

        lay2 = QVBoxLayout()
        lay2.addLayout(monthly_lyt)
        lay2.addStretch()
        
        # Main Layout
        table = QWidget()
        table.setLayout(lay2)

        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidget(table)

        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        
        
        # Main Layout
        main_lyt = QVBoxLayout()
        main_lyt.addWidget(scroll)

        lyt = QVBoxLayout()
        group_box = QGroupBox("Monthly")
        group_box.setLayout(main_lyt)
        lyt.addWidget(group_box)
        self.setLayout(lyt)