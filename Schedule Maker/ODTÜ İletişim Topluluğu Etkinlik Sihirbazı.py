from PyQt5 import QtCore, QtGui, QtWidgets
from PIL import Image, ImageDraw, ImageFont, ImageQt
import random
import sys
import time
from Worker import *
from Settings import *
from SettingsIO import *
            
class AppWindow(QtWidgets.QMainWindow):
    resized = QtCore.pyqtSignal()
    def __init__(self):
        
############################ DEĞİŞKENLER ############################
        ## Kaydedilmiş ayarları okuyan obje
        self.SettingsIO = SettingsFileIO("Seçenekler.txt")
        self.SettingsIO.getSettings()
        
        ## Etkinlikleri tutan sözlük
        self.Work={}
        ## Aynı ders saati içerisinde birden fazla kere yapılabilen
        ## etkinliklerin indexleri
        self.MoreThanOnce=[]
        ## Her sınıf için sözlükteki hangi etkinliğin uygun
        ## olduğunu tutan liste
        self.ActivitiesForClasses=[]
        ## Ders saatlerinin olduğu liste
        self.ClassHours = []
        ## Her ders saati için her sınıfta kaç kişi olacağını 
        ## tutan liste
        self.MegaSchedule=[]
        ## Her ders saatinde için sınıflarda yapılacak etkinlikleri
        ## tutan liste
        self.ClassActivityList=[]
        ## Her ders saatinde hangi sınıfa kimlerin gireceğini tutan
        ## liste
        self.FinalizedSchedule=[]
########################## BAŞLANGIÇ ##########################
        super(QtWidgets.QMainWindow, self).__init__()
        
        self.Error = False
        self.setupUi()

    def setupUi(self):

############################# ARAYÜZ ############################

                    ####### ÇERÇEVE #######
        if not self.objectName():
            self.setObjectName("self")
            self.setWindowTitle("ODTÜ İletişim Topluluğu Paylaşım Etkinlikleri Atama Sihirbazı")
        self.setWindowIcon(QtGui.QIcon('logo.png'))

        
                    ####### PENCERE #######
        self.resize(1800,820)
        
        self.Width  = self.frameGeometry().width()
        self.Height = self.frameGeometry().height()

        self.Scene  = QtWidgets.QGraphicsScene()
        self.View   = QtWidgets.QGraphicsView(self.Scene,self)
        self.View.setStyleSheet("background:transparent;")        

        self.Pixmap = QtGui.QPixmap("logo2.png")
        self.PixmapItem=QtWidgets.QGraphicsPixmapItem(self.Pixmap)
        self.Scene.addItem(self.PixmapItem)
        
        self.resized.connect(self.ResizeScene)

                    ######### FONT #########
        Font = QtGui.QFont()
        Font.setFamily("Arial")
        
        Font1 = QtGui.QFont()
        Font1.setFamily("Arial")
        Font1.setPointSize(24)
        Font1.setUnderline(True)

        Font2 = QtGui.QFont()
        Font2.setFamily("Arial")
        Font2.setPointSize(18)
        
                    ######  KİŞİLER  ######
        ## Liste 1
        self.ListWidget1 = QtWidgets.QListWidget(self)
        self.ListWidget1.setObjectName("List1")
        self.ListWidget1.setGeometry(QtCore.QRect(30, 420,
                                                  240, 180))
        self.ListWidget1.setSelectionMode(2)
        self.ListWidget1.setFont(Font)
        self.LoadNameList()
        
        ## Etiket 1
        self.Label1 = QtWidgets.QLabel(self)
        self.Label1.setObjectName(u"Kişiler:")
        self.Label1.setFont(Font1)
        self.Label1Update()

        ## Metin Kutusu 1
        self.TextBox1 = QtWidgets.QLineEdit(self)
        self.TextBox1.setObjectName("TextBox1")
        self.TextBox1.setGeometry(QtCore.QRect(30, 610,
                                               240, 30))

        self.TextBox1.setFont(Font)
        self.TextBox1.setText("")
        self.TextBox1.editingFinished.connect(self.AddItemtoNameList)

        ## Ekle Butonu 1
        self.AddButton1 = QtWidgets.QPushButton(self)
        self.AddButton1.setObjectName("AddButton1")
        self.AddButton1.setGeometry(QtCore.QRect(30, 650,
                                                 80, 30))
        
        self.AddButton1.setFont(Font)
        self.AddButton1.setText("Ekle")
        self.AddButton1.clicked.connect(self.AddItemtoNameList)
        
        ## Çıkar Butonu 1
        self.RemoveButton1 = QtWidgets.QPushButton(self)
        self.RemoveButton1.setObjectName("RemoveButton1")
        self.RemoveButton1.setGeometry(QtCore.QRect(110, 650,
                                                    80, 30))
        self.RemoveButton1.setFont(Font)
        self.RemoveButton1.setText("Çıkar")
        self.RemoveButton1.clicked.connect(self.RemoveItemfromNameList)

        ## Temizle Butonu 1
        self.ClearButton1 = QtWidgets.QPushButton(self)
        self.ClearButton1.setObjectName("Clear Button1")
        self.ClearButton1.setGeometry(QtCore.QRect(190, 650,
                                                    80, 30))
        self.ClearButton1.setFont(Font)
        self.ClearButton1.setText("Temizle")
        self.ClearButton1.clicked.connect(self.ClearNameList)

                    ######  SINIFLAR  ######        
        ## Liste 2
        self.ListWidget2 = QtWidgets.QListWidget(self)
        self.ListWidget2.setObjectName("List2")
        self.ListWidget2.setGeometry(QtCore.QRect(30, 110,
                                                  240, 150))
        self.ListWidget2.setSelectionMode(2)
        self.ListWidget2.setFont(Font)
        self.LoadClassList()
        
        ## Etiket 2
        self.Label2 = QtWidgets.QLabel(self)
        self.Label2.setObjectName(u"Sınıflar:")
        self.Label2.setFont(Font1)
        self.Label2Update()  

        ## Metin Kutusu 2
        self.TextBox2 = QtWidgets.QLineEdit(self)
        self.TextBox2.setObjectName("TextBox2")
        self.TextBox2.setGeometry(QtCore.QRect(30, 270,
                                               240, 30))
        self.TextBox2.setFont(Font)
        self.TextBox2.setText("")
        self.TextBox2.editingFinished.connect(self.AddItemtoClassList)

        ## Ekle Butonu 2
        self.AddButton2 = QtWidgets.QPushButton(self)
        self.AddButton2.setObjectName("AddButton2")
        self.AddButton2.setGeometry(QtCore.QRect(30, 310,
                                                 80, 30))
        self.AddButton2.setFont(Font)
        self.AddButton2.setText("Ekle")
        self.AddButton2.clicked.connect(self.AddItemtoClassList)

        ## Çıkar Butonu 2
        self.RemoveButton2 = QtWidgets.QPushButton(self)
        self.RemoveButton2.setObjectName("RemoveButton2")
        self.RemoveButton2.setGeometry(QtCore.QRect(110, 310,
                                                    80, 30))
        self.RemoveButton2.setFont(Font)
        self.RemoveButton2.setText("Çıkar")
        self.RemoveButton2.clicked.connect(self.RemoveItemfromClassList)

        ## Temizle Butonu 2
        self.ClearButton2 = QtWidgets.QPushButton(self)
        self.ClearButton2.setObjectName("Clear Button2")
        self.ClearButton2.setGeometry(QtCore.QRect(190, 310,
                                                    80, 30))
        self.ClearButton2.setFont(Font)
        self.ClearButton2.setText("Temizle")       
        self.ClearButton2.clicked.connect(self.ClearClassList)

                    ######  DERS SAATI  ######
        ## Etiket 3
        self.Label3 = QtWidgets.QLabel(self)
        self.Label3.setObjectName(u"Ders Saati:")
        self.Label3.setFont(Font2)
        self.Label3.setText("Ders saati:")
        
        self.Width3 = self.Label3.fontMetrics().boundingRect(self.Label3.text()).width() 
        self.Height3 = self.Label3.fontMetrics().boundingRect(self.Label3.text()).height()

        ## Döndürme Butonu 1        
        self.spinBox1 = QtWidgets.QSpinBox(self)
        self.spinBox1.setObjectName(u"spinBox")

        self.spinBox1.setFont(Font)
        self.spinBox1.setValue(self.SettingsIO.NumberofHours)
        self.spinBox1.valueChanged.connect(self.setClassHour)

        QtCore.QMetaObject.connectSlotsByName(self)
        
                  ######  DURUM ÇUBUĞU  ######

        Font3 = QtGui.QFont()
        Font3.setFamily("Arial")
        Font3.setItalic(True)

        self.Message=QtWidgets.QLabel(self)
        if self.SettingsIO.ErrorMessage:
            self.Message.setText(self.SettingsIO.ErrorMessage)
        else:
            self.Message.setText(" Sihirbazı çalıştırmak için 'Çalıştır' butonuna basınız.")
        self.Message.setFont(Font3) 
        self.statusBar().addWidget(self.Message)
        self.statusBar().setFont(Font3)
        
                  ######  MENU ÇUBUĞU  ######
        
        self.MenuBar    = QtWidgets.QMenuBar(self)
        self.MenuBar.setGeometry(QtCore.QRect(0,0,self.Width,20))
        self.setMenuBar(self.MenuBar)        
        
        self.showAction = QtWidgets.QAction('&Göster',self)
        self.showAction.setShortcut('F4')
        self.showAction.setStatusTip("Ders programını gösterin.")
        self.showAction.triggered.connect(self.Popup)
        self.showAction.setEnabled(False)
        
        self.execAction = QtWidgets.QAction(self)
        self.execAction.setShortcut('F5')
        self.execAction.setText("&Çalıştır [{}]".format(QtGui.QKeySequence.toString(self.execAction.shortcut()) ))
        self.execAction.setStatusTip("Sihirbazı başlatın.")
        self.execAction.triggered.connect(self.AppExecute)

        self.saveAction = QtWidgets.QAction(self)
        self.saveAction.setShortcut('Ctrl+S')
        self.saveAction.setText("&Kaydet")
        self.saveAction.setStatusTip("Ders programını kaydedin.")
        self.saveAction.triggered.connect(self.SaveImageFile)
        self.saveAction.setEnabled(False)

        self.settingsAction = QtWidgets.QAction(self)
        self.settingsAction.setText("&Seçenekler")
        self.settingsAction.setStatusTip("Etkinlikleri ve ders programını düzenleyin.")
        self.settingsAction.triggered.connect(self.ShowSettingsWindow)
        
        self.creditsAction = QtWidgets.QAction('&Hakkında',self)
        self.creditsAction.triggered.connect(self.credits_method)

        
        self.FileBar   = QtWidgets.QMenu('&Dosya',self.MenuBar)
        
        self.MenuBar.addAction(self.FileBar.menuAction())
        self.FileBar.addAction(self.showAction)
        self.FileBar.addAction(self.saveAction)
        self.MenuBar.addAction(self.execAction)
        self.MenuBar.addAction(self.settingsAction)
        self.MenuBar.addAction(self.creditsAction)

    def appLock(self):
        self.AddButton1.setEnabled(False)
        self.ClearButton1.setEnabled(False)
        self.RemoveButton1.setEnabled(False)
        self.TextBox1.setReadOnly(True)

        self.AddButton2.setEnabled(False)
        self.ClearButton2.setEnabled(False)
        self.RemoveButton2.setEnabled(False)
        self.TextBox2.setReadOnly(True)

        self.spinBox1.setReadOnly(True)
        
        self.showAction.setEnabled(False)
        self.execAction.setEnabled(False)
        self.saveAction.setEnabled(False)
        self.settingsAction.setEnabled(False)
        
    def appUnlock(self):
        self.AddButton1.setEnabled(True)
        self.ClearButton1.setEnabled(True)
        self.RemoveButton1.setEnabled(True)
        self.TextBox1.setReadOnly(False)

        self.AddButton2.setEnabled(True)
        self.ClearButton2.setEnabled(True)
        self.RemoveButton2.setEnabled(True)
        self.TextBox2.setReadOnly(False)

        self.spinBox1.setReadOnly(False)
        
        self.showAction.setEnabled(True)
        self.execAction.setEnabled(True)
        self.saveAction.setEnabled(True)
        self.settingsAction.setEnabled(True)
        
    def ShowSettingsWindow(self):

        self.SettingsWindow = SettingsWindow(SettingsIO=self.SettingsIO)
        self.SettingsWindow.ParentWindow = self
        self.SettingsWindow.show()
        self.setEnabled(False)

            
    def Popup(self):
        self.Popup = PopUpWindow()
        self.Popup.ParentWindow=self
        self.Popup.Label= QtWidgets.QLabel(self.Popup)
        self.Popup.setWindowTitle("Ders Programı")
        self.Popup.setCentralWidget(self.Popup.Label)
        self.Popup.Label.setPixmap(self.Pixmap)
        self.Popup.setFixedSize(self.Pixmap.size())
        self.Popup.show()
        self.setEnabled(False)

    def resizeEvent(self, event):
        self.resized.emit()
        return super().resizeEvent(event)

    def ResizeScene(self):
        self.Height = self.frameGeometry().height()
        self.Width  = self.frameGeometry().width()
        
        self.View.setGeometry(300,30,self.Width-320,self.Height-90)
        
        if self.Height > 800 and self.Width > 1600:
            self.Label3.setGeometry(QtCore.QRect(145-self.Width3//2,self.Height-70-self.Height3,
                                                             self.Width3+5,self.Height3))
            self.spinBox1.setGeometry(QtCore.QRect(155+self.Width3//2, self.Height-70-self.Height3,
                                                   40, self.Height3))

    def keyPressEvent(self,event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.SettingsIO.writeSettings()
            self.close()
            
    def SaveImageFile(self):
        file_name,_= QtWidgets.QFileDialog.getSaveFileName(self, 'Open Image File', r"", "Image files (*.jpg *.jpeg *.gif *.png)")
        self.Pixmap.save(file_name,'PNG')
        
    def closeEvent(self,event):
        box = QtWidgets.QMessageBox()
        box.setText('Çıkmak mı istiyorsunuz?')
        box.setWindowTitle('Uyarı')
        box.setStandardButtons(QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
        evet = box.button(QtWidgets.QMessageBox.Yes)
        evet.setText('Evet')
        hayir = box.button(QtWidgets.QMessageBox.No)
        hayir.setText('Hayır')
        box.exec_()
        if box.clickedButton() == evet:
            self.SettingsIO.writeSettings()
            event.accept()
        elif box.clickedButton() == hayir:
            event.ignore()
            
    def AddItemtoNameList(self):
## Metin kutusunda yazılı olan metni al
        Text=self.TextBox1.text()
## Metin boş değiilse
        if Text:
## Metin listede değilse
            if Text not in self.SettingsIO.StaffList:
                Item=QtWidgets.QListWidgetItem(Text)
                self.ListWidget1.addItem(Item)
                self.SettingsIO.StaffList.append(Text)
                self.TextBox1.setText("")
                self.Label1Update()
            else:
                self.TextBox1.setText("")
                
    def LoadNameList(self):
        if self.SettingsIO.StaffList:
            for Name in self.SettingsIO.StaffList:
                Item=QtWidgets.QListWidgetItem(Name)
                self.ListWidget1.addItem(Item)
                
    def RemoveItemfromNameList(self):
        for Selection in self.ListWidget1.selectedItems():
            self.SettingsIO.StaffList.remove(Selection.text())
            self.ListWidget1.takeItem(self.ListWidget1.row(Selection))
        self.Label1Update()

    def ClearNameList(self):
        self.ListWidget1.clear()
        self.SettingsIO.StaffList.clear()
        self.Label1Update()

    def LoadClassList(self):
        if self.SettingsIO.ClassList:
            for Text in self.SettingsIO.ClassList:
                Class=Text.split()
                if len(Class) != 2:
                    continue
                elif not (Class[1].isupper() and Class[1].isalpha()):
                    continue
                else: 
                    try:
                        int(Class[0])
                    except: 
                        continue
                    else:
                        if int(Class[0]) <= 8:
                            Item=QtWidgets.QListWidgetItem(Text)
                            self.ListWidget2.addItem(Item)
                
    def AddItemtoClassList(self):
## Metin kutusunda yazılı olan metni al
        Text=self.TextBox2.text()
        Class= Text.split()
## Text bölündükten sonra bir sayı ve bir harften oluşan bir
## liste oluşmalı

## Listenin uzunluğu 2 değilse
        if len(Class) != 2:
            self.TextBox2.setText("")
## Listenin 2. elemanı büyük bir harf değilse
        elif not (Class[1].isupper() and Class[1].isalpha()):
            self.TextBox2.setText("")
        else: 
            try:
                int(Class[0])
            except: 
                self.TextBox2.setText("")
            else:
                if Class not in [Iter.split() for Iter in self.SettingsIO.ClassList]:
                    if int(Class[0]) in range(1,9):
                        Item=QtWidgets.QListWidgetItem(" ".join(Class))
                        self.ListWidget2.addItem(Item)
                        self.SettingsIO.ClassList.append(" ".join(Class))
                        self.TextBox2.setText("")
                        self.Label2Update()
                else:
                    self.TextBox2.setText("")

    def RemoveItemfromClassList(self):
        for Selection in self.ListWidget2.selectedItems():
            self.SettingsIO.ClassList.remove(Selection.text())
            self.ListWidget2.takeItem(self.ListWidget2.row(Selection))
        self.Label2Update()
        
    def ClearClassList(self):
        self.ListWidget2.clear()
        self.SettingsIO.ClassList.clear()
        self.Label2Update()

    def setClassHour(self):
        self.SettingsIO.NumberofHours= self.spinBox1.value()
        
    def Label1Update(self):
        self.Label1.setText("Kişiler: %d" % len(self.SettingsIO.StaffList))
        Width1  = self.Label1.fontMetrics().boundingRect(self.Label1.text()).width() 
        Height1 = self.Label1.fontMetrics().boundingRect(self.Label1.text()).height()
        self.Label1.setGeometry(QtCore.QRect(145-Width1//2,420-Height1,Width1+5,Height1))    

    def Label2Update(self):
        self.Label2.setText("Sınıflar: %d" % len(self.SettingsIO.ClassList))
        Width2  = self.Label2.fontMetrics().boundingRect(self.Label2.text()).width() 
        Height2 = self.Label2.fontMetrics().boundingRect(self.Label2.text()).height()
        self.Label2.setGeometry(QtCore.QRect(145-Width2//2,110-Height2,Width2+5,Height2))         

    def credits_method(self):
        bmsg = QtWidgets.QMessageBox()
        bmsg.setWindowTitle("Hakkında:")
        bmsg.setText("ODTÜ İLETİŞİM TOPLULUĞU\nMM-Z04, ODTÜ Kampüsü, Üniversiteler Mah. Dumlupınar Blv. No:1\n06800 Çankaya/Ankara \n \nProgramı hazırlayanlar: \nMuammer Buğra KURNAZ \nODTÜ Bilgisayar Mühendisliği öğrencisi \n\nÇağdaş YARDIMCI\nODTÜ Elektrik ve Elektronik Mühendisliği öğrencisi\n\nKatkıda bulunanlar:\nÇağla BİLGİN\n\nDaha fazla bilgi için:\nuser.ceng.metu.edu.tr/~e2448660/topluluk.html")
        bmsgexe = bmsg.exec_()

######################### UYGULAMA YÜRÜTMESİ ###########################
    def AppWorker(self,progress_callback):
        self.appLock()
## Ayarları güncelle.
        self.UpdateSettings()
## Olası hataları kontrol et.
        self.CheckForErrors()
        if not self.Error:
## Ders saatlerini yaz.
            self.WriteClassHours()
## Her ders saati için sınıflara kaç kişi gireceğine karar ver.
            self.FiilMegaSchedule()
            progress_callback.emit(1)
            time.sleep(1)
## Sınıflara etkinlik dağıt.
            self.AssignWorktoClasses()
            progress_callback.emit(2)
            time.sleep(1)
## Sınıflara kimlerin gireceğine karar ver.
            self.AssignPeopletoClasses()
            progress_callback.emit(3)
            time.sleep(1)
## Ders programını çizer ve kaydeder.
            self.DrawSchedule()
            progress_callback.emit(4)
            time.sleep(0.5)
## Sonraki yürütme için gereken değişkenleri sıfırla.
            self.reset()
            progress_callback.emit(0)
            self.appUnlock()
        else:
            self.reset()
            self.appUnlock()
            time.sleep(1.5)
            progress_callback.emit(0)
    def ProgressFunction(self,n):
        Progress={}
        Progress[0] =" Sihirbazı çalıştırmak için 'Çalıştır' butonuna basınız."
        Progress[1] =" Sınıflara kaçar kişi gireceği belirlendi."
        Progress[2] =" Sınıflarda yapılacak etkinliklere karar verildi."
        Progress[3] =" Hangi sınıfa kimlerin gireceğine karar verildi."
        Progress[4] =" Ders programının çizimi tamamlandı."
        self.Message.setText(Progress[n])
        
    def reset(self):
        self.ClassHours.clear()
        self.MegaSchedule.clear()
        self.ClassActivityList.clear()
        self.FinalizedSchedule.clear()
        self.MoreThanOnce.clear()
        self.ActivitiesForClasses.clear()
        self.Work.clear()
        
    def AppExecute(self):
        self.ThreadPool=QtCore.QThreadPool()
        WorkerThread = Worker(self.AppWorker)
        WorkerThread.signals.progress.connect(self.ProgressFunction)
        WorkerThread.signals.finished.connect(self.DisplaySchedule)
        self.ThreadPool.start(WorkerThread)
            
############################# ARKAPLAN #############################
    def UpdateSettings(self):
        self.MoreThanOnce=[Index for Index,Activity in enumerate(self.SettingsIO.ActivityList) if self.SettingsIO.ActivityList[Activity].MoreThanOnce]
        self.ActivitiesForClasses = [[] for Index in range(9)]
        for Index,Activity in enumerate(self.SettingsIO.ActivityList):
            if self.SettingsIO.ActivityList[Activity].Active:
                for Class in self.SettingsIO.ActivityList[Activity].SuitableClasses:
                    self.ActivitiesForClasses[Class].append(Index)
            else:
                continue
        for Index,Activity in enumerate(self.SettingsIO.ActivityList):
            self.Work[Index]=Activity
        self.Work[-1]= "Kütüphane Etkinliği"

    def CheckForErrors(self):
        ## Sınıflara uygun etkinlik sayısı
        GradesofClassrooms=[int(Class.split()[0]) for Class in self.SettingsIO.ClassList]
        self.Error=False
        for Grades in GradesofClassrooms:
            if not self.ActivitiesForClasses[Grades]:
                self.Message.setText(" %d. sınıflara uygun etkinlik bulunamadı, sihirbaz çalışmayı durduracaktır."% Grades)
                self.Error=True
                break
        
    def WriteClassHours(self):
        ClassStart       = self.SettingsIO.TimeSettings[0]
        ClassDuration    = self.SettingsIO.TimeSettings[1]
        BreakDuration    = self.SettingsIO.TimeSettings[2]
        LunchDuration    = self.SettingsIO.TimeSettings[3]
        ClassBeforeLunch = self.SettingsIO.ClassBeforeLunch
        NumberOfClasses  = self.SettingsIO.NumberofHours

        DayStart      = 60*ClassStart[0]    + ClassStart[1]
        ClassDuration = 60*ClassDuration[0] + ClassDuration[1]
        BreakDuration = 60*BreakDuration[0] + BreakDuration[1] 
        LunchDuration = 60*LunchDuration[0] + LunchDuration[1]
        for Class in range(NumberOfClasses):
            
            LunchBreak = int(Class >= ClassBeforeLunch)
            ClassStart = (DayStart + LunchBreak*(LunchDuration-BreakDuration) + Class*(ClassDuration+BreakDuration))%1440

            ClassStartHour   = ClassStart // 60
            ClassStartMinute = ClassStart % 60

            ClassStartMinute = str(ClassStartMinute).zfill(2)
            
            ClassEnd         = (ClassStart + ClassDuration)%1440

            ClassEndHour     = ClassEnd // 60
            ClassEndMinute   = ClassEnd % 60
            ClassEndMinute   = str(ClassEndMinute).zfill(2)
            
            self.ClassHours.append("{}.{} - {}.{}".format(ClassStartHour,ClassStartMinute,ClassEndHour,ClassEndMinute))      
        
    def FiilMegaSchedule(self):

        NumberofPeople = len(self.SettingsIO.StaffList)
        NumberofClasses= len(self.SettingsIO.ClassList)

        MinPeoplePerClass = NumberofPeople // NumberofClasses
        Remainder         = NumberofPeople %  NumberofClasses
        self.MegaSchedule=[[MinPeoplePerClass for Class in range(NumberofClasses)] for Hour in range(self.SettingsIO.NumberofHours)]
        [Hour,Class]=[0,0]

        CurrentRemainder        = Remainder
        CurrentNumberofPeople = NumberofPeople  
        while Hour < self.SettingsIO.NumberofHours:
            if CurrentRemainder == 0:
                CurrentRemainder        = Remainder
                CurrentNumberofPeople   = NumberofPeople  
                Class=0
                Hour+=1
            else:
                if random.random()>0.5 and self.MegaSchedule[Hour][Class] == MinPeoplePerClass :
                    self.MegaSchedule[Hour][Class]+=1
                    CurrentRemainder-=1
                    Class+=1
                else:
                    Class+=1
                if Class==NumberofClasses:
                    Class=0
        
    def AssignWorktoClasses(self):
        self.ClassActivityList=[[] for Hour in range(self.SettingsIO.NumberofHours)]
        Stack=[]
        CurrentHour      = 0
        CurrentClassroom = 0
## Her bir şubenin hangi sınıfta olduğunu tutan liste
        GradesofClassrooms=[int(Class.split()[0]) for Class in self.SettingsIO.ClassList]
        NumberofClassrooms= len(self.SettingsIO.ClassList)

        Conditions=[True,True]
        TraceBack=False
## Her seviye için bir sözlük oluşturarak seviyelere uygun etkinlikleri aşağıdaki listenin indisleriyle eşleştiren sözlük listesi
        ClassActivityDictionary = [{Activity:Index for [Index,Activity] in enumerate(Class)} for Class in self.ActivitiesForClasses]

## Her bir şubede şubenin seviyesine uygun olan etkinliklerin kaçar kere yapıldığını tutan listelerin listesi
        ClassActivityChecklist = [ClassActivityDictionary[Grade] for Grade in GradesofClassrooms]
        ClassActivityChecklist = [[0 for Index in Class] for Class in ClassActivityChecklist]

##Örnek:
##        ClassActivityDictionary[1]={2: 0, 3: 1, 4: 2, 10: 3, 11: 4, 16: 5, 17: 6}
##        self.SettingsIO.ClassList=["1 A","2 A","3 A","4 A","5 A","6 A"]
##        GradesofClassrooms[1]=2
##                                        I
##                                        V
##        ClassActivityChecklist[1]=[0,0,0,0,0,0,>
        while CurrentHour < self.SettingsIO.NumberofHours:
            if CurrentHour == self.SettingsIO.NumberofHours-1 and self.SettingsIO.LibraryHourCheck:
## Son saatte bütün sınıflara kütüphane etkinliği koyulacak.
                
##                self.ClassActivityList[CurrentHour]=[7 for Class in self.SettingsIO.ClassList]

                self.ClassActivityList[CurrentHour]=[-1 for Class in self.SettingsIO.ClassList]
                CurrentHour +=1
            else:
                CurrentGrade = GradesofClassrooms[CurrentClassroom]
## Şubeye etkinlik koymak için sınıflara uygun etkinlikler arasından bir etkinlik seç.
                Guess = random.choice(self.ActivitiesForClasses[CurrentGrade])
                Index = ClassActivityDictionary[CurrentGrade][Guess]
## Bir etkinlik aynı anda birden fazla sınıfta yapılabilen etkinliklerden değilse aynı ders saati içerisinde birden
## fazla kez seçilmemeli.
                Conditions[0]= Guess not in self.ClassActivityList[CurrentHour] or Guess in self.MoreThanOnce
## Bir etkinlik şubeye uygun bütün etkinlikler yapılmadan önce tekrarlanmamalı.
                Conditions[1]= ClassActivityChecklist[CurrentClassroom][Index] == min(ClassActivityChecklist[CurrentClassroom])

## Yapılan tahmin koşulları sağlıyorsa o şubeye o etkinliği koy ve sonraki şubeye geç.  
                if Conditions[0] and Conditions[1]:
                    Stack.append([CurrentHour,CurrentClassroom,Guess])
                    self.ClassActivityList[Stack[-1][0]].append(Stack[-1][2])
                    CurrentGrade = GradesofClassrooms[Stack[-1][1]]
                    Index         = ClassActivityDictionary[CurrentGrade][Stack[-1][2]]
                    ClassActivityChecklist[Stack[-1][1]][Index]+=1
## Sonraki şubeye geç.
                    CurrentClassroom+=1
                    TraceBack = False
## Bulunduğun ders saatindeki şubeler bitmişse sonraki ders saatine geç.
                    if CurrentClassroom==NumberofClassrooms:
                        CurrentClassroom=0
                        CurrentHour+=1
                else:
## Yapılan tahmin koşulları sağlamıyorsa o şubeye uygun bütün etkinliklere bak. Eğer koşulları
## sağlayan bir alternatif bulamazsan yaptıklarını geri sarmaya başla.
                    TraceBack=True
                    CurrentGrade = GradesofClassrooms[CurrentClassroom]
                    for Activity in self.ActivitiesForClasses[CurrentGrade]:
                        Conditions[0]= Activity not in self.ClassActivityList[CurrentHour] or Activity in self.MoreThanOnce
                        Index        = ClassActivityDictionary[CurrentGrade][Activity]
                        Conditions[1]= ClassActivityChecklist[CurrentClassroom][Index] == min(ClassActivityChecklist[CurrentClassroom])
## Koşulları sağlayan bir etkinlik bir etkinlik bulursan o etkinliği o şubeye koy ve
## sonraki şubeye geç.
                        if Conditions[0] and Conditions[1]:
                            Stack.append([CurrentHour,CurrentClassroom,Activity])
                            self.ClassActivityList[Stack[-1][0]].append(Stack[-1][2])
                            CurrentGrade = GradesofClassrooms[Stack[-1][1]]
                            Index         = ClassActivityDictionary[CurrentGrade][Stack[-1][2]]
                            ClassActivityChecklist[Stack[-1][1]][Index]+=1
## Sonraki şubeye geç.
                            CurrentClassroom+=1
                            TraceBack=False
## Bulunduğun ders saatindeki şubeler bitince sonraki ders saatine geç.
                            if CurrentClassroom==NumberofClassrooms:
                                CurrentClassroom=0
                                CurrentHour+=1
                            break
## Geri sarman gerekiyorsa:                        
                    if TraceBack:
                        Conditions[0]= Guess not in self.ClassActivityList[CurrentHour] or Guess in self.MoreThanOnce
                        Index        = ClassActivityDictionary[CurrentGrade][Guess]
                        Conditions[1]= ClassActivityChecklist[CurrentClassroom][Index] == min(ClassActivityChecklist[CurrentClassroom])
## Eğer aynı ders saati içerisinde birden fazla etkinlik seçmemek için kullanabilecek bir
## etkinliğin kalmadıysa o ders saatinde şubelere koyduğun etkinlikleri tamamen kaldırana kadar
## geri sar.
                        if not Conditions[0] and Conditions[1]:                                                   
                            while True:
                                if Stack[-1][0] != CurrentHour:
                                    [CurrentHour,CurrentClassroom]=End[:2]
                                    TraceBack=False
                                    break
                                self.ClassActivityList[Stack[-1][0]].remove(Stack[-1][2])
                                LastGrade    = GradesofClassrooms[Stack[-1][1]]
                                Index         = ClassActivityDictionary[LastGrade][Stack[-1][2]]
                                ClassActivityChecklist[Stack[-1][1]][Index]-=1
                                End=Stack.pop()      
## Eğer bir şubede etkinlik tekrarına düşmemek için kullanabileceğin alternatif bir etkinliğin
## yoksa önden tahmin ettiğin etkinliği koyduğun ders saatine kadar geri sar.
                        else:
                            Target=[CurrentClassroom,Guess]
                            while True:
                                if Stack[-1][1:] == Target:
                                    [CurrentHour,CurrentClassroom]=End[:2]
                                    TraceBack=False
                                    break
                                self.ClassActivityList[Stack[-1][0]].remove(Stack[-1][2])
                                LastGrade    = GradesofClassrooms[Stack[-1][1]]
                                Index         = ClassActivityDictionary[LastGrade][Stack[-1][2]]
                                ClassActivityChecklist[Stack[-1][1]][Index]-=1
                                End=Stack.pop()

## Listeyi oluşturduktan sonra listedeki sayıları etkinliklerle eşleştir.
        self.ClassActivityList = [[self.Work[CLASSROOM] for CLASSROOM in Hour] for Hour in self.ClassActivityList]
    
    def AssignPeopletoClasses(self):   
        Stack = [] ## [ROW,COLUMN,CELL,ID]

        Collision=False
        self.FinalizedSchedule=[[[] for Iter in range(len(self.SettingsIO.ClassList))] for Iter in range(len(self.MegaSchedule))]
## Listedeki her kişinin hangi sınıfa kaç kere girdiğini tutan liste
        ColumnCheck=[[0 for Iter in range(len(self.SettingsIO.StaffList))] for Iter in range(len(self.SettingsIO.ClassList))]
## Her ders saati için listedeki herkes için bir numara tutan liste
        IdList=[[Iter for Iter in range(len(self.SettingsIO.StaffList))] for Iter in range(len(self.MegaSchedule))]
        Row=0
        Column=0
        Cell=0
        while Row < len(self.MegaSchedule):
## Listedeki numaralardan birini seç.
            NextID=random.choice(IdList[Row])
## Seçtiğin numara şu anda bulunduğun sınıfta tekrara düşüyorsa (yani o numarayı
## o sınıfa diğerlerinden önce koymuşsan) bir alternatif ara:
            if ColumnCheck[Column][NextID] != min(ColumnCheck[Column]):
                Collision=True
## Eğer şu anda bulunduğun ders saatindeki numaralardan sınıfa uygun bir alternatif
## bulabiliyorsan onu seç.
                for Number in IdList[Row]:
                    if ColumnCheck[Column][Number] == min(ColumnCheck[Column]):
                        Collision=False
                        NextID=Number
                        break
## Eğer sınıf için seçimine alternatif olarak başka bir numara bulamadıysan seçtiğin
## seçtiğin numarayı bulunduğun sınıfa daha önce yerleştirdiğin saate kadar geri sar.
            if Collision:
                Target=[Column,NextID]
                while True:
                    if [Stack[-1][1],Stack[-1][3]] ==  Target:
                        [Row,Column,Cell]=Item[:3]
                        break
                    self.FinalizedSchedule[Stack[-1][0]][Stack[-1][1]].pop()
                    ColumnCheck[Stack[-1][1]][Stack[-1][3]]-=1
                    IdList[Stack[-1][0]].append(Stack[-1][3])
                    Item=Stack.pop()
                Collision=False
                continue
## Eğer seçimin çakışmaya sebep olmuyorsa onu mevcut sınıfa ekle.                
            if not Collision:
                ID=NextID
                Stack.append([Row,Column,Cell,ID])
                self.FinalizedSchedule[Stack[-1][0]][Stack[-1][1]].append(Stack[-1][3])
                ColumnCheck[Stack[-1][1]][Stack[-1][3]]+=1
                IdList[Stack[-1][0]].remove(Stack[-1][3])
## Sınıftaki sonraki öğrenciye geç.
                Cell+=1
## Sınıftaki öğrenciler bittiyse sonraki sınıfa geç.
                if Cell >= self.MegaSchedule[Row][Column]:
                    Column+=1
                    Cell=0
## Ders saatindeki sınıflar bittiyse sonraki ders ssatine geç.
                if Column > len(self.SettingsIO.ClassList)-1:
                    Row+=1
                    Column=0
                    Cell=0

    def DrawSchedule(self):
        Schedule  = self.FinalizedSchedule
## Satır/sütun çizgisi kalınlığı
        Thickness =3
## Etkinliklerin altındaki çizgilerin kalınlığı
        Thickness2=2
## Bütün stringlerin ekranda kaplayacağı boyutları tutan sözlük         
        StringSize={}
## Ders programına yazılacak her şeyi (ders saatleri ve sınıf isimleri dahil) tutacak liste
        ClassSchedule= [[[] for Column in range(len(Schedule[0])+1)] for Row in range(len(Schedule)+1)]
## Ders saatlerinde sınıflarda olacak isimlerin tek bir strıng içinde olduğu liste
        Names=[["\n".join([self.SettingsIO.StaffList[Name] for Name in Schedule[Row][Column]]) for Column in range(len(Schedule[Row]))] for Row in range(len(Schedule))]

## Standart font
        ImageFont1 = ImageFont.truetype("comic.ttf", 12)
## Ders saatlerinin fontu
        ImageFont2 = ImageFont.truetype("comic.ttf", 24)
## Sınıf isimlerinin fontu
        ImageFont3 = ImageFont.truetype("comic.ttf", 32)

## String boyutlarını sözlüğe yaz.
        for Class in self.SettingsIO.ClassList:
            StringSize[Class]=ImageFont3.getsize(Class)
        for Activity in self.Work:
            StringSize[self.Work[Activity]]=ImageFont1.getsize(self.Work[Activity])
        for Hours in self.ClassHours:
            StringSize[Hours]=ImageFont2.getsize(Hours)
        for Row in Names:
            for Name in Row:
                StringSize[Name]=ImageFont1.getsize_multiline(Name,spacing=8)
## Sınıfların isimlerini listeye işle.                      
        for Column,Class in enumerate(self.SettingsIO.ClassList):
            ClassSchedule[0][Column+1].append(Class)
## Ders saatlerini listeye işle
        for Rows,Hours in enumerate(self.ClassHours):
            ClassSchedule[Rows+1][0].append(Hours)
## Etkinlikleri ve kişileri listeye işleself.SettingsIO.ClassList
        for Row in range(1,len(Schedule)+1):
            for Column in range(1,len(Schedule[0])+1):
                ClassSchedule[Row][Column].append(self.ClassActivityList[Row-1][Column-1])
                ClassSchedule[Row][Column].append(Names[Row-1][Column-1])
## Her bir "hücre"nin (ders programındaki kutucuk) boyutlarını tutan liste 
        CellSizes=[[[StringSize[Name] for Name in ClassSchedule[Row][Column]] for Column in range(len(ClassSchedule[Row]))] for Row in range(len(ClassSchedule))]
        CellSizes[0][0]=[(0,0)]
        CellSizesCopy= CellSizes.copy()
        CellSizes  =[[(max([SIZE[0] for SIZE in CellSizes[Row][Column]]),sum([SIZE[1] for SIZE in CellSizes[Row][Column]])) for Column in range(len(CellSizes[Row]))] for Row in range(len(CellSizes))]
## Sütun çizgilerinin pozisyonlarını tutan liste
        ColumnWidth=[max([CellSizes[Row][Column][0]+Thickness for Row in range(len(CellSizes))]) for Column in range(len(CellSizes[0]))]
        ColumnWidth=[sum(ColumnWidth[:Column+1]) + 10*Column for Column in range(len(ColumnWidth))]
## Satır çizgilerinin pozisyonlarını tutan liste
        RowHeight  =[max([CellSizes[Row][Column][1]+Thickness for Column in range(len(CellSizes[Row]))]) for Row in range(len(CellSizes))]
        RowHeight  =[sum(RowHeight[:Row+1]) + 3*Thickness2*Row for Row in range(len(RowHeight))]

## Çizimin eni ve boyu
        Width =ColumnWidth[-1]+Thickness//2
        Height=RowHeight[-1]  +Thickness//2

        self.Image = Image.new("RGBA", (Width,Height), (255, 255, 255,0))
        self.Draw = ImageDraw.Draw(self.Image)

        XAverage=[ColumnWidth[0]//2]
        YAverage=[RowHeight[0]//2]
## Çizimdeki tek sayılı (1,3,...) sütünları boya.
        Even =[2*Index for Index in range(len(ColumnWidth)) if 2*Index+2 <= len(ColumnWidth)]
        for Column in Even:
            self.Draw.rectangle([ColumnWidth[Column],0,ColumnWidth[Column+1],RowHeight[-1]],fill=(180,120,110,200))
        self.Draw.rectangle([ColumnWidth[0],0,ColumnWidth[1],RowHeight[-1]],fill=(180,120,110,200))
        
## Çizimdeki çift sayılı (0,2,4...) sütunları boya.
        Odd =[2*Index+1 for Index in range(len(ColumnWidth)) if 2*Index+3 <= len(ColumnWidth)]
        for Column in Odd:
            self.Draw.rectangle([ColumnWidth[Column],0,ColumnWidth[Column+1],RowHeight[-1]],fill=(210,160,110,200))
        self.Draw.rectangle([0,0,ColumnWidth[0],RowHeight[-1]],fill=(210,160,110,200))             
## Her sütunun orta noktasını hesapla.
        for Column in range(len(ColumnWidth)-1):
            XAverage.append(sum(ColumnWidth[Column:Column+2])//2)
               
## Her satırın orta noktasını hesapla.
        for Row in range(len(RowHeight)-1):
            YAverage.append(sum(RowHeight[Row:Row+2])//2)
               
## Çizime sınıf isimlerini yaz.
        for Column in range(1,len(CellSizes[0])):
            self.Draw.text((XAverage[Column]-CellSizes[0][Column][0]//2,YAverage[0]-2-CellSizes[0][Column][1]//2),ClassSchedule[0][Column][0],font=ImageFont3, fill=(0,0,0))

## Çizime ders saatlerini yaz.
        for Row in range(1,len(CellSizes)):
            self.Draw.text((XAverage[0]-CellSizes[Row][0][0]//2,YAverage[Row]-CellSizes[Row][0][1]//2),ClassSchedule[Row][0][0],font=ImageFont2, fill=(0,0,0))

## Çizimdeki sınıfların içlerini doldur.
        for Row in range(1,len(CellSizesCopy)):
            for Column in range(1,len(CellSizesCopy[Row])):
## Etkinlik isimlerini yaz.
                self.Draw.text((XAverage[Column]-CellSizesCopy[Row][Column][0][0]//2,RowHeight[Row-1]+2),ClassSchedule[Row][Column][0],font=ImageFont1,fill=(0,0,0))
## Etkinlik isimlerinin altını çiz.
                self.Draw.line([XAverage[Column]-CellSizesCopy[Row][Column][0][0]//2,RowHeight[Row-1]+CellSizesCopy[Row][Column][0][1]+Thickness2,
                          XAverage[Column]+CellSizesCopy[Row][Column][0][0]//2,RowHeight[Row-1]+CellSizesCopy[Row][Column][0][1]+Thickness2],
                          width=Thickness2,fill=(0, 0, 0))
## Sınıftaki kişilerin ismini yaz.
                self.Draw.multiline_text((ColumnWidth[Column-1]+5,RowHeight[Row-1]+CellSizesCopy[Row][Column][0][1]+3*Thickness2),
                                                        ClassSchedule[Row][Column][1],spacing=8,font=ImageFont1,fill=(0,0,0))
## Satır çizgilerini çiz.
        for Row in RowHeight:
            self.Draw.line([0,Row,Width,Row],width=Thickness,fill=(0, 0, 0))
        self.Draw.line([0,0,0,Height],width=Thickness,fill=(0, 0, 0))

## Sütun çizgilerini çiz.
        for Column in ColumnWidth:
            self.Draw.line([Column,0,Column,Height],width=Thickness,fill=(0, 0, 0))
        self.Draw.line([0,0,Width,0],width=Thickness,fill=(0, 0, 0))

    def DisplaySchedule(self):
        if not self.Error:
            if self.PixmapItem != None:
                self.Scene.clear()
            self.Display    = ImageQt.ImageQt(self.Image)
            self.Pixmap     = QtGui.QPixmap.fromImage(self.Display)
            self.PixmapItem = QtWidgets.QGraphicsPixmapItem(self.Pixmap)
            self.Scene.addItem(self.PixmapItem)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = AppWindow()
    MainWindow.show()
  
    sys.exit(app.exec_()) 
