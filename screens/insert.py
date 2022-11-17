from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from helperclasses.constants import Constants
from helperclasses.timetemplate import TimeTemplate, PaceTemplate


class Insert(QWidget):
    """
    A widget which shows the insert form to add an activity

    ...

    Attributes
    ----------
    database : DatabaseHandler
        Current database handler

    Methods
    -------
    submit_status_change(show, is_error, message)
        Shows, hides and stylizes the submit status message, depending on is_error
    is_valid_input(name, distance, time)
        Checks whether the name, distance and time inputs are valid
    clear_inputs()
        Clears all inputs
    submit_pressed()
        Action of the submit button. Prepares data to be submitted. 
    submit(name, date, distance, time, pace, speed)
        Adds name, date, distance, time, pace and speed to database
    display()
        Shows this widget and removes submit status message

    """

    def __init__(self, database):
        """
        Parameters
        ----------
        database : DatabaseHandler
            Current database handler
        """
        super(Insert, self).__init__()

        # Sets widget size and database
        WIDGET_WIDTH = 270
        self.database = database

        # Form widgets with validators and layout initializations
        text = QLabel("Insert new activity")
        text.setStyleSheet(''' font-size: 24px; font-weight: bold;''')

        self.name = QLineEdit()
        self.name.setFixedWidth(WIDGET_WIDTH)

        self.date = QCalendarWidget()
        self.date.showToday()
        self.date.setSelectedDate(QDate.currentDate())
        self.date.setFixedWidth(WIDGET_WIDTH)
        self.date.setFixedHeight(170)

        self.distance = QLineEdit()
        doubleValidator = QDoubleValidator()
        doubleValidator.setBottom(0)
        doubleValidator.setDecimals(2)
        doubleValidator.setLocale(QLocale("en"))
        doubleValidator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.distance.setValidator(doubleValidator)
        self.distance.setFixedWidth(WIDGET_WIDTH)

        self.time = QLineEdit ()
        rx = QRegularExpression(r"[0-9]:[0-5][0-9]:[0-5][0-9]")
        validator = QRegularExpressionValidator(rx, self)
        self.time.setValidator(validator)
        self.time.setFixedWidth(WIDGET_WIDTH)

        submit_button = QPushButton("Submit")
        submit_button.setFixedWidth(100)
        submit_button.clicked.connect(self.submit_pressed)

        self.submit_status = QLabel("Acitivity is submitted succesfully!")
        self.submit_status.hide()

        # Define form layout
        form_lyt = QFormLayout()
        form_lyt.addRow("Name your activity ", self.name)
        form_lyt.addRow(Constants.DATA_TYPES[1], self.date)
        form_lyt.addRow(Constants.DATA_TYPES[2] + "(km)", self.distance)
        form_lyt.addRow(Constants.DATA_TYPES[3] + "(h:mm:ss)", self.time)
        
        # Define overlapping main layout
        layout = QVBoxLayout()
        layout.addWidget(text)
        layout.addLayout(form_lyt)
        layout.addWidget(submit_button)
        layout.addWidget(self.submit_status)
        layout.addStretch()
        self.setLayout(layout)


    def submit_status_change(self, show, is_error, message):
        """
        Shows, hides and stylizes the submit status message, depending on is_error

        Parameters
        ----------
        show : bool
            If True then show, else hide submit status
        is_error : bool
            If True then set message in red color, else black
        message : str
            Message to be shown as submit status
        """
        self.submit_status.setText(message)
        if is_error:
            self.submit_status.setStyleSheet(''' color:red;''')
        else:
            self.submit_status.setStyleSheet(''' color:black;''')
        if show:
            self.submit_status.show()
        else: 
            self.submit_status.hide()

    def is_valid_input(self, name, distance, time):
        """
        Returns True if name, distance and time are valid.
        Otherwise returns False and shows submit status message. 

        Parameters
        ----------
        name : str
            Name of new activity
        distance : float
            Distance of new activity
        time : str
            Time of new activity
        """
        if name != "" and distance != "" and time != "" and len(time)>=7:
            return True
        else: 
            self.submit_status_change(True, True, "Input is not valid!")
            return False

    def clear_inputs(self):
        """ Clears all input fields and sets calender widget to today """
        self.name.setText("")
        self.date.showToday()
        self.date.setSelectedDate(QDate.currentDate())
        self.distance.setText("")
        self.time.setText("")


    def submit_pressed(self): 
        """
        Action of the submit button. If inputs are valid all inputs in 
        correct format are send to submit(). Additionally clear_inputs() is called.
        """
        if self.is_valid_input(self.name.text(), self.distance.text(), self.time.text()):

            time_submit = TimeTemplate(self.time.text())
            self.pace = PaceTemplate(time_submit.__str__(), float(self.distance.text()))

            self.submit(self.name.text(), self.date.selectedDate().toString('yyyy-MM-dd'), float(self.distance.text()), 
                time_submit.__str__(), self.pace.__str__(), self.pace.speed)
            
            self.clear_inputs()
    
    def submit(self, name, date, distance, time, pace, speed):
        """
        Adds name, date, distance, time, pace and speed to database. 
        Additionally shows submit message.

        Parameters
        ----------
        name : str
            Name of new activity
        distance : float
            Distance of new activity
        time : str
            Time of new activity
        pace : str
            Pace of new activity
        speed : float
            Speed of new activity
        """
        self.database.insert_activity((name, date, distance, time, pace, speed))
        self.submit_status_change(True, False, "Input is submitted!")
        #print("Submitted")

    def display(self):
        """ Shows this widget and removes submit status message """
        self.submit_status.hide()
        self.show()
        