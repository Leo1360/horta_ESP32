import time

class DateTime:
    def __init__(self,timeTuple) -> None:
        #(year, month, mday, hour, minute, second, weekday, yearday)
        self.year   = timeTuple[0]
        self.month  = timeTuple[1]
        self.day    = timeTuple[2]
        self.hour   = timeTuple[3]
        self.minute = timeTuple[4]
        self.second = timeTuple[5]
        self.weekday = timeTuple[6]
        pass

    def __str__(self) -> str:
        return str(self.day) + "/" + str(self.month) + "/" + str(self.year) + " " + str(self.hour) + ":" + str(self.minute) + ":" + str(self.second)

    def getTouple(self):
        return(self.year,self.month,self.day,self.hour,self.minute,self.second,self.weekday,"0")

    @staticmethod
    def now():
        return DateTime(time.localtime())