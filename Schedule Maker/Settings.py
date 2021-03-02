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

class SettingsMenuItem(QtWidgets.QTreeWidgetItem):

    def __init__(self,*args,Widget=None,**kwargs):
        self.Widget         = Widget
        self.args           = args
        self.kwargs         = kwargs
        super().__init__(*self.args,**self.kwargs)

class SettingsWindow(QtWidgets.QWidget):

    def __init__(self,ParentWindow=None,SettingsIO=None,*args,**kwargs):
        
        self.ParentWindow   = ParentWindow
        self.SettingsIO     = SettingsIO
        self.args           = args
        self.kwargs         = kwargs
        super().__init__(*self.args,**self.kwargs)

## Ağaç ve ağacın dalları        
        self.__TreeWidget = QtWidgets.QTreeWidget(self)
        self.__TreeWidget.setHeaderLabel("Ayarlar")
        
        self.__TopLevelItem1= SettingsMenuItem()
        self.__TopLevelItem1.setText(0, "Etkinlik Ayarları")
        
        self.__subItem1= SettingsMenuItem(self.__TopLevelItem1)
        self.__subItem1.setText(0,"Etkinlikleri Düzenle")
        self.__subItem1.Widget = QtWidgets.QWidget()
        
        self.__subItem2= SettingsMenuItem(self.__TopLevelItem1)
        self.__subItem2.setText(0,"Etkinlik Ekle/Çıkar")
        self.__subItem2.Widget = QtWidgets.QWidget()
        
        self.__TopLevelItem2= SettingsMenuItem()
        self.__TopLevelItem2.setText(0, "Ders Programı Ayarları")
        self.__TopLevelItem2.Widget = QtWidgets.QWidget()
        
        self.__TreeWidget.addTopLevelItem(self.__TopLevelItem1)
        self.__TreeWidget.addTopLevelItem(self.__TopLevelItem2)
        self.__TreeWidget.setGeometry(QtCore.QRect(30, 30, 200, 200))

        self.__TreeWidget.itemDoubleClicked.connect(lambda X: self.display(X.Widget))
        
## Dalların uçlarındaki widgetlar
        self.setupUI1()
        self.setupUI2()
        self.setupUI3()

## Widget yığını
        self.StackedWidget = QtWidgets.QStackedWidget(self)

        self.StackedWidget.setGeometry(QtCore.QRect(250, 20, 550, 600))
        
        self.StackedWidget.addWidget (self.__subItem1.Widget)
        self.StackedWidget.addWidget (self.__subItem2.Widget)
        self.StackedWidget.addWidget (self.__TopLevelItem2.Widget)        

## Pencere
        self.resize(800,600)
        self.setFixedSize(self.size())
        self.setWindowTitle(u"Ayarlar")
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.show()
      
    def setupUI1(self):
        VBoxLayout           = QtWidgets.QVBoxLayout()
        GroupBox             = QtWidgets.QGroupBox("Etkinlikleri Düzenle",self.__subItem1.Widget)

        GridLayout           = QtWidgets.QGridLayout()
        self.UI1ListWidget   = QtWidgets.QListWidget(self.__subItem1.Widget)
        self.initializeListWidget(self.UI1ListWidget)
        self.UI1ListWidget.currentRowChanged.connect(self.setupEditScreen)
        
        PushButton1          = QtWidgets.QPushButton("Kaydet",self.__subItem1.Widget)
        PushButton1.clicked.connect(self.saveUI1Edit)
        GridLayout.addWidget(self.UI1ListWidget,1,0,1,2)
        GridLayout.addWidget(PushButton1,0,4,1,1)
        
        SpacerItem1          = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        GroupBox1            = QtWidgets.QGroupBox("Sınıflar",self.__subItem1.Widget)
        GridLayout1          = QtWidgets.QGridLayout()
        GridLayout.addItem(SpacerItem1,1,3,1,1)
        
        self.UI1checkBoxList = [QtWidgets.QCheckBox("%d. Sınıf" % (Class+1),self.__subItem1.Widget) for Class in range(8)]
        for Class,checkBox in enumerate(self.UI1checkBoxList):
            GridLayout1.addWidget(checkBox,Class%4,(Class//4),1,1)
        GroupBox1.setLayout(GridLayout1)

        self.UI1checkBox1    = QtWidgets.QCheckBox("Bu etkinlik aynı ders saati içerisinde birden fazla kere yapılabilir.",self.__subItem1.Widget)        
        self.UI1checkBox2    = QtWidgets.QCheckBox("Ders programını hazırlarken bu etkinliği programa dahil et.",self.__subItem1.Widget)

        GridLayout.addWidget(GroupBox1,2,0,2,2)
        GridLayout.addWidget(self.UI1checkBox1,4,0,2,2)
        GridLayout.addWidget(self.UI1checkBox2,0,0,1,2)
        GroupBox.setLayout(GridLayout)            

    def setupEditScreen(self):
        Item         = self.UI1ListWidget.currentItem()
        ActivityName = Item.text()

        for Class in range(8):
            if Class+1 in self.SettingsIO.ActivityList[ActivityName].SuitableClasses:
                self.UI1checkBoxList[Class].setChecked(True)
            else:
                self.UI1checkBoxList[Class].setChecked(False)
                
        self.UI1checkBox1.setChecked(self.SettingsIO.ActivityList[ActivityName].MoreThanOnce)
        self.UI1checkBox2.setChecked(self.SettingsIO.ActivityList[ActivityName].Active)
        
    def saveUI1Edit(self):   
        Item         = self.UI1ListWidget.currentItem()
        ActivityName = Item.text()
        self.SettingsIO.ActivityList[ActivityName].SuitableClasses = [Class+1 for Class,checkBox in enumerate(self.UI1checkBoxList) if checkBox.isChecked()] 
        self.SettingsIO.ActivityList[ActivityName].MoreThanOnce    = self.UI1checkBox1.isChecked()
        self.SettingsIO.ActivityList[ActivityName].Active          = self.UI1checkBox2.isChecked()
        
    def setupUI2(self):
                               ####### Ders Çıkar ####### 
        GroupBox1            = QtWidgets.QGroupBox("Etkinlik Çıkar",self.__subItem2.Widget)        

        GridLayout1          = QtWidgets.QGridLayout()
        self.UI2ListWidget   = QtWidgets.QListWidget(self.__subItem2.Widget)
        self.initializeListWidget(self.UI2ListWidget)
        PushButton1          = QtWidgets.QPushButton("Çıkar",self.__subItem2.Widget)
        PushButton1.clicked.connect(self.RemoveActivity)
        
        GridLayout1.addWidget(self.UI2ListWidget,0,0,2,3)
        GridLayout1.addWidget(PushButton1,0,4,1,1)
        GroupBox1.setLayout(GridLayout1)
        
                               ####### Ders Ekle #######        
        GroupBox2            = QtWidgets.QGroupBox("Etkinlik Ekle",self.__subItem2.Widget)
        VBoxLayout2          = QtWidgets.QVBoxLayout()
        GridLayout2_1        = QtWidgets.QGridLayout()
        
        self.UI2LineEdit     = QtWidgets.QLineEdit(self.__subItem2.Widget)
        PushButton2          = QtWidgets.QPushButton("Ekle",self.__subItem2.Widget)
        PushButton2.clicked.connect(self.AddActivity)
        
        GridLayout2_1.addWidget(self.UI2LineEdit,0,0,1,3)
        GridLayout2_1.addWidget(PushButton2 ,0,4,1,1)
        
        GridLayout2_2        = QtWidgets.QGridLayout()

        GridLayout2          = QtWidgets.QGridLayout()
        GroupBox2_1          = QtWidgets.QGroupBox("Sınıflar",self.__subItem2.Widget)
        
        box2 = QtWidgets.QGridLayout()
        self.UI2checkBoxList = [QtWidgets.QCheckBox("%d. Sınıf" % (Class+1),self.__subItem2.Widget) for Class in range(8)]
        for Class,checkBox in enumerate(self.UI2checkBoxList):
            box2.addWidget(checkBox,Class%4,2*(Class//4),1,2)
            
        self.UI2checkBox     = QtWidgets.QCheckBox("Bu etkinlik aynı ders saati içerisinde birden fazla kere yapılabilir.")
        GroupBox2_1.setLayout(box2)

        GridLayout2_2.addWidget(GroupBox2_1,0,0,4,3)
        GridLayout2_2.addWidget(self.UI2checkBox,4,0,2,1)

        VBoxLayout2.addLayout(GridLayout2_1)
        VBoxLayout2.addSpacing(10)
        VBoxLayout2.addLayout(GridLayout2_2)
        GroupBox2.setLayout(VBoxLayout2)

                            ####### Ders Ekle/Çıkar #######
        GroupBox             = QtWidgets.QGroupBox("Etkinlik Ekle/Çıkar",self.__subItem2.Widget)  
        VBoxLayout           = QtWidgets.QVBoxLayout()
        VBoxLayout.addWidget(GroupBox2)
        VBoxLayout.addWidget(GroupBox1)
        GroupBox.setLayout(VBoxLayout)

    def initializeListWidget(self,Widget):
        for ActivityName in self.SettingsIO.ActivityList:
            ListItem= QtWidgets.QListWidgetItem(ActivityName)          
            Widget.addItem(ListItem)
            
    def AddActivity(self):
        ActivityName    = self.UI2LineEdit.text()
        if ActivityName in self.SettingsIO.ActivityList:
            pass
        
        else:
            if ActivityName:
                SuitableClasses    = [Class+1 for Class,checkBox in enumerate(self.UI2checkBoxList) if checkBox.isChecked()] 
                MoreThanOnce       = self.UI2checkBox.isChecked()
                self.SettingsIO.ActivityList[ActivityName]=Activity(ActivityName,SuitableClasses,MoreThanOnce=MoreThanOnce)
                UI1ListItem        = QtWidgets.QListWidgetItem(ActivityName)
                self.UI1ListWidget.addItem(UI1ListItem)
                UI2ListItem        = QtWidgets.QListWidgetItem(ActivityName)
                self.UI2ListWidget.addItem(UI2ListItem)
                self.UI2LineEdit.setText("")
                for checkBox in self.UI2checkBoxList:
                    checkBox.setChecked(False)
                self.UI2checkBox.setChecked(False)
            else:
                pass

    def RemoveActivity(self):
        CurrentRow   = self.UI2ListWidget.currentRow()
        Item         = self.UI2ListWidget.takeItem(CurrentRow)
        self.UI1ListWidget.takeItem(CurrentRow)
        ActivityName = Item.text()
        self.SettingsIO.ActivityList.pop(ActivityName,None)
        
    def setupUI3(self):
        GroupBox               = QtWidgets.QGroupBox("Ders Programı Ayarları",self.__TopLevelItem2.Widget)
        GridLayout             = QtWidgets.QGridLayout()

        self.UI3TimeSettings   = [QtWidgets.QTimeEdit(self.__TopLevelItem2.Widget) for Index in range(4)]
        
        Label1                 = QtWidgets.QLabel("Derslerin başlama saati:",self.__TopLevelItem2.Widget)        
        Label2                 = QtWidgets.QLabel("Derslerin süresi:",self.__TopLevelItem2.Widget)
        Label3                 = QtWidgets.QLabel("Teneffüs süresi:",self.__TopLevelItem2.Widget)
        Label4                 = QtWidgets.QLabel("Öğle arasının süresi:",self.__TopLevelItem2.Widget)
        Label5                 = QtWidgets.QLabel("Öğle arasından önceki ders sayısı:",self.__TopLevelItem2.Widget)
        self.UI3SpinBox1       = QtWidgets.QSpinBox(self.__TopLevelItem2.Widget)
        
        self.UI3CheckBox1      = QtWidgets.QCheckBox("Ders programının son saatine kütüphane kurma etkinliği koy.",self.__TopLevelItem2.Widget)
        PushButton1            = QtWidgets.QPushButton("Kaydet",self.__TopLevelItem2.Widget)
        
        self.initializeUI3()

        GridLayout.addWidget(Label1,0,0,1,1)
        GridLayout.addWidget(self.UI3TimeSettings[0],0,1,1,1)

        GridLayout.addWidget(PushButton1,0,2,1,1)
        PushButton1.clicked.connect(self.saveUI3Edit)
        
        GridLayout.addWidget(Label2,1,0,1,1)
        GridLayout.addWidget(self.UI3TimeSettings[1],1,1,1,1)
        
        self.UI3TimeSettings[1].setMinimumTime(QtCore.QTime(0,1))
        
        GridLayout.addWidget(Label3,2,0,1,1)
        GridLayout.addWidget(self.UI3TimeSettings[2],2,1,1,1)        

        GridLayout.addWidget(Label4,3,0,1,1)
        GridLayout.addWidget(self.UI3TimeSettings[3],3,1,1,1)        

        GridLayout.addWidget(Label5,4,0,1,1)
        GridLayout.addWidget(self.UI3SpinBox1,4,1,1,1)
        
        GridLayout.addWidget(self.UI3CheckBox1,5,0,1,2)
        self.UI3CheckBox1.stateChanged.connect(self.saveUI3Edit)
        
        GroupBox.setLayout(GridLayout)
        
    def saveUI3Edit(self):
        for Index in range(4):
            Hour = self.UI3TimeSettings[Index].time().hour()
            Minute= self.UI3TimeSettings[Index].time().minute()
            self.SettingsIO.TimeSettings[Index]= (Hour, Minute)

        self.SettingsIO.ClassBeforeLunch = self.UI3SpinBox1.value()
        self.SettingsIO.LibraryHourCheck = self.UI3CheckBox1.isChecked()

    def initializeUI3(self):
        for Index,TimeEdit in enumerate(self.UI3TimeSettings):
            TimeEdit.setTime(QtCore.QTime(self.SettingsIO.TimeSettings[Index][0],self.SettingsIO.TimeSettings[Index][1]))
        self.UI3SpinBox1.setValue(self.SettingsIO.ClassBeforeLunch)
        self.UI3CheckBox1.setChecked(self.SettingsIO.LibraryHourCheck) 
        
    def display(self,Widget):
        if Widget != None:
            Index = self.StackedWidget.indexOf(Widget)
            self.StackedWidget.setCurrentIndex(Index)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
            self.ParentWindow.setEnabled(True)
            
    def closeEvent(self,event) :
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
            event.accept()
            self.ParentWindow.setEnabled(True)
        elif box.clickedButton() == hayir:
            event.ignore()
