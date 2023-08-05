# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 14:51:02 2023

@author: fatemeh
"""

class Date:
    def __init__(self,year,month,day):
        self.year=year
        self.month=month
        self.day=day
class Shamsi(Date):
     def __init__(self, year, month, day):
         Date.__init__(self, year, month, day)
     def shamsitomiladi(self,year,month,day):

           #year
           if month==11 or month==12 or (month==10 and day>=11):
                year = year+622
           else:
                year= year+621
           print(year)    
           #month
           #first month----------------------jaunary
           if ((month==10 and day>10)or(month==11 and day<=11)):
               #month=1
               if month==10 and day==11:
                   day=1
                   #month=1
               elif month==10 and day==12:
                    day=2  
               elif month==10 and day==13:
                   day=3
               elif month==10 and day==14:
                   day=4
               elif month==10 and day==15:
                   day=5
               elif month==10 and day==16:
                   day=6
               elif month==10 and day==17:
                   day=7
               elif month==10 and day==18:
                   day=8
               elif month==10 and day==19:
                   day=9
               elif month==10 and day==20:
                   day=10
               elif month==10 and day==21:
                   day=11
               elif month==10 and day==22:
                   day=12
               elif month==10 and day==23:
                   day=13
               elif month==10 and day==24:
                   day=14
               elif month==10 and day==25:
                   day=15
               elif month==10 and day==26:
                   day=16
               elif month==10 and day==27:
                   day=17
               elif month==10 and day==28:
                   day=18
               elif month==10 and day==29:
                   day=19
               elif month==10 and day==30:
                   day=20
               elif month==11 and day==1:
                   day=21
               elif month==11 and day==2:
                   day=22
               elif month==11 and day==3:
                   day=23
               elif month==11 and day==4:
                   day=24
               elif month==11 and day==5:
                   day=25
               elif month==11 and day==6:
                   day=26
               elif month==11 and day==7:
                   day=27
               elif month==11 and day==8:
                   day=28
               elif month==11 and day==9:
                   day=29
               elif month==11 and day==10:
                   day=30
               elif month==11 and day==11:
                   day=31
               month=1
               print(month)
               print(day)
           #-------------------------------------------february
           elif ((month==11 and day>11)or(month==12 and day<=9)):
                #month=2
                if month==11 and day==12:
                    day=1
                    #month=1
                elif month==11 and day==13:
                     day=2  
                elif month==11 and day==14:
                    day=3
                elif month==11 and day==15:
                    day=4
                elif month==11 and day==16:
                    day=5
                elif month==11 and day==17:
                    day=6
                elif month==11 and day==18:
                    day=7
                elif month==11 and day==19:
                    day=8
                elif month==11 and day==20:
                    day=9
                elif month==11 and day==21:
                    day=10
                elif month==11 and day==22:
                    day=11
                elif month==11 and day==23:
                    day=12
                elif month==11 and day==24:
                    day=13
                elif month==11 and day==25:
                    day=14
                elif month==11 and day==26:
                    day=15
                elif month==11 and day==27:
                    day=16
                elif month==11 and day==28:
                    day=17
                elif month==11 and day==29:
                    day=18
                elif month==11 and day==30:
                    day=19
                elif month==12 and day==1:
                    day=20
                elif month==12 and day==2:
                    day=21
                elif month==12 and day==3:
                    day=22
                elif month==12 and day==4:
                    day=23
                elif month==12 and day==5:
                    day=24
                elif month==12 and day==6:
                    day=25
                elif month==12 and day==7:
                    day=26
                elif month==12 and day==8:
                    day=27
                elif month==12 and day==9:
                    day=28
                    
                #elif month==12 and day==10:
                #    day=29
                #elif month==12 and day==11:
                #    day=30
                #elif month==11 and day==11:
                #   day=31
                
                month=2
                print(month)
                print(day)
           #-------------------------------------------march29
           elif ((month==12 and day>9)or(month==1 and day<=11)):
                #month=3
                 if month==12 and day==10:
                     day=1
                     #month=1
                 elif month==12 and day==11:
                      day=2  
                 elif month==12 and day==12:
                     day=3
                 elif month==12 and day==13:
                     day=4
                 elif month==12 and day==14:
                     day=5
                 elif month==12 and day==15:
                     day=6
                 elif month==12 and day==16:
                     day=7
                 elif month==12 and day==17:
                     day=8
                 elif month==12 and day==18:
                     day=9
                 elif month==12 and day==19:
                     day=10
                 elif month==12 and day==20:
                     day=11
                 elif month==12 and day==21:
                     day=12
                 elif month==12 and day==22:
                     day=13
                 elif month==12 and day==23:
                     day=14
                 elif month==12 and day==24:
                     day=15
                 elif month==12 and day==25:
                     day=16
                 elif month==12 and day==26:
                     day=17
                 elif month==12 and day==27:
                     day=18
                 elif month==12 and day==28:
                     day=19
                 elif month==12 and day==29:
                     day=20
                 elif month==1 and day==1:
                     day=21
                 elif month==1 and day==2:
                     day=22
                 elif month==1 and day==3:
                     day=23
                 elif month==1 and day==4:
                     day=24
                 elif month==1 and day==5:
                     day=25
                 elif month==1 and day==6:
                     day=26
                 elif month==1 and day==7:
                     day=27
                 elif month==1 and day==8:
                     day=28
                 elif month==1 and day==9:
                     day=29
                 elif month==1 and day==10:
                     day=30
                 elif month==1 and day==11:
                     day=31
                 month=3
                 print(month)
                 print(day)
           #-------------------------------------------april
           elif ((month==1 and day>11)or(month==2 and day<=10)):
                #month=4 
                if month==1 and day==12:
                    day=1
                    #month=1
                elif month==1 and day==13:
                     day=2  
                elif month==1 and day==14:
                    day=3
                elif month==1 and day==15:
                    day=4
                elif month==1 and day==16:
                    day=5
                elif month==1 and day==17:
                    day=6
                elif month==1 and day==18:
                    day=7
                elif month==1 and day==19:
                    day=8
                elif month==1 and day==20:
                    day=9
                elif month==1 and day==21:
                    day=10
                elif month==1 and day==22:
                    day=11
                elif month==1 and day==23:
                    day=12
                elif month==1 and day==24:
                    day=13
                elif month==1 and day==25:
                    day=14
                elif month==1 and day==26:
                    day=15
                elif month==1 and day==27:
                    day=16
                elif month==1 and day==28:
                    day=17
                elif month==1 and day==29:
                    day=18
                elif month==1 and day==30:
                    day=19
                elif month==1 and day==31:
                    day=20
                elif month==2 and day==1:
                    day=21
                elif month==2 and day==2:
                    day=22
                elif month==2 and day==3:
                    day=23
                elif month==2 and day==4:
                    day=24
                elif month==2 and day==5:
                    day=25
                elif month==2 and day==6:
                    day=26
                elif month==2 and day==7:
                    day=27
                elif month==2 and day==8:
                    day=28
                elif month==2 and day==9:
                    day=29
                elif month==2 and day==10:
                    day=30
                #elif month==2 and day==11:
                #   day=31
                month=4
                print(month)
                print(day)
           #-------------------------------------------may
           elif ((month==2 and day>10)or(month==3 and day<=10)):
                #month=5   
                if month==2 and day==11:
                    day=1
                    #month=1
                elif month==2 and day==12:
                     day=2  
                elif month==2 and day==13:
                    day=3
                elif month==2 and day==14:
                    day=4
                elif month==2 and day==15:
                    day=5
                elif month==2 and day==16:
                    day=6
                elif month==2 and day==17:
                    day=7
                elif month==2 and day==18:
                    day=8
                elif month==2 and day==19:
                    day=9
                elif month==2 and day==20:
                    day=10
                elif month==2 and day==21:
                    day=11
                elif month==2 and day==22:
                    day=12
                elif month==2 and day==23:
                    day=13
                elif month==2 and day==24:
                    day=14
                elif month==2 and day==25:
                    day=15
                elif month==2 and day==26:
                    day=16
                elif month==2 and day==27:
                    day=17
                elif month==2 and day==28:
                    day=18
                elif month==2 and day==29:
                    day=19
                elif month==2 and day==30:
                    day=20
                elif month==2 and day==31:
                    day=21
                elif month==3 and day==1:
                    day=22
                elif month==3 and day==2:
                    day=23
                elif month==3 and day==3:
                    day=24
                elif month==3 and day==4:
                    day=25
                elif month==3 and day==5:
                    day=26
                elif month==3 and day==6:
                    day=27
                elif month==3 and day==7:
                    day=28
                elif month==3 and day==8:
                    day=29
                elif month==3 and day==9:
                    day=30
                elif month==3 and day==10:
                   day=31
                month=5
                print(month)
                print(day)
           #-------------------------------------------june
           elif ((month==3 and day>10)or(month==4 and day<=9)):
               # month=6 
                if month==3 and day==11:
                    day=1
                    #month=1
                elif month==3 and day==12:
                     day=2  
                elif month==3 and day==13:
                    day=3
                elif month==3 and day==14:
                    day=4
                elif month==3 and day==15:
                    day=5
                elif month==3 and day==16:
                    day=6
                elif month==3 and day==17:
                    day=7
                elif month==3 and day==18:
                    day=8
                elif month==3 and day==19:
                    day=9
                elif month==3 and day==20:
                    day=10
                elif month==3 and day==21:
                    day=11
                elif month==3 and day==22:
                    day=12
                elif month==3 and day==23:
                    day=13
                elif month==3 and day==24:
                    day=14
                elif month==3 and day==25:
                    day=15
                elif month==3 and day==26:
                    day=16
                elif month==3 and day==27:
                    day=17
                elif month==3 and day==28:
                    day=18
                elif month==3 and day==29:
                    day=19
                elif month==3 and day==30:
                    day=20
                elif month==3 and day==31:
                    day=21
                elif month==4 and day==1:
                    day=22
                elif month==4 and day==2:
                    day=23
                elif month==4 and day==3:
                    day=24
                elif month==4 and day==4:
                    day=25
                elif month==4 and day==5:
                    day=26
                elif month==4 and day==6:
                    day=27
                elif month==4 and day==7:
                    day=28
                elif month==4 and day==8:
                    day=29
                elif month==4 and day==9:
                    day=30
                #elif month==4 and day==10:
                #   day=31
                month=6
                print(month)
                print(day)
           #-------------------------------------------july
           elif ((month==4 and day>9)or(month==5 and day<=9)):
                #month=7 
                if month==4 and day==10:
                    day=1
                    #month=1
                elif month==4 and day==11:
                     day=2  
                elif month==4 and day==12:
                    day=3
                elif month==4 and day==13:
                    day=4
                elif month==4 and day==14:
                    day=5
                elif month==4 and day==15:
                    day=6
                elif month==4 and day==16:
                    day=7
                elif month==4 and day==17:
                    day=8
                elif month==4 and day==18:
                    day=9
                elif month==4 and day==19:
                    day=10
                elif month==4 and day==20:
                    day=11
                elif month==4 and day==21:
                    day=12
                elif month==4 and day==22:
                    day=13
                elif month==4 and day==23:
                    day=14
                elif month==4 and day==24:
                    day=15
                elif month==4 and day==25:
                    day=16
                elif month==4 and day==26:
                    day=17
                elif month==4 and day==27:
                    day=18
                elif month==4 and day==28:
                    day=19
                elif month==4 and day==29:
                    day=20
                elif month==4 and day==30:
                    day=21
                elif month==4 and day==31:
                    day=22
                elif month==5 and day==1:
                    day=23
                elif month==5 and day==2:
                    day=24
                elif month==5 and day==3:
                    day=25
                elif month==5 and day==4:
                    day=26
                elif month==5 and day==5:
                    day=27
                elif month==5 and day==6:
                    day=28
                elif month==5 and day==7:
                    day=29
                elif month==5 and day==8:
                    day=30
                elif month==5 and day==9:
                   day=31
                month=7
                print(month)
                print(day)
           #-------------------------------------------August
           elif ((month==5 and day>9)or(month==6 and day<=9)):
                #month=8  
                if month==5 and day==10:
                    day=1
                    #month=1
                elif month==5 and day==11:
                     day=2  
                elif month==5 and day==12:
                    day=3
                elif month==5 and day==13:
                    day=4
                elif month==5 and day==14:
                    day=5
                elif month==5 and day==15:
                    day=6
                elif month==5 and day==16:
                    day=7
                elif month==5 and day==17:
                    day=8
                elif month==5 and day==18:
                    day=9
                elif month==5 and day==19:
                    day=10
                elif month==5 and day==20:
                    day=11
                elif month==5 and day==21:
                    day=12
                elif month==5 and day==22:
                    day=13
                elif month==5 and day==23:
                    day=14
                elif month==5 and day==24:
                    day=15
                elif month==5 and day==25:
                    day=16
                elif month==5 and day==26:
                    day=17
                elif month==5 and day==27:
                    day=18
                elif month==5 and day==28:
                    day=19
                elif month==5 and day==29:
                    day=20
                elif month==5 and day==30:
                    day=21
                elif month==5 and day==31:
                    day=22
                elif month==6 and day==1:
                    day=23
                elif month==6 and day==2:
                    day=24
                elif month==6 and day==3:
                    day=25
                elif month==6 and day==4:
                    day=26
                elif month==6 and day==5:
                    day=27
                elif month==6 and day==6:
                    day=28
                elif month==6 and day==7:
                    day=29
                elif month==6 and day==8:
                    day=30
                elif month==6 and day==9:
                   day=31
                month=8
                print(month)
                print(day)
           #-------------------------------------------september
           elif ((month==6 and day>9)or(month==7 and day<=8)):
                #month=9
                if month==6 and day==10:
                    day=1
                    #month=1
                elif month==6 and day==11:
                     day=2  
                elif month==6 and day==12:
                    day=3
                elif month==6 and day==13:
                    day=4
                elif month==6 and day==14:
                    day=5
                elif month==6 and day==15:
                    day=6
                elif month==6 and day==16:
                    day=7
                elif month==6 and day==17:
                    day=8
                elif month==6and day==18:
                    day=9
                elif month==6 and day==19:
                    day=10
                elif month==6 and day==20:
                    day=11
                elif month==6 and day==21:
                    day=12
                elif month==6 and day==22:
                    day=13
                elif month==6 and day==23:
                    day=14
                elif month==6 and day==24:
                    day=15
                elif month==6 and day==25:
                    day=16
                elif month==6 and day==26:
                    day=17
                elif month==6 and day==27:
                    day=18
                elif month==6 and day==28:
                    day=19
                elif month==6 and day==29:
                    day=20
                elif month==6 and day==30:
                    day=21
                elif month==6 and day==31:
                    day=22
                elif month==7 and day==1:
                    day=23
                elif month==7 and day==2:
                    day=24
                elif month==7 and day==3:
                    day=25
                elif month==7 and day==4:
                    day=26
                elif month==7 and day==5:
                    day=27
                elif month==7 and day==6:
                    day=28
                elif month==7 and day==7:
                    day=29
                elif month==7 and day==8:
                    day=30
                #elif month==6 and day==9:
                #  day=31
                month=9
                print(month)
                print(day)
           #-------------------------------------------october
           elif ((month==7 and day>8)or(month==8 and day<=9)):
                #month=10  
                if month==7 and day==9:
                    day=1
                    #month=1
                elif month==7 and day==10:
                     day=2  
                elif month==7 and day==11:
                    day=3
                elif month==7 and day==12:
                    day=4
                elif month==7 and day==13:
                    day=5
                elif month==7 and day==14:
                    day=6
                elif month==7 and day==15:
                    day=7
                elif month==7 and day==16:
                    day=8
                elif month==7 and day==17:
                    day=9
                elif month==7 and day==18:
                    day=10
                elif month==7 and day==19:
                    day=11
                elif month==7 and day==20:
                    day=12
                elif month==7 and day==21:
                    day=13
                elif month==7 and day==22:
                    day=14
                elif month==7 and day==23:
                    day=15
                elif month==7 and day==24:
                    day=16
                elif month==7 and day==25:
                    day=17
                elif month==7 and day==26:
                    day=18
                elif month==7 and day==27:
                    day=19
                elif month==7 and day==28:
                    day=20
                elif month==7 and day==29:
                    day=21
                elif month==7 and day==30:
                    day=22
                elif month==8 and day==1:
                    day=23
                elif month==8 and day==2:
                    day=24
                elif month==8 and day==3:
                    day=25
                elif month==8 and day==4:
                    day=26
                elif month==8 and day==5:
                    day=27
                elif month==8 and day==6:
                    day=28
                elif month==8 and day==7:
                    day=29
                elif month==8 and day==8:
                    day=30
                #elif month==6 and day==9:
                #  day=31
                month=10
                print(month)
                print(day)
           #------------------------------------------november
           elif ((month==8 and day>9)or(month==9 and day<=9)):
                #month=11 
                if month==8 and day==9:
                    day=1
                    #month=1
                elif month==8 and day==10:
                     day=2  
                elif month==8 and day==11:
                    day=3
                elif month==8 and day==12:
                    day=4
                elif month==8 and day==13:
                    day=5
                elif month==8 and day==14:
                    day=6
                elif month==8 and day==15:
                    day=7
                elif month==8 and day==16:
                    day=8
                elif month==8 and day==17:
                    day=9
                elif month==8 and day==18:
                    day=10
                elif month==8 and day==19:
                    day=11
                elif month==8 and day==20:
                    day=12
                elif month==8 and day==21:
                    day=13
                elif month==8 and day==22:
                    day=14
                elif month==8 and day==23:
                    day=15
                elif month==8 and day==24:
                    day=16
                elif month==8 and day==25:
                    day=17
                elif month==8 and day==26:
                    day=18
                elif month==8 and day==27:
                    day=19
                elif month==8 and day==28:
                    day=20
                elif month==8 and day==29:
                    day=21
                elif month==8 and day==30:
                    day=22
                elif month==9 and day==1:
                    day=23
                elif month==9 and day==2:
                    day=24
                elif month==9 and day==3:
                    day=25
                elif month==9 and day==4:
                    day=26
                elif month==9 and day==5:
                    day=27
                elif month==9 and day==6:
                    day=28
                elif month==9 and day==7:
                    day=29
                elif month==9 and day==8:
                    day=30
                elif month==9 and day==9:
                  day=31
                month=11
                print(month)
                print(day)
           #------------------------------------------desember
           elif ((month==9 and day>9)or(month==10 and day<=10)):
                #month=2       
                if month==9 and day==10:
                     day=1
                     #month=1
                elif month==9 and day==11:
                    day=2
                elif month==9 and day==12:
                    day=3
                elif month==9 and day==13:
                    day=4
                elif month==9 and day==14:
                    day=5
                elif month==9 and day==15:
                    day=6
                elif month==9 and day==16:
                    day=7
                elif month==9 and day==17:
                    day=8
                elif month==9 and day==18:
                    day=9
                elif month==9 and day==19:
                    day=10
                elif month==9 and day==20:
                    day=11
                elif month==9 and day==21:
                    day=12
                elif month==9 and day==22:
                    day=13
                elif month==9 and day==23:
                    day=14
                elif month==9 and day==24:
                    day=15
                elif month==9 and day==25:
                    day=16
                elif month==9 and day==26:
                    day=17
                elif month==9 and day==27:
                    day=18
                elif month==9 and day==28:
                    day=19
                elif month==9 and day==29:
                    day=20
                elif month==9 and day==30:
                    day=21
                elif month==10 and day==1:
                    day=22
                elif month==10 and day==2:
                    day=23
                elif month==10 and day==3:
                    day=24
                elif month==10 and day==4:
                    day=25
                elif month==10 and day==5:
                    day=26
                elif month==10 and day==6:
                    day=27
                elif month==10 and day==7:
                    day=28
                elif month==10 and day==8:
                    day=29
                elif month==10 and day==9:
                    day=30
                elif month==10 and day==10:
                    day=31
                month=12
                print(month)   

     