import math
import re
from .datetime import datetime
from .gregorian import gregorian
from .UmalqurraArray import UmalqurraArray


class hijri():
    
    def __init__(self,*date):
        # Parse date
        if len(date) == 1:
            date = date[0]
            if type(date) is str:
                m = re.match(r'^(\d{4})\D(\d{1,2})\D(\d{1,2})$', date)
                if m:
                    [year, month, day] = [int(m.group(1)), int(m.group(2)), int(m.group(3))]
                else:
                    raise Exception("Invalid Input String")
            elif type(date) is datetime.date:
                [year, month, day] = [date.year, date.month, date.day]
            elif type(date) is tuple:
                year, month, day = date
                year = int(year)
                month = int(month)
                day = int(day)
            else:
                raise Exception("Invalid Input Type")
        elif len(date) == 3:
            year = int(date[0])
            month = int(date[1])
            day = int(date[2])
        else:
            raise Exception("Invalid Input")

        # Check the validity of input date
        try:
            datetime(year, month, day)
        except:
            raise Exception("Invalid Date")

        self.hijri_year = year
        self.hijri_month = month
        self.hijri_day = day
        
    def hijri_to_gregorian(self):
        self.year = int(self.hijri_year)
        self.month = int(self.hijri_month)
        self.day = int(self.hijri_day)
        
        self.iy = self.year
        self.im = self.month
        self.id_ = self.day
        self.ii = self.iy - 1
        self.iln = (self.ii * 12) + 1 + (self.im - 1)
        i = self.iln - 16260
        mcjdn = self.id_ + UmalqurraArray.ummalqura_dat[i - 1] - 1
        cjdn = mcjdn + 2400000
        
        def julian_to_gregorian(julian_date):
            """
            Convert Julian date to Gregorian date.
            Source from: http://keith-wood.name/calendars.html
            :param julian_date:
            :return:
            """

            z = math.floor(julian_date + 0.5)
            a = math.floor((z - 1867216.25) / 36524.25)
            a = z + 1 + a - math.floor(a / 4)
            b = a + 1524
            c = math.floor((b - 122.1) / 365.25)
            d = math.floor(365.25 * c)
            e = math.floor((b - d) / 30.6001)
            if self.year>=1444 and ((self.month>=2 and self.month<=5) or(self.month==8 )or (self.month==10)or(self.month==12)):
                
                if self.month==8:
                    self.day = b - d - math.floor(e * 30.6001)
                    if self.day<4 and self.day>28:
                        self.day+=2
                self.day = b - d - math.floor(e * 30.6001)+1
                        
            else:
                self.day = b - d - math.floor(e * 30.6001)

            if e > 13.5:
                self.month = e - 13
            else:
                self.month = e - 1
            if self.month > 2.5:
                self.year = c - 4716
            else:
                self.year = c - 4715
            if self.year <= 0:
                self.year -= 1
                
            self.year=str(int(self.year)).zfill(4)#format(y,'0000')
            self.month= str(int(self.month)).zfill(2)#format(m,'00')
            self.day= str(int(self.day)).zfill(2)#format(d,'00')
            return self.year, self.month, self.day
        return julian_to_gregorian(cjdn)

    

    def hijri_to_jalali(self):
        if self.hijri_month % 2!=0:
            self.hijri_day = self.hijri_day -1
            
        return gregorian(hijri.hijri_to_gregorian(self)).gregorian_to_jalali()
        
    def now():
        now = datetime.now()
        return (gregorian(now.year,now.month,now.day).gregorian_to_hijri())
        
    def weekday(self):
        
        return (gregorian(hijri.hijri_to_gregorian(self)).weekday())
    
    def elapsedtime(self):
        current_date_year = int(hijri.now()[0])
        current_date_month = int(hijri.now()[1])
        current_date_day = int(hijri.now()[2])
        
        elapsedtime_day = current_date_day-self.hijri_day
        elapsedtime_month = current_date_month-self.hijri_month
        elapsedtime_year = current_date_year-self.hijri_year
        
        if elapsedtime_day <0:
            elapsedtime_month=elapsedtime_month-1
            
            if (self.hijri_month==1 or
                self.hijri_month==5 or
                self.hijri_month==7 or
                self.hijri_month==9 or
                self.hijri_month==11): 
                numb_day = 30
            elif (self.hijri_month==3):
                numb_day = 29
            elif (self.hijri_month==2 or
                self.hijri_month==4 or
                self.hijri_month==6 or
                self.hijri_month==8 or
                self.hijri_month==10 or
                self.hijri_month==12):
                 numb_day = 30 # or 29
            else:
                numb_day=0
            elapsedtime_day = current_date_day+numb_day
            elapsedtime_day = elapsedtime_day-self.hijri_day
            
        if elapsedtime_month <0:
            elapsedtime_year=elapsedtime_year-1
            
            elapsedtime_month = current_date_month+12
            elapsedtime_month = elapsedtime_month-self.hijri_month
        
        if elapsedtime_year>=0 and elapsedtime_month>=0 and elapsedtime_day>=0:
            return (elapsedtime_year,elapsedtime_month,elapsedtime_day)
        else:
             raise Exception("Invalid Input")
