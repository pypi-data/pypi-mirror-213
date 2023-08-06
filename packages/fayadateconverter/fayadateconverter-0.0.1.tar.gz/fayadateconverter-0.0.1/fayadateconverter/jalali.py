import math
import re
from .datetime import datetime
from .gregorian import gregorian

class jalali():
    
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

        # Check validity of date. TODO better check (leap years)
        if year < 1 or month < 1 or month > 12 or day < 1 or day > 31 or (month > 6 and day == 31):
            raise Exception("Incorrect Date")

        self.persian_year = year
        self.persian_month = month
        self.persian_day = day
        
    def jalali_to_gregorian(self):
        
        # Convert date
        d_4 = (self.persian_year + 1) % 4
        if self.persian_month < 7:
            doy_j = ((self.persian_month - 1) * 31) + self.persian_day
        else:
            doy_j = ((self.persian_month - 7) * 30) + self.persian_day + 186
        d_33 = int(((self.persian_year - 55) % 132) * .0305)
        a = 287 if (d_33 != 3 and d_4 <= d_33) else 286
        if (d_33 == 1 or d_33 == 2) and (d_33 == d_4 or d_4 == 1):
            b = 78
        else:
            b = 80 if (d_33 == 3 and d_4 == 0) else 79
        if int((self.persian_year - 19) / 63) == 20:
            a -= 1
            b += 1
        if doy_j <= a:
            gy = self.persian_year + 621
            gd = doy_j + b
        else:
            gy = self.persian_year + 622
            gd = doy_j - a
        for gm, v in enumerate([0, 31, 29 if (gy % 4 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]):
            if gd <= v:
                break
            gd -= v

        self.gregorian_year = gy
        self.gregorian_month = gm
        self.gregorian_day = gd
        
        self.gregorian_year=str(self.gregorian_year).zfill(4)#format(y,'0000')
        self.gregorian_month= str(self.gregorian_month).zfill(2)#format(m,'00')
        self.gregorian_day= str(self.gregorian_day).zfill(2)#format(d,'00')
        return self.gregorian_year,self.gregorian_month,self.gregorian_day
        
    
    def jalali_to_hijri(self):
        return gregorian(jalali.jalali_to_gregorian(self)).gregorian_to_hijri()
        
       
    def now():
        now = datetime.now()
        return (gregorian(now.year,now.month,now.day).gregorian_to_jalali())
        
    def weekday(self):
        return (gregorian(jalali.jalali_to_gregorian(self)).weekday())
    
    
     ##########################################
    def elapsedtime(self):
        from datetime import datetime, timedelta
        
        current_date_year = int(jalali.now()[0])
        current_date_month = int(jalali.now()[1])
        current_date_day = int(jalali.now()[2])
        
        elapsedtime_day = current_date_day-self.persian_day
        elapsedtime_month = current_date_month-self.persian_month
        elapsedtime_year = current_date_year-self.persian_year
        
        
        if elapsedtime_day <0:
            elapsedtime_month=elapsedtime_month-1
            
            
            if (self.persian_month>1 or self.persian_month<=7):
                numb_day = 31
            elif (self.persian_month>=8 or self.persian_month<=12):
                  numb_day = 30
            elif (self.persian_month==1):
                numb_day = 29
            else:
                numb_day=0
            elapsedtime_day = current_date_day+numb_day
            elapsedtime_day = elapsedtime_day-self.persian_day
            
        
        
        if elapsedtime_month <0:
            elapsedtime_year=elapsedtime_year-1
           
            elapsedtime_month = current_date_month+12
            elapsedtime_month = elapsedtime_month-self.persian_month
            
        
        if elapsedtime_year>=0 and elapsedtime_month>=0 and elapsedtime_day>=0:
            return (elapsedtime_year,elapsedtime_month,elapsedtime_day)
        else:
             raise Exception("Invalid Input")
