import sqlite3
from sqlite3 import Error
from datetime import timedelta, datetime

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
        cmd = ''' INSERT INTO activities(name,date, distance, time, pace, speed)
              VALUES(?,?,?,?,?,?) '''

        cursor = self.conn.cursor()
        cursor.execute(cmd, activity_list)
        self.update_monthly(cursor, activity_list)
        self.conn.commit()
        self.latest_activity = self.find_latest_activity()
        self.close_connection()

        return cursor.lastrowid

    def get_from_database(self, cmd):
        self.create_connection()
        
        cursor = self.conn.cursor()
        cursor.execute(cmd)
        records = cursor.fetchall()
        
        self.close_connection()

        return records

    def get_activities(self, filter, sort_by, order):
        if filter == "All":
            return self.get_from_database(f'''SELECT * FROM activities ORDER BY {sort_by} {order}''')
        return self.get_from_database(f'''SELECT * FROM activities WHERE distance BETWEEN {filter-1} and {filter+1} ORDER BY {sort_by} {order} ''')
        
    def find_latest_activity(self):
        try: 
            return self.get_activities("All", "date", "DESC")[0]
        except IndexError: 
            return None

    ########################################################################
    # Monthly Functions
    ########################################################################
    def update_monthly(self, cursor, activity_list):
        month = activity_list[1][:7] ;#yyyy-mm
        distance = activity_list[2]
        try:
            t = datetime.strptime(activity_list[3],"%H:%M:%S") 
        except ValueError:
            t = datetime.strptime(activity_list[3],"%M:%S") 

        time = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)

        cursor.execute("SELECT * FROM monthly WHERE month = ?", (month,))
        data=cursor.fetchall()
        if len(data)==0:
            cmd = ''' INSERT INTO monthly(month, tot_distance, tot_time, nb_activities)
              VALUES(?,?,?,?) '''
            cursor.execute(cmd, (month, distance, str(time), 1))
        else: 
            data = data[0]
            new_tot_distance = data[2]+distance
            try:
                t_data = datetime.strptime(data[3],"%H:%M:%S") 
            except ValueError:
                t_data = datetime.strptime(data[3],"%M:%S") 
            time_data = timedelta(hours=t_data.hour, minutes=t_data.minute, seconds=t_data.second)
            new_tot_time = str(time_data+time)
            new_nb_activity = data[4]+1
            cmd = ''' UPDATE monthly
              SET tot_distance = ? ,
                  tot_time = ? ,
                  nb_activities = ?
              WHERE month = ?'''
            cursor.execute(cmd, (new_tot_distance, new_tot_time, new_nb_activity, month))

    def get_months(self):
        return self.get_from_database(f'''SELECT * FROM monthly ORDER BY month DESC ''')
        