import math
import re
from .datetime import datetime
from .UmalqurraArray import UmalqurraArray
class gregorian():
    
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

        self.gregorian_year = year
        self.gregorian_month = month
        self.gregorian_day = day
        
        
    def gregorian_to_hijri(self):

        self.day = int(self.gregorian_day)
        self.m = int(self.gregorian_month) 
        self.y = int(self.gregorian_year)

        # Append January and February to the previous year 
        #(i.e. regard March as the first month of the year
        # in order to simplify leapday corrections)
        if self.m < 3:
            self.y -= 1
            self.m += 12

        # Determine offset between Julian and Gregorian calendar
        a = math.floor(self.y / 100.)
        jgc = a - math.floor(a / 4.) - 2

        # Compute Chronological Julian Day Number (CJDN)
        cjdn = math.floor(365.25 * (self.y + 4716)) + math.floor(30.6001 * (self.m + 1)) + self.day - jgc - 1524

        # Compute Modified Chronological Julian Day Number (MCJDN)
        mcjdn = cjdn - 2400000

        # The MCJDN's of the start of the lunations in the Umm al-Qura calendar are stored in 'ummalqura_arrray.py'
        index = UmalqurraArray.get_index(mcjdn)

        # Compute and output the Umm al-Qura calendar date
        self.iln = index + 16260
        self.ii = math.floor((self.iln - 1) / 12)
        self.iy = self.ii + 1
        self.im = self.iln - 12 * self.ii
        if (self.im<=2)or(self.im==5)or(self.im==7)or(self.im==8)or(self.im==10)or(self.im==12):
            self.id_ = mcjdn - UmalqurraArray.ummalqura_dat[index - 1] 
        else:
            self.id_ = mcjdn - UmalqurraArray.ummalqura_dat[index - 1] +1
        
        self.iy=str(int(self.iy)).zfill(4)#format(self.iy,'0000')
        self.im= str(int(self.im)).zfill(2)#format(self.im,'00')
        self.id_= str(int(self.id_)).zfill(2)#format(self.id_,'00')
        
        return (self.iy, self.im, self.id_)


    
    def gregorian_to_jalali(self):
        # Convert date to Jalali
        d_4 = self.gregorian_year % 4
        g_a = [0, 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
        doy_g = g_a[self.gregorian_month] + self.gregorian_day
        if d_4 == 0 and self.gregorian_month > 2:
            doy_g += 1
        d_33 = int(((self.gregorian_year - 16) % 132) * .0305)
        a = 286 if (d_33 == 3 or d_33 < (d_4 - 1) or d_4 == 0) else 287
        if (d_33 == 1 or d_33 == 2) and (d_33 == d_4 or d_4 == 1):
            b = 78
        else:
            b = 80 if (d_33 == 3 and d_4 == 0) else 79
        if int((self.gregorian_year - 10) / 63) == 30:
            a -= 1
            b += 1
        if doy_g > b:
            jy = self.gregorian_year - 621
            doy_j = doy_g - b
        else:
            jy = self.gregorian_year - 622
            doy_j = doy_g + a
        if doy_j < 187:
            jm = int((doy_j - 1) / 31)
            jd = doy_j - (31 * jm)
            jm += 1
        else:
            jm = int((doy_j - 187) / 30)
            jd = doy_j - 186 - (jm * 30)
            jm += 7
        self.persian_year = jy
        self.persian_month = jm
        self.persian_day = jd
        
        self.py=str(self.persian_year).zfill(4)#format(y,'0000')
        self.pm= str(self.persian_month).zfill(2)#format(m,'00')
        self.pd_= str(self.persian_day).zfill(2)#format(d,'00')
        return self.py,self.pm,self.pd_
    
    def now():
        now = datetime.now()
        
        year=str(now.year).zfill(4)#format(y,'0000')
        month= str(now.month).zfill(2)#format(m,'00')
        day= str(now.day).zfill(2)#format(d,'00')
        
        return (year,month,day)
       
    def weekday(self):
        x = datetime(self.gregorian_year,self.gregorian_month,self.gregorian_day)
        return(x.strftime("%A"))
    ################################################################
    
    def elapsedtime(self):
        from datetime import datetime, timedelta
        current_date_year = datetime.now().year
        current_date_month = datetime.now().month
        current_date_day = datetime.now().day
        
        
        elapsedtime_day = datetime.now().day-self.gregorian_day
        elapsedtime_month =datetime.now().month-self.gregorian_month
        elapsedtime_year = datetime.now().year-self.gregorian_year 
        
        if elapsedtime_day < 0:
            elapsedtime_month=elapsedtime_month-1
            
            if (self.gregorian_month==1 or
                self.gregorian_month==3 or
                self.gregorian_month==5 or
                self.gregorian_month==7 or
                self.gregorian_month==8 or
                self.gregorian_month==10 or
                self.gregorian_month==12):
                numb_day = 31
            elif (self.gregorian_month==4 ):
                numb_day = 30
            elif (self.gregorian_month==6 or 
                  self.gregorian_month==9 or
                  self.gregorian_month==11):
                numb_day = 30
            elif (self.gregorian_month==2):
                numb_day = 28 # or 29
            else:
                numb_day=0
           
            
            elapsedtime_day = datetime.now().day+numb_day
            elapsedtime_day = elapsedtime_day-self.gregorian_day
            
        ###########################################################
        if elapsedtime_month <0:
            elapsedtime_year=elapsedtime_year-1
            
            if (elapsedtime_month >=0 and elapsedtime_month<=5):
                numb_month=12
            else:
                numb_month=11
            elapsedtime_month = datetime.now().month + numb_month
            elapsedtime_month = elapsedtime_month-self.gregorian_month

           
        return (elapsedtime_year,elapsedtime_month,elapsedtime_day)

    
