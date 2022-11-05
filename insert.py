import re
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

class Insert(QWidget):

    def __init__(self, database):
        super(Insert, self).__init__()

        WIDGET_WIDTH = 270
        self.database = database

        # Widgets
        text = QLabel("Insert new activity!")
        text.setStyleSheet(''' font-size: 24px; font-weight: bold;''')

        self.name = QLineEdit()
        self.name.setFixedWidth(WIDGET_WIDTH)

        self.date = QCalendarWidget()
        self.date.showToday()
        self.date.setSelectedDate(QDate.currentDate())
        self.date.setFixedWidth(WIDGET_WIDTH)
        self.date.setFixedHeight(170)

        self.distance = QLineEdit()
        self.distance.setValidator(QDoubleValidator().setNotation(QDoubleValidator.Notation.StandardNotation))
        self.distance.setFixedWidth(WIDGET_WIDTH)

        self.time = QLineEdit ()
        rx = QRegularExpression(r"[0-9]?[0-9]:[0-5][0-9]:[0-5][0-9]")
        validator = QRegularExpressionValidator(rx, self)
        self.time.setValidator(validator )
        self.time.setFixedWidth(WIDGET_WIDTH)

        self.pace = QLineEdit()
        rx = QRegularExpression(r"[0-9]:[0-5][0-9]")
        validator = QRegularExpressionValidator(rx, self)
        self.pace.setValidator(validator)
        self.pace.setFixedWidth(WIDGET_WIDTH)

        submit_button = QPushButton("Submit")
        submit_button.setFixedWidth(100)
        submit_button.clicked.connect(self.submit_pressed)

        self.submit_status = QLabel("Acitivity is submitted succesfully!")
        self.submit_status.hide()

        # Layout
        form_lyt = QFormLayout()
        form_lyt.addRow("Name your activity ", self.name)
        form_lyt.addRow("Date ", self.date)
        form_lyt.addRow("Distance (km)", self.distance)
        form_lyt.addRow("Time (hh:mm:ss)", self.time)
        form_lyt.addRow("Pace (m:ss)", self.pace)
        

        layout = QVBoxLayout()
        layout.addWidget(text)
        layout.addLayout(form_lyt)
        layout.addWidget(submit_button)
        layout.addWidget(self.submit_status)
        layout.addStretch()
        self.setLayout(layout)


    def submit_status_change(self, show, is_error, message):
        self.submit_status.setText(message)
        if is_error:
            self.submit_status.setStyleSheet(''' color:red;''')
        else:
            self.submit_status.setStyleSheet(''' color:black;''')
        if show:
            self.submit_status.show()
        else: 
            self.submit_status.hide()

    def is_valid_input(self, name, distance, time, pace):
        if name != "" and distance != "" and pace != "" and time != "":
            return True
        else: 
            self.submit_status_change(True, True, "Input is not valid!")
            return False

    def clear_inputs(self):
        self.name.setText("")
        self.date.showToday()
        self.date.setSelectedDate(QDate.currentDate())
        self.distance.setText("")
        self.pace.setText("")
        self.time.setText("")

    def pace_to_speed(self, pace):
        match = re.search(r"([0-9]):([0-5][0-9])", pace)
        minutes = int(match.group(1))
        seconds = int(match.group(2))
        seconds += minutes*60
        speed = 1/seconds*3600
        return "%.1f" % speed

    def submit_pressed(self): 
        if self.is_valid_input(self.name.text(), self.distance.text(), self.time.text(), self.pace.text()):
            self.submit(self.name.text(), self.date.selectedDate().toString('yyyy-MM-dd'), float(self.distance.text()), 
                self.time.text(), self.pace.text(), self.pace_to_speed(self.pace.text()))
            self.submit_status_change(True, False, "Input is submitted!")
            self.clear_inputs()
    
    def submit(self, name, date, distance, time, pace, speed):
        self.database.insert_activity((name, date, distance, time, pace, speed))
        #print("Submitted")

    def display(self):
        self.submit_status.hide()
        self.show()

        