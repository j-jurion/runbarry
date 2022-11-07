from datetime import timedelta, datetime

class TimeTemplate():
    
    # if len(args) == 1 : args[0] = time_str
    def __init__(self, *args):

        assert len(args) == 1 or len(args) == 0, f"Input arguments of TimeTemplate is not 0 or 1, got {len(args)}"

        if len(args) == 1:
            self.time_str = args[0] ;# In string format
            self.time_dt = self.convert_to_datetime(self.time_str);# In datetime format
        else:
            self.__init__("0:00")

    def __str__(self):
        return self.time_str

    def convert_to_datetime(self, time_str):
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
        time_delta = timedelta(days = self.time_dt.day, hours=self.time_dt.hour, minutes=self.time_dt.minute, seconds=self.time_dt.second)
        time_dt2 = self.convert_to_datetime(time_str2)
        time_delta2 = timedelta(days=time_dt2.day, hours=time_dt2.hour, minutes=time_dt2.minute, seconds=time_dt2.second)
        return str(time_delta + time_delta2)



class PaceTemplate(TimeTemplate):

    # if len(args) == 2: args[0] = time_str and args[1] = distance
    # if len(args) == 1: args[0] = pace_str
    def __init__(self, *args):

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
        return self.pace_str

    def calc_pace(self, distance):
        time_in_min = self.time_dt.hour*60 + self.time_dt.minute + self.time_dt.second/60
        pace = time_in_min/distance

        p_min = int(pace)
        p_sec = round((pace - p_min)*60)
        
        if p_sec < 10:
            p_sec = f"0{p_sec}"
        return f"{p_min}:{p_sec}"

    def calc_speed(self):
        minutes = self.pace_dt.minute
        seconds = self.pace_dt.second
        seconds += minutes*60
        speed = 1/seconds*3600
        return "%.1f" % speed