from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from helperclasses.constants import Constants


class ActivityLayout(QWidget):
    def __init__(self, activity, overview, latest_activity_id):
        super(ActivityLayout, self).__init__()

        icon = QIcon()
        icon.addPixmap(QPixmap(Constants.REMOVE_FILENAME))

        name = QLabel(str(activity[1]))
        date = QLabel(str(activity[2]))
        distance = QLabel(str(activity[3]))
        time = QLabel(str(activity[4]))
        pace = QLabel(str(activity[5]))
        speed = QLabel(str(activity[6]))
        remove_btn = QToolButton()
        remove_btn.setIcon(icon)
        remove_btn.clicked.connect(lambda:overview.remove_activity(activity))

        if activity[0] == latest_activity_id:
            background_color = "yellow"
            name.setStyleSheet(f"background-color : {background_color}")
            date.setStyleSheet("background-color : yellow")
            distance.setStyleSheet("background-color : yellow")
            time.setStyleSheet("background-color : yellow")
            pace.setStyleSheet("background-color : yellow")
            speed.setStyleSheet("background-color : yellow")

        self.get = [name, date, distance, time, pace, speed, remove_btn] 


class ActivityTable(QWidget):

    def __init__(self, activities, latest_activity, overview):
        super(ActivityTable, self).__init__()

        # Table Layout
        table_lyt = QGridLayout()
        table_lyt.setHorizontalSpacing(0)

        # Horizontal Headers
        for d in range(len(Constants.DATA_TYPES)):
            label = QLabel(Constants.DATA_TYPES[d] + Constants.DATA_UNITS[d])
            label.setStyleSheet('''font-weight: bold;''')
            table_lyt.addWidget(label, 0, d)

        
        # Add Activities
        row = 1
        
        for a in activities:
            activity = ActivityLayout(a, overview, latest_activity[0])

            for i in range(7):
                table_lyt.addWidget(activity.get[i], row, i)

            row=row+1

        lay2 = QVBoxLayout()
        lay2.addLayout(table_lyt)
        lay2.addStretch()
        
        # Main Layout
        table = QWidget()
        table.setLayout(lay2)


        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidget(table)
        #scroll.setFixedHeight(500)

        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        
        
        # Main Layout
        main_lyt = QVBoxLayout()
        main_lyt.addWidget(scroll)
        self.setLayout(main_lyt)
