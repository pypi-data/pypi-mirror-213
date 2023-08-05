# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 15:32:49 2023

@author: fatemeh
"""

class Date:
    def __init__(self,year,month,day):
        self.year=year
        self.month=month
        self.day=day
class Miladi(Date):
     def __init__(self, year, month, day):
         Date.__init__(self, year, month, day)
     def miladitoshamsi(self,year,month,day):
         
         #year
         if month==1 or month==2 or (month==3 and day<=20):
                  year = year-622
         else:
              year= year-621
         print(year)  
         #month
         #first month--------------------farvardin
         if ((month==3 and day>20)or(month==4 and day<=20)):
             #month=1
             if month==3 and day==21:
                 day=1
                 #month=1
             elif month==3 and day==22:
                  day=2  
             elif month==3 and day==23:
                 day=3
             elif month==3 and day==24:
                 day=4
             elif month==3 and day==25:
                 day=5
             elif month==3 and day==26:
                 day=6
             elif month==3 and day==27:
                 day=7
             elif month==3 and day==28:
                 day=8
             elif month==3 and day==29:
                 day=9
             elif month==3 and day==30:
                 day=10
             elif month==3 and day==31:
                 day=11
             elif month==4 and day==1:
                 day=12
             elif month==4 and day==2:
                 day=13
             elif month==4 and day==3:
                 day=14
             elif month==4 and day==4:
                 day=15
             elif month==4 and day==5:
                 day=16
             elif month==4 and day==6:
                 day=17
             elif month==4 and day==7:
                 day=18
             elif month==4 and day==8:
                 day=19
             elif month==4 and day==9:
                 day=20
             elif month==4 and day==10:
                 day=21
             elif month==4 and day==11:
                 day=22
             elif month==4 and day==12:
                 day=23
             elif month==4 and day==13:
                 day=24
             elif month==4 and day==14:
                 day=25
             elif month==4 and day==15:
                 day=26
             elif month==4 and day==16:
                 day=27
             elif month==4 and day==17:
                 day=28
             elif month==4 and day==18:
                 day=29
             elif month==4 and day==19:
                 day=30
             elif month==4 and day==20:
                 day=31
             month=1
             print(month)
             print(day)  
         #--------------------------------ordibehesht
         if ((month==4 and day>20)or(month==5 and day<=21)):
             #month=1
             if month==4 and day==21:
                 day=1
                 #month=1
             elif month==4 and day==22:
                  day=2  
             elif month==4 and day==23:
                 day=3
             elif month==4 and day==24:
                 day=4
             elif month==4 and day==25:
                 day=5
             elif month==4 and day==26:
                 day=6
             elif month==4 and day==27:
                 day=7
             elif month==4 and day==28:
                 day=8
             elif month==4 and day==29:
                 day=9
             elif month==4 and day==30:
                 day=10
             elif month==5 and day==1:
                 day=11
             elif month==5 and day==2:
                 day=12
             elif month==5 and day==3:
                 day=13
             elif month==5 and day==4:
                 day=14
             elif month==5 and day==5:
                 day=15
             elif month==5 and day==6:
                 day=16
             elif month==5 and day==7:
                 day=17
             elif month==5 and day==8:
                 day=18
             elif month==5 and day==9:
                 day=19
             elif month==5 and day==10:
                 day=20
             elif month==5 and day==11:
                 day=21
             elif month==5 and day==12:
                 day=22
             elif month==5 and day==13:
                 day=23
             elif month==5 and day==14:
                 day=24
             elif month==5 and day==15:
                 day=25
             elif month==5 and day==16:
                 day=26
             elif month==5 and day==17:
                 day=27
             elif month==5 and day==18:
                 day=28
             elif month==5 and day==19:
                 day=29
             elif month==5 and day==20:
                 day=30
             elif month==5 and day==21:
                 day=31
             month=2
             print(month)
             print(day)
         #------------------------------khordad
         if ((month==5 and day>21)or(month==6 and day<=21)):
             #month=1
             if month==5 and day==22:
                 day=1
                 #month=1
             elif month==5 and day==23:
                  day=2  
             elif month==5 and day==24:
                 day=3
             elif month==5 and day==25:
                 day=4
             elif month==5 and day==26:
                 day=5
             elif month==5 and day==27:
                 day=6
             elif month==5 and day==28:
                 day=7
             elif month==5 and day==29:
                 day=8
             elif month==5 and day==30:
                 day=9
             elif month==5 and day==31:
                 day=10
             elif month==6 and day==1:
                 day=11
             elif month==6 and day==2:
                 day=12
             elif month==6 and day==3:
                 day=13
             elif month==6 and day==4:
                 day=14
             elif month==6 and day==5:
                 day=15
             elif month==6 and day==6:
                 day=16
             elif month==6 and day==7:
                 day=17
             elif month==6 and day==8:
                 day=18
             elif month==6 and day==9:
                 day=19
             elif month==6 and day==10:
                 day=20
             elif month==6 and day==11:
                 day=21
             elif month==6 and day==12:
                 day=22
             elif month==6 and day==13:
                 day=23
             elif month==6 and day==14:
                 day=24
             elif month==6 and day==15:
                 day=25
             elif month==6 and day==16:
                 day=26
             elif month==6 and day==17:
                 day=27
             elif month==6 and day==18:
                 day=28
             elif month==6 and day==19:
                 day=29
             elif month==6 and day==20:
                 day=30
             elif month==6 and day==21:
                 day=31
             month=3
             print(month)
             print(day)
         #---------------------------------tir
         if ((month==6 and day>21)or(month==7 and day<=22)):
             #month=1
             if month==6 and day==22:
                 day=1
                 #month=1
             elif month==6 and day==23:
                  day=2  
             elif month==6 and day==24:
                 day=3
             elif month==6 and day==25:
                 day=4
             elif month==6 and day==26:
                 day=5
             elif month==6 and day==27:
                 day=6
             elif month==6 and day==28:
                 day=7
             elif month==6 and day==29:
                 day=8
             elif month==6 and day==30:
                 day=9
             elif month==7 and day==1:
                 day=10
             elif month==7 and day==2:
                 day=11
             elif month==7 and day==3:
                 day=12
             elif month==7 and day==4:
                 day=13
             elif month==7 and day==5:
                 day=14
             elif month==7 and day==6:
                 day=15
             elif month==7 and day==7:
                 day=16
             elif month==7 and day==8:
                 day=17
             elif month==7 and day==9:
                 day=18
             elif month==7 and day==10:
                 day=19
             elif month==7 and day==11:
                 day=20
             elif month==7 and day==12:
                 day=21
             elif month==7 and day==13:
                 day=22
             elif month==7 and day==14:
                 day=23
             elif month==7 and day==15:
                 day=24
             elif month==7 and day==16:
                 day=25
             elif month==7 and day==17:
                 day=26
             elif month==7 and day==18:
                 day=27
             elif month==7 and day==19:
                 day=28
             elif month==7 and day==20:
                 day=29
             elif month==7 and day==21:
                 day=30
             elif month==7 and day==22:
                 day=31
             month=4
             print(month)
             print(day)
         #----------------------------------mordad
         if ((month==7 and day>22)or(month==8 and day<=22)):
             #month=1
             if month==7 and day==23:
                 day=1
                 #month=1
             elif month==7 and day==24:
                  day=2  
             elif month==7 and day==25:
                 day=3
             elif month==7 and day==26:
                 day=4
             elif month==7 and day==27:
                 day=5
             elif month==7 and day==28:
                 day=6
             elif month==7 and day==29:
                 day=7
             elif month==7 and day==30:
                 day=8
             elif month==7 and day==31:
                 day=9
             elif month==8 and day==1:
                 day=10
             elif month==8 and day==2:
                 day=11
             elif month==8 and day==3:
                 day=12
             elif month==8 and day==4:
                 day=13
             elif month==8 and day==5:
                 day=14
             elif month==8 and day==6:
                 day=15
             elif month==8 and day==7:
                 day=16
             elif month==8 and day==8:
                 day=17
             elif month==8 and day==9:
                 day=18
             elif month==8 and day==10:
                 day=19
             elif month==8 and day==11:
                 day=20
             elif month==8 and day==12:
                 day=21
             elif month==8 and day==13:
                 day=22
             elif month==8 and day==14:
                 day=23
             elif month==8 and day==15:
                 day=24
             elif month==8 and day==16:
                 day=25
             elif month==8 and day==17:
                 day=26
             elif month==8 and day==18:
                 day=27
             elif month==8 and day==19:
                 day=28
             elif month==8 and day==20:
                 day=29
             elif month==8 and day==21:
                 day=30
             elif month==8 and day==22:
                 day=31
             month=5
             print(month)
             print(day)   
         #---------------------------------sharivar
         if ((month==8 and day>22)or(month==9 and day<=22)):
             #month=1
             if month==8 and day==23:
                 day=1
                 #month=1
             elif month==8 and day==24:
                  day=2  
             elif month==8 and day==25:
                 day=3
             elif month==8 and day==26:
                 day=4
             elif month==8 and day==27:
                 day=5
             elif month==8 and day==28:
                 day=6
             elif month==8 and day==29:
                 day=7
             elif month==8 and day==30:
                 day=8
             elif month==8 and day==31:
                 day=9
             elif month==9 and day==1:
                 day=10
             elif month==9 and day==2:
                 day=11
             elif month==9 and day==3:
                 day=12
             elif month==9 and day==4:
                 day=13
             elif month==9 and day==5:
                 day=14
             elif month==9 and day==6:
                 day=15
             elif month==9 and day==7:
                 day=16
             elif month==9 and day==8:
                 day=17
             elif month==9 and day==9:
                 day=18
             elif month==9 and day==10:
                 day=19
             elif month==9 and day==11:
                 day=20
             elif month==9 and day==12:
                 day=21
             elif month==9 and day==13:
                 day=22
             elif month==9 and day==14:
                 day=23
             elif month==9 and day==15:
                 day=24
             elif month==9 and day==16:
                 day=25
             elif month==9 and day==17:
                 day=26
             elif month==9 and day==18:
                 day=27
             elif month==9 and day==19:
                 day=28
             elif month==9 and day==20:
                 day=29
             elif month==9 and day==21:
                 day=30
             elif month==9 and day==22:
                 day=31
             month=6
             print(month)
             print(day)   
         #---------------------------mehr
         if ((month==9 and day>22)or(month==10 and day<=22)):
             #month=1
             if month==9 and day==23:
                 day=1
                 #month=1
             elif month==9 and day==24:
                  day=2  
             elif month==9 and day==25:
                 day=3
             elif month==9 and day==26:
                 day=4
             elif month==9 and day==27:
                 day=5
             elif month==9 and day==28:
                 day=6
             elif month==9 and day==29:
                 day=7
             elif month==9 and day==30:
                 day=8
             elif month==10 and day==1:
                 day=9
             elif month==10 and day==2:
                 day=10
             elif month==10 and day==3:
                 day=11
             elif month==10 and day==4:
                 day=12
             elif month==10 and day==5:
                 day=13
             elif month==10 and day==6:
                 day=14
             elif month==10 and day==7:
                 day=15
             elif month==10 and day==8:
                 day=16
             elif month==10 and day==9:
                 day=17
             elif month==10 and day==10:
                 day=18
             elif month==10 and day==11:
                 day=19
             elif month==10 and day==12:
                 day=20
             elif month==10 and day==13:
                 day=21
             elif month==10 and day==14:
                 day=22
             elif month==10 and day==15:
                 day=23
             elif month==10 and day==16:
                 day=24
             elif month==10 and day==17:
                 day=25
             elif month==10 and day==18:
                 day=26
             elif month==10 and day==19:
                 day=27
             elif month==10 and day==20:
                 day=28
             elif month==10 and day==21:
                 day=29
             elif month==10 and day==22:
                 day=30
             #elif month==10 and day==23:
             #    day=31
             month=7
             print(month)
             print(day)
         #--------------------------------aban
         if ((month==10 and day>22)or(month==11 and day<=21)):
             #month=1
             if month==10 and day==23:
                 day=1
                 #month=1
             elif month==10 and day==24:
                  day=2  
             elif month==10 and day==25:
                 day=3
             elif month==10 and day==26:
                 day=4
             elif month==10 and day==27:
                 day=5
             elif month==10 and day==28:
                 day=6
             elif month==10 and day==29:
                 day=7
             elif month==10 and day==30:
                 day=8
             elif month==10 and day==31:
                 day=9
             elif month==11 and day==1:
                 day=10
             elif month==11 and day==2:
                 day=11
             elif month==11 and day==3:
                 day=12
             elif month==11 and day==4:
                 day=13
             elif month==11 and day==5:
                 day=14
             elif month==11 and day==6:
                 day=15
             elif month==11 and day==7:
                 day=16
             elif month==11 and day==8:
                 day=17
             elif month==11 and day==9:
                 day=18
             elif month==11 and day==10:
                 day=19
             elif month==11 and day==11:
                 day=20
             elif month==11 and day==12:
                 day=21
             elif month==11 and day==13:
                 day=22
             elif month==11 and day==14:
                 day=23
             elif month==11 and day==15:
                 day=24
             elif month==11 and day==16:
                 day=25
             elif month==11 and day==17:
                 day=26
             elif month==11 and day==18:
                 day=27
             elif month==11 and day==19:
                 day=28
             elif month==11 and day==20:
                 day=29
             elif month==11 and day==21:
                 day=30
             #elif month==10 and day==23:
             #    day=31
             month=8
             print(month)
             print(day)
         #--------------------------------azar
         if ((month==11 and day>21)or(month==12 and day<=21)):
             #month=1
             if month==11 and day==22:
                 day=1
                 #month=1
             elif month==11 and day==23:
                  day=2  
             elif month==11 and day==24:
                 day=3
             elif month==11 and day==25:
                 day=4
             elif month==11 and day==26:
                 day=5
             elif month==11 and day==27:
                 day=6
             elif month==11 and day==28:
                 day=7
             elif month==11 and day==29:
                 day=8
             elif month==11 and day==30:
                 day=9
             elif month==12 and day==1:
                 day=10
             elif month==12 and day==2:
                 day=11
             elif month==12 and day==3:
                 day=12
             elif month==12 and day==4:
                 day=13
             elif month==12 and day==5:
                 day=14
             elif month==12 and day==6:
                 day=15
             elif month==12 and day==7:
                 day=16
             elif month==12 and day==8:
                 day=17
             elif month==12 and day==9:
                 day=18
             elif month==12 and day==10:
                 day=19
             elif month==12 and day==11:
                 day=20
             elif month==12 and day==12:
                 day=21
             elif month==12 and day==13:
                 day=22
             elif month==12 and day==14:
                 day=23
             elif month==12 and day==15:
                 day=24
             elif month==12 and day==16:
                 day=25
             elif month==12 and day==17:
                 day=26
             elif month==12 and day==18:
                 day=27
             elif month==12 and day==19:
                 day=28
             elif month==12 and day==20:
                 day=29
             elif month==12 and day==21:
                 day=30
             #elif month==10 and day==23:
             #    day=31
             month=9
             print(month)
             print(day)
         #----------------------------dey
         if ((month==12 and day>21)or(month==1 and day<=20)):
             #month=1
             if month==12 and day==22:
                 day=1
                 #month=1
             elif month==12 and day==23:
                  day=2  
             elif month==12 and day==24:
                 day=3
             elif month==12 and day==25:
                 day=4
             elif month==12 and day==26:
                 day=5
             elif month==12 and day==27:
                 day=6
             elif month==12 and day==28:
                 day=7
             elif month==12 and day==29:
                 day=8
             elif month==12 and day==30:
                 day=9
             elif month==12 and day==31:
                 day=10
             elif month==1 and day==1:
                 day=11
             elif month==1 and day==2:
                 day=12
             elif month==1 and day==3:
                 day=13
             elif month==1 and day==4:
                 day=14
             elif month==1 and day==5:
                 day=15
             elif month==1 and day==6:
                 day=16
             elif month==1 and day==7:
                 day=17
             elif month==1 and day==8:
                 day=18
             elif month==1 and day==9:
                 day=19
             elif month==1 and day==10:
                 day=20
             elif month==1 and day==11:
                 day=21
             elif month==1 and day==12:
                 day=22
             elif month==1 and day==13:
                 day=23
             elif month==1 and day==14:
                 day=24
             elif month==1 and day==15:
                 day=25
             elif month==1 and day==16:
                 day=26
             elif month==1 and day==17:
                 day=27
             elif month==1 and day==18:
                 day=28
             elif month==1 and day==19:
                 day=29
             elif month==1 and day==20:
                 day=30
             #elif month==10 and day==23:
             #    day=31
             month=10
             print(month)
             print(day)
         #--------------------------------bahman
         if ((month==1 and day>20)or(month==2 and day<=19)):
             #month=1
             if month==1 and day==21:
                 day=1
                 #month=1
             elif month==1 and day==22:
                  day=2  
             elif month==1 and day==23:
                 day=3
             elif month==1 and day==24:
                 day=4
             elif month==1 and day==25:
                 day=5
             elif month==1 and day==26:
                 day=6
             elif month==1 and day==27:
                 day=7
             elif month==1 and day==28:
                 day=8
             elif month==1 and day==29:
                 day=9
             elif month==1 and day==30:
                 day=10
             elif month==1 and day==31:
                 day=11
             elif month==2 and day==1:
                 day=12
             elif month==2 and day==2:
                 day=13
             elif month==2 and day==3:
                 day=14
             elif month==2 and day==4:
                 day=15
             elif month==2 and day==5:
                 day=16
             elif month==2 and day==6:
                 day=17
             elif month==2 and day==7:
                 day=18
             elif month==2 and day==8:
                 day=19
             elif month==2 and day==9:
                 day=20
             elif month==2 and day==10:
                 day=21
             elif month==2 and day==11:
                 day=22
             elif month==2 and day==12:
                 day=23
             elif month==2 and day==13:
                 day=24
             elif month==2 and day==14:
                 day=25
             elif month==2 and day==15:
                 day=26
             elif month==2 and day==16:
                 day=27
             elif month==2 and day==17:
                 day=28
             elif month==2 and day==18:
                 day=29
             elif month==2 and day==19:
                 day=30
             #elif month==10 and day==23:
             #    day=31
             month=11
             print(month)
             print(day)
         #---------------------------sfand29
         if ((month==2 and day>19)or(month==3 and day<=20)):
             #month=1
             if month==2 and day==20:
                 day=1
                 #month=1
             elif month==2 and day==21:
                  day=2  
             elif month==2 and day==22:
                 day=3
             elif month==2 and day==23:
                 day=4
             elif month==2 and day==24:
                 day=5
             elif month==2 and day==25:
                 day=6
             elif month==2 and day==26:
                 day=7
             elif month==2 and day==27:
                 day=8
             elif month==2 and day==28:
                 day=9
             elif month==3 and day==1:
                 day=10
             elif month==3 and day==2:
                 day=11
             elif month==3 and day==3:
                 day=12
             elif month==3 and day==4:
                 day=13
             elif month==3 and day==5:
                 day=14
             elif month==3 and day==6:
                 day=15
             elif month==3 and day==7:
                 day=16
             elif month==3 and day==8:
                 day=17
             elif month==3 and day==9:
                 day=18
             elif month==3 and day==10:
                 day=19
             elif month==3 and day==11:
                 day=20
             elif month==3 and day==12:
                 day=21
             elif month==3 and day==13:
                 day=22
             elif month==3 and day==14:
                 day=23
             elif month==3 and day==15:
                 day=24
             elif month==3 and day==16:
                 day=25
             elif month==3 and day==17:
                 day=26
             elif month==3 and day==18:
                 day=27
             elif month==3 and day==19:
                 day=28
             elif month==3 and day==20:
                 day=29
             #elif month==2 and day==19:
             #   day=30
             #elif month==10 and day==23:
             #    day=31
             month=12
             print(month)
             print(day)