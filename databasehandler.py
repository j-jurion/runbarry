import sqlite3
from sqlite3 import Error
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
from timetemplate import TimeTemplate


class DatabaseHandler():

    def __init__(self, db_file):
        self.db_file = db_file

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
        try:
            c = self.conn.cursor()
            c.execute(sql_create_activity_table)
        except Error as e:
            print(e)

    
    def create_connection(self):
        """ create a database connection to a SQLite database """
        self.conn = None
        try:
            self.conn = sqlite3.connect(self.db_file)
            #print(sqlite3.version)
        except Error as e:
            print(e)
            print("Creating new database")
    
    def close_connection(self):
        if self.conn:
            self.conn.close()


    def insert_activity(self, activity_list):
        self.create_connection()
        cmd = f''' INSERT INTO activities(name,date, distance, time, pace, speed)
              VALUES{activity_list} '''
        self.cmd_to_database(cmd)

        self.update_monthly(activity_list)
        self.latest_activity = self.find_latest_activity()


    def cmd_to_database(self, cmd, fetch=False):
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
        if filter == "All":
            return self.cmd_to_database(f'''SELECT * FROM activities ORDER BY {sort_by} {order}''', True)
        return self.cmd_to_database(f'''SELECT * FROM activities WHERE distance BETWEEN {filter-1} and {filter+1} ORDER BY {sort_by} {order} ''', True)
        
    def find_latest_activity(self):
        try: 
            return self.get_activities("All", "date", "DESC")[0]
        except IndexError: 
            return None

    ########################################################################
    # Monthly Functions
    ########################################################################
    def update_monthly(self, activity_list):
        month = activity_list[1][:7] ;#yyyy-mm
        distance = activity_list[2]
        time = TimeTemplate(activity_list[3])

        data = self.cmd_to_database(f'''SELECT * FROM monthly WHERE month = "{month}"''', True)
        if len(data)==0:
            cmd = f''' INSERT INTO monthly (month, tot_distance, tot_time, nb_activities)
              VALUES("{month}",{distance},"{str(time)}",1) '''
            self.cmd_to_database(cmd)
            self.fill_monthly(month)
        else: 
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
        return self.cmd_to_database(f'''SELECT * FROM monthly ORDER BY month DESC ''', True)

    def fill_monthly(self, month):
        data = self.cmd_to_database(f'''SELECT * FROM monthly''', True)
        if len(data)>1:
            last_month = self.cmd_to_database(f'''SELECT month FROM monthly ORDER BY month DESC ''', True)[0][0]
            first_month = self.cmd_to_database(f'''SELECT month FROM monthly ORDER BY month ASC ''', True)[0][0]
            month = self.get_next_month(first_month)
            while month != last_month:
                print(f"month in loop {month}")

                self.add_month(month)
                month = self.get_next_month(month)

        
    def add_month(self, month):
        data = self.cmd_to_database(f'''SELECT * FROM monthly WHERE month = "{month}"''', True)
        if len(data)==0:
            print(f"Inserting month {month}")
            cmd = f''' INSERT INTO monthly(month, tot_distance, tot_time, nb_activities)
              VALUES("{month}",0,"00:00",0) '''
            self.cmd_to_database(cmd)

    def get_previous_month(self, month):
        month = datetime.strptime(month,"%Y-%m") 
        previous_month = month - relativedelta(months=1)
        return datetime.strftime(previous_month,"%Y-%m") 

    def get_next_month(self, month):
        month = datetime.strptime(month,"%Y-%m") 
        next_month = month + relativedelta(months=1)
        return datetime.strftime(next_month,"%Y-%m") 
        