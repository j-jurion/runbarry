import sqlite3
from sqlite3 import Error
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
from helperclasses.timetemplate import TimeTemplate


class DatabaseHandler():
    """
    A class which manipulates the database. The Database has 2 tables:
      - activity: data of all individual activities
      - monthly: processed data grouped per month
    
    ...

    Attributes
    ----------
    db_file : str
        Filename of database
    
    Methods
    -------
    create_table(sql_create_activity_table)
        Create new table with given instructions
    create_connection()
        Create a database connection to a SQLite database
    close_connection()
        Close connection to database
    insert_activity(activity_list)
        Insert new dataset into acitivity table and updates monthly table
    cmd_to_database(cmd, fetch=False)
        General method to send commands to database
    get_activities(filter, sort_by, order)
        Returns all acitivities filtered by filter and sorted 
        by sort_by with given order
    find_latest_activity()
        Returns latest activity (by date)
    update_monthly(activity_list)
        Updates monthly table with given activity_list
    get_months()
        Return list of all months in database
    fill_monthly(month)
        Fill table with missing months between all months in the database 
        and the given new month
    add_month(month)
        Insert month as empty month if month does not exist yet in database
    get_previous_month(month)
        Return previous month to month (by date)
    get_next_month(self, month):
        Return next month to month (by date)

    """

    def __init__(self, db_file):
        """
        Parameters
        ----------
        db_file : str
            File name of the database
        """

        # Define database file name
        self.db_file = db_file

        # Create activity and monthly tables
        self.create_connection()
        sql_create_activity_table = """ CREATE TABLE IF NOT EXISTS activities (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        date text NOT NULL,
                                        distance double NOT NULL,
                                        time text NOT NULL,
                                        pace text NOT NULL,
                                        speed double NOT NULL
                                    ); """
        sql_create_monthly_table = """ CREATE TABLE IF NOT EXISTS monthly (
                                        id integer PRIMARY KEY,
                                        month text NOT NULL,
                                        tot_distance double NOT NULL,
                                        tot_time text NOT NULL,
                                        nb_activities integer NOT NULL
                                    ); """
        self.create_table(sql_create_activity_table)
        self.create_table(sql_create_monthly_table)
        self.latest_activity = self.find_latest_activity()
        self.close_connection()
    
    def create_table(self, sql_create_activity_table):
        """
        Creates new table with given instructions
        
        Parameters
        ----------
        sql_create_activity_table : str
            Instructions to create new table
        """
        try:
            c = self.conn.cursor()
            c.execute(sql_create_activity_table)
        except Error as e:
            print(e)

    
    def create_connection(self):
        """ Create a database connection to a SQLite database """
        self.conn = None
        try:
            self.conn = sqlite3.connect(self.db_file)
            #print(sqlite3.version)
        except Error as e:
            print(e)
            print("Creating new database")
    
    def close_connection(self):
        """ Close connection to database """
        if self.conn:
            self.conn.close()


    def insert_activity(self, activity_list):
        """
        Insert new dataset into acitivity table and updates monthly table

        Parameters
        ----------
        activity_list : tuple
            A tuple consisting of all activity parameters
        """
        self.create_connection()
        cmd = f''' INSERT INTO activities(name, date, distance, time, pace, speed)
              VALUES{activity_list} '''
        self.cmd_to_database(cmd)

        self.update_monthly(activity_list)
        self.latest_activity = self.find_latest_activity()


    def cmd_to_database(self, cmd, fetch=False):
        """
        General method to send commands to database. 
        This includes opening and closing connection to the database

        Parameters
        ----------
        cmd : str
            Command to be send to SQLite database
        fetch : bool, optional
            If true, fetches data returned from database command
        """
        self.create_connection()
        cursor = self.conn.cursor()
        cursor.execute(cmd)
        if fetch:
            records = cursor.fetchall()
            self.close_connection()
            return records
        self.conn.commit()
        self.close_connection()
        

    def get_activities(self, filter, sort_by, order):
        """
        Returns all acitivities filtered by filter and sorted 
        by sort_by with given order

        Parameters
        ----------
        filter : str
            String to filter distance on
        sort_by : str 
            String to sort by (date, time or pace)
        order : str
            Defines ordering of the sort (ASC: ascending, DESC: descending)
        """
        if filter == "All":
            return self.cmd_to_database(f'''SELECT * FROM activities ORDER BY {sort_by} {order}''', True)
        return self.cmd_to_database(f'''SELECT * FROM activities WHERE distance BETWEEN {filter-0.1} and {filter+1.55} ORDER BY {sort_by} {order} ''', True)
        
    def find_latest_activity(self):
        """
        Returns latest activity (by date)
        """
        try: 
            return self.get_activities("All", "date", "DESC")[0]
        except IndexError: 
            return None

    def remove_activity(self, activity):
        self.cmd_to_database(f'''DELETE FROM activities WHERE id = {activity[0]}''')
        self.refresh_month(activity[2][:7]) ;#YYYY-MM

    ########################################################################
    # Monthly Functions
    ########################################################################
    def update_monthly(self, activity_list):
        """
        Updates monthly table with given activity_list

        Parameters
        ----------
        activity_list : tuple
            A tuple consisting of all activity parameters
        """
        month = activity_list[1][:7] ;#yyyy-mm
        distance = activity_list[2]
        time = TimeTemplate(activity_list[3])

        # Check whether month already exists or not
        data = self.cmd_to_database(f'''SELECT * FROM monthly WHERE month = "{month}"''', True)
        if len(data)==0:
            # Create new month and fill up database
            cmd = f''' INSERT INTO monthly (month, tot_distance, tot_time, nb_activities)
              VALUES("{month}",{distance},"{str(time)}",1) '''
            self.cmd_to_database(cmd)
            self.fill_monthly(month)
            self.clean_monthly()
        else: 
            # Accumulate data to existing month
            data = data[0]
            new_tot_distance = "%.2f" % float(data[2]+distance)
            new_tot_time = time.add_times(data[3])
            new_nb_activity = data[4]+1
            cmd = f''' UPDATE monthly
              SET tot_distance = {new_tot_distance} ,
                  tot_time = "{new_tot_time}" ,
                  nb_activities = {new_nb_activity}
              WHERE month = "{month}"'''
            self.cmd_to_database(cmd)

    def get_months(self):
        """ Return list of all months in database """
        return self.cmd_to_database(f'''SELECT * FROM monthly ORDER BY month DESC ''', True)

    def fill_monthly(self, month):
        """
        Fill table with missing months between all months in the database 
        and the given new month

        Parameter
        ---------
        month : str
            new month to be reached by adding empty months
        """
        data = self.cmd_to_database(f'''SELECT * FROM monthly''', True)
        if len(data)>1:
            last_month = self.cmd_to_database(f'''SELECT month FROM monthly ORDER BY month DESC ''', True)[0][0]
            first_month = self.cmd_to_database(f'''SELECT month FROM monthly ORDER BY month ASC ''', True)[0][0]
            month = self.get_next_month(first_month)
            while month != last_month:
                self.add_month(month)
                month = self.get_next_month(month)
    
    def clean_monthly(self):
        data = self.cmd_to_database(f'''SELECT * FROM monthly''', True)
        if len(data)>0:
            last_month = self.cmd_to_database(f'''SELECT * FROM monthly ORDER BY month DESC ''', True)[0]
            while self.is_empty(last_month):
                self.cmd_to_database(f'''DELETE FROM monthly WHERE month = "{last_month[1]}"''')
                last_month = self.cmd_to_database(f'''SELECT * FROM monthly ORDER BY month DESC ''', True)[0]
            first_month = self.cmd_to_database(f'''SELECT * FROM monthly ORDER BY month ASC ''', True)[0]
            while self.is_empty(first_month):
                self.cmd_to_database(f'''DELETE FROM monthly WHERE month = "{first_month[1]}"''')
                first_month = self.cmd_to_database(f'''SELECT * FROM monthly ORDER BY month ASC ''', True)[0]


    def is_empty(self, month):
        if len(month) > 0:
            if month[4] == 0: 
                return True
            else: 
                return False

    def add_month(self, month):
        """
        Insert month as empty month if month does not exist yet in database

        Parameter
        ---------
        month : str
            new month to be reached by adding empty months
        """
        data = self.cmd_to_database(f'''SELECT * FROM monthly WHERE month = "{month}"''', True)
        if len(data)==0:
            #print(f"Inserting month {month}")
            cmd = f''' INSERT INTO monthly(month, tot_distance, tot_time, nb_activities)
              VALUES("{month}",0,"00:00",0) '''
            self.cmd_to_database(cmd)

    def get_previous_month(self, month):
        """
        Return previous month to month (by date)

        Parameter
        ---------
        month : str
            A month in the format "YYYY-MM"
        """
        month = datetime.strptime(month,"%Y-%m") 
        previous_month = month - relativedelta(months=1)
        return datetime.strftime(previous_month,"%Y-%m") 

    def get_next_month(self, month):
        """
        Return next month to month (by date)

        Parameter
        ---------
        month : str
            A month in the format "YYYY-MM"
        """
        month = datetime.strptime(month,"%Y-%m") 
        next_month = month + relativedelta(months=1)
        return datetime.strftime(next_month,"%Y-%m") 
        
    def refresh_month(self, month):
        self.cmd_to_database(f'''DELETE FROM monthly WHERE month = "{month}"''')
        self.clean_monthly()
        activities =  self.cmd_to_database(f'''SELECT * FROM activities WHERE date LIKE "{month}-%"''', True)
        for a in activities:
            a=a[1:] ;#Remove first element of tuple (which is the id)
            self.update_monthly(a)

    def recreate_monthly(self):
        self.cmd_to_database(f'''DELETE FROM monthly''')
        activities =  self.cmd_to_database(f'''SELECT * FROM activities''', True)
        for a in activities:
            a=a[1:] ;#Remove first element of tuple (which is the id)
            self.update_monthly(a)