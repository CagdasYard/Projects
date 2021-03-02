from PyQt5 import QtCore, QtGui, QtWidgets
from PIL import Image, ImageDraw, ImageFont, ImageQt
import random
import sys
import time

class Activity:
    
    def __init__(self,ActivityName,SuitableClasses,MoreThanOnce=False,Active=True):
        self.ActivityName    = ActivityName
        self.SuitableClasses = [Item for Item in SuitableClasses if isinstance(Item,int)]
        self.SuitableClasses = [Item for Item in self.SuitableClasses if Item in range(1,9)]
        self.MoreThanOnce    = MoreThanOnce
        self.Active          = Active

    def __getitem__(self,key):
        if key== self.ActivityName:
            return self
        
class SettingsFileIO:

    def __init__(self,FileDirectory):

        self.FileDirectory    = FileDirectory
        self.ActivityList     = {}
        self.ClassList        = []
        self.StaffList        = []
        self.ClassBeforeLunch = 0
        self.LibraryHourCheck = True
        self.NumberofHours    = 4
        self.ErrorMessage     = ""
        self.__defaultTimeSettings={"04":(9,0),"05":(0,40),"06":(0,10),"07":(1,10)}
        self.TimeSettings     = [self.__defaultTimeSettings[Item] for Item in self.__defaultTimeSettings]

    def getSettings(self):
        try:
            with open(self.FileDirectory, 'r',encoding='utf-16') as File:
                for FLine in File:
                    self.SettingsFileInput(FLine)
            self.ClassList.sort()
            self.ClassList = ["%d %c" % (Class[0],Class[1]) for Class in self.ClassList]
        except UnicodeError:
            self.ErrorMessage     = "Uyarı: Seçenekler dosyasını UTF-16 kodlama ile kaydettiğinizden emin olun."
        except FileNotFoundError:
            self.ErrorMessage     = "Uyarı: Programın çalıştığı dizinde Seçenekler dosyası bulunamadı."

    def SettingsFileInput(self,FLine):
        args=FLine.replace("\n","")
        args=args.split(":")
        if len(args) == 4:
            if args[0] == "01":
                Conditions=[False,False]         
                Name          = args[1].replace(" ","")
                Conditions[0] = Name.isalpha()
                List=args[2].split(",")        
                try:
                    Classes=list(map(int,List))
                except:
                    Conditions[1] = False
                else:
                    Conditions[1] = True
                if all(Conditions):
                    self.ActivityList[args[1]] = Activity(args[1],Classes,args[3]=="True")
                else:
                    pass
            else:
                pass
        elif len(args) == 2:
            if args[0] == "02":
                Name = args[1].replace(" ","")
                if Name.isalpha() and args[1] not in self.StaffList:
                    self.StaffList.append(args[1])
                else:
                    pass
            elif args[0] == "03":
                Class = args[1].split(" ")
                Conditions=[False,False,False,False]  
                Conditions[0]= len(Class)== 2
                try:
                    Number = int(Class[0])
                except:
                    Conditions[1]= False
                else:
                    Conditions[1]= Number in range(1,9)
                Conditions[2] = Class[1].isalpha() and Class[1].isupper()
                Conditions[3] = [Number,Class[1]] not in self.ClassList
                if all(Conditions):
                    self.ClassList.append([Number,Class[1]])
                else:
                    return None
            elif args[0] in ["04","06","07"]:
                Hour = args[1].split(".")
                Conditions=[False,False]  
                Conditions[0]= len(Hour)== 2
                try:
                    Hour = list(map(int,Hour))
                except:
                    Conditions[1] = False
                else:
                    Conditions[1] = Hour[0] in range(24) and Hour[1] in range(60)
                if all(Conditions):
                    self.TimeSettings[int(args[0])-4]=(Hour[0],Hour[1])
                else:
                    pass

            elif args[0] == "05":
                Hour = args[1].split(".")
                Conditions=[False,False,False]  
                Conditions[0]= len(Hour)== 2
                try:
                    Hour = list(map(int,Hour))
                except:
                    Conditions[1] = False
                else:
                    Conditions[1] = Hour[0] in range(24) and Hour[1] in range(60)
                    Conditions[2] = Hour[0],Hour[1] != (0,0)
                if all(Conditions):
                    self.TimeSettings[int(args[0])-4]=(Hour[0],Hour[1])
                else:
                    pass

            elif args[0] == "08":
                try:
                    Number = int(args[1])
                except:
                    pass
                else:
                    self.ClassBeforeLunch = Number

            elif args[0] == "09":
                if args[1] == "False":
                    self.LibraryHourCheck = False
            elif args[0] == "10":
                try:
                    Number = int(args[1])
                except:
                    pass
                else:
                    self.NumberofHours = Number
        else:
            pass

    def writeSettings(self):

        with open(self.FileDirectory, 'w',encoding='utf-16') as File:
            for SavedActivity in self.ActivityList:
                LineType        = "01"
                Name            = SavedActivity
                SuitableClasses = ",".join(map(str,self.ActivityList[SavedActivity].SuitableClasses))
                MoreThanOnce    = str(self.ActivityList[SavedActivity].MoreThanOnce)
                File.write(":".join([LineType,Name,SuitableClasses,MoreThanOnce])+"\n")

            for SavedName in self.StaffList:
                LineType        = "02"
                File.write(":".join([LineType,SavedName])+"\n")
    
            for SavedClass in self.ClassList:
                LineType        = "03"
                File.write(":".join([LineType,SavedClass])+"\n")
                
            for SettingType,Setting in enumerate(self.TimeSettings):
                LineType        = "0"+str(SettingType+4)
                SavedSetting    = ".".join(map(str,Setting))
                File.write(":".join([LineType,SavedSetting])+"\n")

            File.write("08:%d\n" % self.ClassBeforeLunch)
            File.write("09:%s\n" % str(self.LibraryHourCheck))
            File.write("10:%d\n" % self.NumberofHours)
            File.close()
