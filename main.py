# *********************************************************
# Program: main.py
# Course: PSP0101 PROBLEM SOLVING AND PROGRAM DESIGN
# Class: TC1V
# Trimester: 2110
# Year: 2021/22 Trimester 1
# Member_1: 1211103139 | HANNAH SOFEA BINTI ROSLEE | 1211103139@student.mmu.edu.my | +60123616790
# Member_2: 1211103830 | HAKEEM BIN AMINUDDIN | 1211103830@student.mmu.edu.my | +601121380773
# Member_3: 1211103183 | NURUL NABILAH BINTI MOHD NOOR HAKIM | 1211103183@student.mmu.edu.my | +60132027946
# Member_4: 1211103128 | MUHAMMAD AJWAD BIN MOHAMAD A'SIM | 1211103128@student.mmu.edu.my | +601154261979
# *********************************************************
# Task Distribution
# Member_1:Account sign up & login authentication
# Member_2:Menu and result display
# Member_3:Public user update information & view appointment
# Member_4:Administrator assign appointment,create vaccination center & generate list
# *********************************************************

########## import command for gui ##########
from sqlite3.dbapi2 import Time
import sys
from PyQt5.QtGui import QMatrix2x2
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QWidget

########### import command for everything else ##########
import sqlite3
import datetime
from operator import itemgetter

########## declaring connection and cursor for database ##########
connection = sqlite3.connect('user.db')
myCursor = connection.cursor()

########## creating class for GUI and implementing functions with GUI ##########

class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("1welcome.ui", self)
        self.login_button.clicked.connect(self.goToLogin)
        self.sign_up_button.clicked.connect(self.goToSignUp)
        self.admin_login_button.clicked.connect(self.goToAdminPage)
                
    # functions to navigate to other pages
    def goToLogin(self):
        login = LoginPage()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToSignUp(self):
        signup = SignupPage()
        widget.addWidget(signup)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToAdminPage(self):
        adminpage = AdminPage()
        widget.addWidget(adminpage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class LoginPage(QDialog):
    def __init__(self): 
        super(LoginPage, self).__init__()
        loadUi("1login_page.ui", self)
        self.login.clicked.connect(self.checkLogin)
        self.btn_goTosignup.clicked.connect(self.goToSignUp)

    # authenticate user phone number and ic during login
    def checkLogin(self): 
        phoneNumber = self.text_edit_phone_number.text()
        icNumber = self.text_edit_ic_number.text()

        if len(phoneNumber) == 0 or len(icNumber) == 0:
            self.label_error.setText("Please enter the required details.")
        else:
            query = myCursor.execute("SELECT rowid,* FROM userdata WHERE ic_number = :icNumber", {'icNumber':icNumber})
            for val in query:
                IC = val[3]
                PHONE = val[4]
            try:
                if IC == icNumber and PHONE == phoneNumber:
                    print("Succesfully logged in")
                    self.goToMainMenu(icNumber)
            except UnboundLocalError:
                self.label_error.setText("Phone number and IC number doesn't match.")
                self.text_edit_phone_number.setText("")
                self.text_edit_ic_number.setText("")

    # functions to navigate to other pages
    def goToSignUp(self):
        sign_up = SignupPage()
        widget.addWidget(sign_up)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToMainMenu(self, icNumber):
        mainMenu = MainMenu(icNumber)
        widget.addWidget(mainMenu)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        
class SignupPage(QDialog):
    def __init__(self): #5
        super(SignupPage, self).__init__()
        loadUi("1signup_page.ui", self)
        self.signup.clicked.connect(self.userSignUp)
        self.goToSignIn.clicked.connect(self.goToLoginPage)

    # update user data in database userdata when user signs up
    def userSignUp(self): 
        NAME = self.text_edit_name.text().strip().title()
        AGE = self.text_edit_age.text().strip()
        PHONE = self.text_edit_phone_number.text().strip()
        IC = self.text_edit_ic_number.text().strip()
        STATE = self.text_edit_state.text().strip()
        ADDRESS = self.text_edit_address.toPlainText().strip()

        myCursor.execute("INSERT INTO userdata (user_name , user_age, ic_number, phone_number, state, home_address) VALUES (?, ?, ?, ?, ?, ?)", 
        (NAME, AGE, IC, PHONE, STATE, ADDRESS))
        connection.commit()
        self.goToMainMenu(IC)

    # functions to navigate to other pages
    def goToLoginPage(self):
        login_page = LoginPage()
        widget.addWidget(login_page)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        self.clearBox()

    def goToMainMenu(self, icNumber):
        mainMenu = MainMenu(icNumber)
        widget.addWidget(mainMenu)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        self.clearBox()

    def clearBox(self):
        self.text_edit_name.setText("")
        self.text_edit_age.setText("")
        self.text_edit_phone_number.setText("")
        self.text_edit_ic_number.setText("")
        self.text_edit_state.setText("")
        self.text_edit_address.setText("")

class MainMenu(QDialog):
    def __init__(self, icNumber): #9
        super(MainMenu, self).__init__()
        loadUi("3main_menu.ui", self)
        self.btn_vaccination.clicked.connect(lambda: self.goToVaccination(icNumber))
        self.btn_covid19_status.clicked.connect(lambda: self.goToCovid19Status(icNumber))
        self.btn_edit_user.clicked.connect(lambda: self.goToEditUser(icNumber))
        self.btn_logout.clicked.connect(self.logout)
        
        myCursor.execute("SELECT user_name, vaccination_date, priority, priority1, priority2 from userdata WHERE ic_number = :IC", {'IC':icNumber})
        USERDATA = myCursor.fetchone()
        NAME = USERDATA[0]
        DATE = USERDATA[1]
        PRIORITY = USERDATA[2]
        PRIORITY1 = USERDATA[3]
        PRIORITY2 = USERDATA[4]
        
        self.label_greeting.setAlignment(QtCore.Qt.AlignCenter)
        self.label_greeting.setText("Hello " + NAME + "!")

        # checks whether user has appointment or not
        if DATE == None: 
            self.label_appointment_status.setText("Sorry, you don't have any appointment yet")
        else:
            self.btn_view_appointment.clicked.connect(lambda: self.goToViewAppointment(icNumber))

        # calculate priority(priority1 + priority2)
        if PRIORITY1 != None and PRIORITY2 != None:
            PRIORITY = int(PRIORITY1) + int(PRIORITY2)
            myCursor.execute("UPDATE userdata SET priority = :priority WHERE ic_number = :IC", {'priority':PRIORITY, 'IC':icNumber})
            connection.commit()
        # nabilah's code

    # functions to navigate to other pages
    def goToVaccination(self, icNumber):
        vaccination = Vaccination(icNumber)
        widget.addWidget(vaccination)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToCovid19Status(self, icNumber):
        covid19_status = Covid19Status(icNumber)
        widget.addWidget(covid19_status)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToViewAppointment(self, icNumber):
        view_appointment = ViewAppointment(icNumber)
        widget.addWidget(view_appointment)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToEditUser(self, icNumber):
        edit_user = EditUser(icNumber)
        widget.addWidget(edit_user)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def logout(self):
        welcome_screen = WelcomeScreen()
        widget.addWidget(welcome_screen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class ViewAppointment(QDialog):
    def __init__(self, icNumber): #10
        super(ViewAppointment, self).__init__()
        loadUi("3view_appointment.ui", self)
        myCursor.execute("SELECT vaccination_date, vaccination_time, vaccination_venue FROM userdata WHERE ic_number = :IC", {'IC':icNumber})
        USERDATA = myCursor.fetchone()
        DATE = USERDATA[0]
        TIME = USERDATA[1]
        VENUE = USERDATA[2]
        print(DATE, TIME, VENUE)
        
        # show appointment details to user
        self.label_date.setAlignment(QtCore.Qt.AlignCenter)
        self.label_time.setAlignment(QtCore.Qt.AlignCenter)
        self.label_venue.setAlignment(QtCore.Qt.AlignCenter)
        self.label_date.setText(DATE)
        self.label_time.setText(TIME)
        self.label_venue.setText(VENUE)
        self.btn_rsvp.clicked.connect(lambda: self.goToRSVP(icNumber))

    # function to navigate to other pages
    def goToRSVP(self, icNumber):
        rsvp = RSVP(icNumber)
        widget.addWidget(rsvp)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class Vaccination(QDialog):
    def __init__(self, icNumber): #11
        super(Vaccination, self).__init__()
        loadUi("3vaccination_page.ui",self)
        self.radioButton_5.setChecked(True)
        self.submit_vaccination.clicked.connect(lambda: self.submitVaccination(icNumber))
        self.btn_goToMainMenu.clicked.connect(lambda: self.goToMainMenu(icNumber))

    # function to navigate to other pages
    def goToMainMenu(self, icNumber):
        main_menu = MainMenu(icNumber)
        widget.addWidget(main_menu)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    # sumbit vaccination-related questions into database userdata
    def submitVaccination(self, icNumber): 
        Q1 = self.comboBox_q1_1.currentText()
        Q2 = self.comboBox_q1_2.currentText() 
        Q3 = self.comboBox_q1_3.currentText() 
        Q4 = self.comboBox_q1_4.currentText()
        Q5 = self.comboBox_q1_5.currentText()
        
        if self.radioButton_1.isChecked():
            Q6 = self.radioButton_1.text() 
        elif self.radioButton_2.isChecked():
            Q6 = self.radioButton_2.text()
        elif self.radioButton_3.isChecked():
            Q6 = self.radioButton_3.text()
        elif self.radioButton_4.isChecked():
            Q6 = self.radioButton_4.text()
        else:
            Q6 = self.radioButton_5.text()
        Q7 = self.comboBox_q1_7.currentText()

        priority1 = 0 
        # automate calculation of priority for user
        if Q1 == "Yes":
            priority1 += 1
        if Q2 == "Yes":
            priority1 += 1
        if Q3 == "Yes":
            priority1 += 1
        if Q4 == "Yes":
            priority1 += 1
        if Q5 == "Yes":
            priority1 += 1
        if Q6 == "Yes":
            priority1 += 1
        if Q7 == "Health-care worker": 
            priority1 += 1
        elif Q7 == "Community Services":
            priority1 += 1
        elif Q7 == "Workers":
            priority1 += 1
        elif Q7 == "Students":
            priority1 += 1
        
        # update questions and priority into database
        myCursor.execute("UPDATE userdata SET q1_1 = :Q1, q1_2 = :Q2, q1_3 = :Q3, q1_4 = :Q4, q1_5 = :Q5, q1_6 = :Q6, q1_7 = :Q7, priority1 = :priority1 WHERE ic_number = :IC", {'Q1':Q1, 'Q2':Q2, 'Q3':Q3, 'Q4':Q4, 'Q5':Q5, 'Q6':Q6, 'Q7':Q7, 'priority1':priority1, 'IC':icNumber})
        connection.commit()
        self.goToMainMenu(icNumber)

class Covid19Status(QDialog):
    def __init__(self, icNumber): #13
        super(Covid19Status, self).__init__()
        loadUi("3covid19_status.ui", self)

        self.submit_covid19_status.clicked.connect(lambda: self.submitCOVID19Status(icNumber))
        self.btn_goToMainMenu.clicked.connect(lambda: self.goToMainMenu(icNumber))

    # function to navigate to other pages
    def goToMainMenu(self, icNumber):
        main_menu = MainMenu(icNumber)
        widget.addWidget(main_menu)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    # submit covid-19-related questions into database userdata
    def submitCOVID19Status(self, icNumber):
        Q1 = self.comboBox_q2_1.currentText()
        Q2 = self.comboBox_q2_2.currentText() 
        Q3 = self.comboBox_q2_3.currentText() 
        Q4 = self.comboBox_q2_4.currentText()
        Q5 = self.comboBox_q2_5.currentText()
        Q6 = self.comboBox_q2_6.currentText()
        Q7 = self.comboBox_q2_7.currentText()

        priority2 = 0 #to declare variable priority2

        # automate calculation of priority for user
        if Q1 == "Yes":
            priority2 += 1
        if Q2 == "Yes":
            priority2 += 1
        if Q3 == "Yes":
            priority2 += 1
        if Q4 == "Yes":
            priority2 += 1
        if Q5 == "Yes":
            priority2 += 1
        if Q6 == "Yes":
            priority2 += 1
        if Q7 == "Yes":
            priority2 += 1
        
        # update questions and priority2 into database userdata
        myCursor.execute("UPDATE userdata SET q2_1 = :Q1, q2_2 = :Q2, q2_3 = :Q3, q2_4 = :Q4, q2_5 = :Q5, q2_6 = :Q6, q2_7 = :Q7, priority2 = :priority2 WHERE ic_number = :IC", {'Q1':Q1, 'Q2':Q2, 'Q3':Q3, 'Q4':Q4, 'Q5':Q5, 'Q6':Q6, 'Q7':Q7, 'priority2':priority2, 'IC':icNumber})
        connection.commit()
        self.goToMainMenu(icNumber)

class RSVP(QDialog):
    def __init__(self, icNumber):
        super(RSVP, self).__init__()
        loadUi("2rsvp.ui", self)
        self.submit_rsvp.clicked.connect(lambda: self.SubmitRSVP(icNumber))
        self.radioButton_no.setChecked(True)

    # function to navigate to other pages
    def goToMainMenu(self, icNumber):
        main_menu = MainMenu(icNumber)
        widget.addWidget(main_menu)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def SubmitRSVP(self, icNumber): #8
        # hakeem's code
        result = "No"
        if self.radioButton_yes.isChecked():
            result = "Yes"
            # update rsvp info into database userdata
            myCursor.execute("UPDATE userdata SET rsvp = :result WHERE ic_number = :IC", {'result':result, 'IC':icNumber})
            connection.commit()
            self.goToMainMenu(icNumber)
        else:
            # update rsvp info into database userdata(delete appointment details to give new appointment)
            myCursor.execute("UPDATE userdata SET vaccination_date = :None, vaccination_time = :None, vaccination_venue = :None WHERE ic_number = :IC", {'IC':icNumber, "None":None, "None":None, "None":None})
            connection.commit()
            self.goToMainMenu(icNumber)

class EditUser(QDialog):
    def __init__(self, icNumber):
        super(EditUser, self).__init__()
        loadUi("2edit_user.ui", self)
        newName = self.text_edit_new_name.text().strip()
        newPhone = self.text_edit_new_phone_number.text().strip()
        newIC = self.text_edit_new_ic_number.text().strip()
        newPostcode = self.text_edit_new_postcode.text().strip()
        newAddress = self.text_edit_new_address.toPlainText().strip()
        self.btn_update_new_info.clicked.connect(lambda: self.updateNewInfo(icNumber, newName, newPhone, newIC, newPostcode, newAddress))

    # function to navigate to other pages
    def goToMainMenu(self, icNumber):
        main_menu = MainMenu(icNumber)
        widget.addWidget(main_menu)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    # update new info into database userdata
    def updateNewInfo(self, icNumber, newName, newPhone, newIC, newPostcode, newAddress):
        if len(newIC) == 0: # if no input from user
            pass
        else:
            myCursor.execute(" UPDATE userdata SET ic_number = :newicNumber WHERE ic_number = :icNumber", {'icNumber':icNumber,'newicNumber':newIC})
            connection.commit()

        if len(newName) == 0: # if no input from user
            pass
        else:
            myCursor.execute(""" UPDATE userdata SET user_name = :newName WHERE ic_number = :icNumber""", {'icNumber':icNumber,'newName':newName})
            connection.commit()

        if len(newAddress) == 0: # if no input from user
            pass
        else:
            myCursor.execute("UPDATE userdata SET home_address = :newAddress WHERE ic_number = :icNumber " , {'icNumber':icNumber, 'newAddress':newAddress})
            connection.commit()

        if len(newPostcode) == 0: # if no input from user
            pass
        else:
            myCursor.execute("UPDATE userdata SET post_code = :newPostcode WHERE ic_number = :icNumber " , {'icNumber':icNumber, 'newAddress':newPostcode})
            connection.commit()

        if len(newPhone) == 0: # if no input from user
            pass
        else:
            myCursor.execute("UPDATE userdata SET phone_number = :newNumber WHERE ic_number = :icNumber " , {'icNumber':icNumber, 'newNumber':newPhone})
            connection.commit()
        
        self.goToMainMenu(icNumber)

class AdminPage(QDialog):
    def __init__(self): #15
        super(AdminPage, self).__init__()
        loadUi("4admin_page.ui", self)
        self.create_center_button.clicked.connect(self.goToCreateCenter)
        self.view_appontment_button.clicked.connect(self.goToViewAppointment)
        self.button_assign_appointment.clicked.connect(self.goToAssignAppointment)
        self.logout_button.clicked.connect(self.goToWelcome)

    # functions to navigate to other pages
    def goToCreateCenter(self):
        createcenter = CreateCenterPage()
        widget.addWidget(createcenter)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def goToViewAppointment(self):
        view_users_appointment = ViewUsersAppointment()
        widget.addWidget(view_users_appointment)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    def goToAssignAppointment(self):
        assign_appointment = AssignAppointment()
        widget.addWidget(assign_appointment)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToWelcome(self):
        welcome = WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class CreateCenterPage(QDialog): 
    def __init__(self): #16
        super(CreateCenterPage, self).__init__()
        loadUi("4create_center.ui", self)
        self.create_center.clicked.connect(self.CreateCenter)
        self.back_admin_page.clicked.connect(self.goToAdminPage)
    
    # create new vaccination center
    def CreateCenter(self): #create vaccination center
        NAME = self.text_edit_name.text()
        POSTCODE = self.text_edit_postcode.text()
        ADDRESS = self.text_edit_address.toPlainText()
        STATE = self.text_edit_state.text()
        CAPHOUR = self.text_edit_caphour.text()
        CAPDAY = self.text_edit_capday.text()

        #insert new vaccination center data to database vaccinationCenters
        myCursor.execute("INSERT INTO vaccinationCenters (name, postcode, address, state, capacityHour, capacityDay) VALUES (?, ?, ?, ?, ?, ?)", 
        (NAME, POSTCODE, ADDRESS, STATE, CAPHOUR, CAPDAY))
        connection.commit()
        self.goToAdminPage()
    
    # function to navigate to other pages
    def goToAdminPage(self):
        adminpage = AdminPage()
        widget.addWidget(adminpage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class ViewUsersAppointment(QDialog):
    def __init__(self):
        super(ViewUsersAppointment, self).__init__()
        loadUi("4list_vaccination_centers.ui", self)
        # set header for tableWidget GUI
        self.tableWidget.setColumnWidth(0, 150)
        self.tableWidget.setColumnWidth(1, 400)
        self.tableWidget.setColumnWidth(2, 120)
        self.tableWidget.setColumnWidth(3, 120)
        self.tableWidget.setColumnWidth(4, 100)
        self.tableWidget.setColumnWidth(5, 100)
        self.tableWidget.setColumnWidth(6, 120)
        self.tableWidget.setHorizontalHeaderLabels(["IC", "NAME", "PHONE", "DATE", "TIME", "RSVP", "RISK GROUP"])
        self.btn_goToAdminPage.clicked.connect(self.goToAdminPage)
        self.loaddata()

    def loaddata(self):
        # adding center name into combo box
        vacc_center_list = []
        myCursor.execute("SELECT name FROM vaccinationCenters")
        vacc_name = myCursor.fetchall()
        for i in vacc_name:
            for j in i:
                vacc_center_list.append(j)
        self.comboBox_vacc_center.addItems(vacc_center_list)
        self.btn_show.clicked.connect(self.showdata)

    def showdata(self):
        venue = self.comboBox_vacc_center.currentText()
        sortBy = self.comboBox_sortBy.currentText()
        if sortBy == "Name":
            n = 1
        elif sortBy == "IC Number":
            n = 0
        elif sortBy == "Vaccination Date":
            n = 3
        elif sortBy == "Vaccination Time":
            n = 4
        self.tableWidget.setRowCount(50)
        tableRow = 0

        # display user at a vaccination center in a table
        myCursor.execute(f"SELECT ic_number, user_name, phone_number, vaccination_date, vaccination_time, rsvp, state FROM userdata WHERE vaccination_venue = :venue", {'venue':venue})
        userdata = myCursor.fetchall()
        userdata.sort(key = lambda userdata: userdata[n])
        print(userdata)
        for row in userdata:
            self.tableWidget.setItem(tableRow, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.tableWidget.setItem(tableRow, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.tableWidget.setItem(tableRow, 2, QtWidgets.QTableWidgetItem(row[2]))
            self.tableWidget.setItem(tableRow, 3, QtWidgets.QTableWidgetItem(row[3]))
            self.tableWidget.setItem(tableRow, 4, QtWidgets.QTableWidgetItem(row[4]))
            self.tableWidget.setItem(tableRow, 5, QtWidgets.QTableWidgetItem(row[5]))
            self.tableWidget.setItem(tableRow, 6, QtWidgets.QTableWidgetItem(row[6]))
            tableRow += 1
    
    def goToAdminPage(self):
        admin_page = AdminPage()
        widget.addWidget(admin_page)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class AssignAppointment(QDialog):
    def __init__(self):
        super(AssignAppointment, self).__init__()
        loadUi("4assign_appointment.ui", self)
        # set header for tableWidget GUI
        self.tableWidget.setColumnWidth(0, 140)
        self.tableWidget.setColumnWidth(1, 500)
        self.tableWidget.setColumnWidth(2, 100)
        self.tableWidget.setColumnWidth(3, 150)
        self.tableWidget.setColumnWidth(4, 100)
        self.tableWidget.setColumnWidth(5, 130)
        self.tableWidget.setHorizontalHeaderLabels(["IC", "NAME", "AGE", "STATE", "PRIORITY", "RISK GROUP"])
        self.btn_goToAdminPage.clicked.connect(self.goToAdminPage)
        self.loaddata()

    def loaddata(self):
        # adding center name into combo box
        vacc_center_list = []
        myCursor.execute("SELECT name FROM vaccinationCenters")
        vacc_name = myCursor.fetchall()
        for i in vacc_name:
            for j in i:
                vacc_center_list.append(j)
        self.comboBox_vacc_center.addItems(vacc_center_list)

        # adding name of user without appointment into combo box
        myCursor.execute("SELECT rowid, * FROM userdata") #query all data from userdata table
        listUser = myCursor.fetchall() #store all data in database into a tuple in list listUser
        userWithoutAppointment = [i[1] for i in listUser if i[24] == None] # user_name
        self.comboBox_name.addItems(userWithoutAppointment)
        print(userWithoutAppointment)

        # show user without appointment in table
        userdata = [[i[3], i[1], i[2], i[30], i[21], i[3]] for i in listUser if i[24] == None] # 
        self.tableWidget.setRowCount(len(userdata))
        tableRow = 0
        for row in userdata:
            self.tableWidget.setItem(tableRow, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.tableWidget.setItem(tableRow, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.tableWidget.setItem(tableRow, 2, QtWidgets.QTableWidgetItem(row[2]))
            self.tableWidget.setItem(tableRow, 3, QtWidgets.QTableWidgetItem(row[3]))
            self.tableWidget.setItem(tableRow, 4, QtWidgets.QTableWidgetItem(row[4]))
            self.tableWidget.setItem(tableRow, 5, QtWidgets.QTableWidgetItem(row[5]))
            tableRow += 1

        # TODO CHECK AVAILABILITY ON THAT DAY/HOUR
        # getting info to update appointment for user
        date = str(self.calendarWidget.selectedDate())
        name = self.comboBox_name.currentText()
        time = self.comboBox_time.currentText()
        venue = self.comboBox_vacc_center.currentText()
        self.btn_submit.clicked.connect(lambda: self.updateData(name, date, time, venue))

    def updateData(self, name, date, time, venue):
        day = date[28:30].strip()
        month = date[25:27]
        year = date[19:23]
        userPerDay = 0
        userPerHour = 0

        print(date, time)
        print(day, month, year)

        # myCursor.execute("SELECT rowid FROM userdata WHERE vaccination_venue = :vaccVenue and vaccination_date = :vaccDate", {'vaccVenue':venue, 'vaccDate':f"{day}/{month}/{year}"})
        # userPerDay += len(myCursor.fetchall())

        # myCursor.execute("SELECT rowid FROM userdata WHERE vaccination_venue = :vaccVenue and vaccination_date = :vaccDate and vaccination_time = :vaccTime", {'vaccVenue':vaccCenter, 'vaccDate':f"{day}/{month}/{year}", 'vaccTime':f"{hour}:00"})
        # userThisHour = myCursor.fetchall()
        # userPerHour += (len(userThisHour))

        # myCursor.execute("UPDATE userdata SET vaccination_date = :date, vaccination_time = :time, vaccination_venue= :venue WHERE user_name = :name", {'date':date, 'time':time, 'venue':venue, 'name':name})
        # connection.commit()
        # self.goToAdminPage()

    def goToAdminPage(self):
        admin_page = AdminPage()
        widget.addWidget(admin_page)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        
########## show gui ##########
app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(800)
widget.setFixedWidth(1200)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting.......")
    connection.close()