from datetime import timedelta, datetime

class TimeTemplate():
    """
    A class to format and manipulate time notations (like hh:mm:ss)

    ...

    Attributes
    ----------
    *args : Max. one attribute. 
        time_str : str (if len(args) == 1)
            A string representing time in format hh:mm:ss

    Methods
    -------
    convert_to_datetime(time_str)
        Return a datetime object from a converted string
    add_times(time_str2)
        Add a string time_str2 to the datetime object time_dt
    """
    def __init__(self, *args):
        """
        Parameters
        ----------
        *args : Max. one attribute. 
            time_str : str (if len(args) == 1)
                A string representing time in format hh:mm:ss
        """

        assert len(args) == 1 or len(args) == 0, f"Input arguments of TimeTemplate is not 0 or 1, got {len(args)}"

        if len(args) == 1:
            self.time_str = args[0] ;# In string format
            self.time_dt = self.convert_to_datetime(self.time_str);# In datetime format
        else:
            self.__init__("0:00")

    def __str__(self):
        """ Return the string time_str"""
        return self.time_str

    def convert_to_datetime(self, time_str):
        """
        Return a datetime object from a converted string

        Parameters
        ----------
        time_str : str
            string to be converted to a datetime object
        """
        try:
            t = datetime.strptime(time_str,"%d day, %H:%M:%S") 
        except ValueError:
            try:
                t = datetime.strptime(time_str,"%d days, %H:%M:%S") 
            except ValueError:
                try:
                    t = datetime.strptime(time_str,"%H:%M:%S") 
                except ValueError:
                    t = datetime.strptime(time_str,"%M:%S") 
        return t

    def add_times(self, time_str2):
        """
        Add a string time_str2 to the datetime object time_dt
        
        Parameters
        ----------
        time_str2 : str
            string to be added to datetime object time_dt
        """
        time_delta = timedelta(days = self.time_dt.day-1, hours=self.time_dt.hour, minutes=self.time_dt.minute, seconds=self.time_dt.second)
        time_dt2 = self.convert_to_datetime(time_str2)
        time_delta2 = timedelta(days=time_dt2.day-1, hours=time_dt2.hour, minutes=time_dt2.minute, seconds=time_dt2.second)
        return str(time_delta + time_delta2)



class PaceTemplate(TimeTemplate):
    """
    A class to format and manipulate pace notations (like mm:ss)
    Inherited from TimeTemplate class

    ...

    Attributes
    ----------
    *args : 1 or 2 attributes 
        time_str : str (if len(args) == 2, 1st element)
            A string representing time in format hh:mm:ss
        distance : float (if len(args) == 2, 2nd element)
            A float representing distance in km
        pace_str : str (if len(args) == 1)
            A string representing pace in format mm:ss
    Methods
    -------
    calc_pace(distance)
        Calculate pace from time and distance
    calc_speed()
        Calculate speed from pace
    """
   
    def __init__(self, *args):
        """
        Parameters
        ----------
        *args : 1 or 2 attributes 
            time_str : str (if len(args) == 2, 1st element)
                A string representing time in format hh:mm:ss
            distance : float (if len(args) == 2, 2nd element)
                A float representing distance in km
            pace_str : str (if len(args) == 1)
                A string representing pace in format mm:ss
        """
        # if len(args) == 2: args[0] = time_str and args[1] = distance
        # if len(args) == 1: args[0] = pace_str
        assert len(args) == 2 or len(args) == 1, f"Input arguments of PaceTemplate is not 1 or 2, got {len(args)}"
        if len(args) == 2:
            super(PaceTemplate, self).__init__(args[0])
            self.pace_str = self.calc_pace(args[1])
        elif len(args) == 1:
            super(PaceTemplate, self).__init__()
            self.pace_str = args[0]

        self.pace_dt = self.convert_to_datetime(self.pace_str)
        self.speed = self.calc_speed()

    def __str__(self):
        """ Return the string pace_str"""
        return self.pace_str

    def calc_pace(self, distance):
        """
        Calculate pace from time and distance

        Parameters
        ----------
        distance : float
            A float representing distance in km
        """
        time_in_min = self.time_dt.hour*60 + self.time_dt.minute + self.time_dt.second/60
        pace = time_in_min/distance

        p_min = int(pace)
        p_sec = round((pace - p_min)*60)

        if p_sec == 60:
            p_min = p_min+1
            p_sec = 0
        
        
        if p_sec < 10:
            p_sec = f"0{p_sec}"
        return f"{p_min}:{p_sec}"

    def calc_speed(self):
        """ Calculate speed from pace """
        minutes = self.pace_dt.minute
        seconds = self.pace_dt.second
        seconds += minutes*60
        speed = 1/seconds*3600
        return "%.1f" % speed