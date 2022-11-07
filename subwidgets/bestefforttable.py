from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from helperclasses.constants import Constants

class BestEffortTable(QWidget):

    def __init__(self, database):
        super(BestEffortTable, self).__init__()

        best_lyt = QGridLayout()

        # Column Names
        count = 0
        for d in [2, 3, 4, 5, 1]:
            d_lbl = QLabel(Constants.DATA_TYPES[d] + Constants.DATA_UNITS[d])
            d_lbl.setStyleSheet(''' font : bold;''')
            best_lyt.addWidget(d_lbl, 0, count)
            count = count+1
        


        for d in range(0, 6):
            label = QLabel(Constants.DISTANCES[d])
            label.setStyleSheet(''' font : bold;''')

            try:
                best_activity = database.get_activities(Constants.DISTANCES_DOUBLE[d], "pace", "ASC")[0]
                time = QLabel(best_activity[4])
                pace = QLabel(best_activity[5])
                speed = QLabel(f"{best_activity[6]}")
                date = QLabel(best_activity[2])

                best_lyt.addWidget(label, d+1, 0)
                best_lyt.addWidget(time, d+1, 1)
                best_lyt.addWidget(pace, d+1, 2)
                best_lyt.addWidget(speed, d+1, 3)
                best_lyt.addWidget(date, d+1, 4)

            except IndexError:
                best_lyt.addWidget(label, d+1, 0)
                none_lbl = QLabel("None")
                none_lbl.setStyleSheet(''' font: italic ''')
                best_lyt.addWidget(none_lbl, d+1, 1)

        layout = QVBoxLayout()
        group_box = QGroupBox("Best Efforts")
        group_box.setLayout(best_lyt)
        layout.addWidget(group_box)
        #layout.addStretch()
        self.setLayout(layout)