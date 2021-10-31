#import command for gui
from sqlite3.dbapi2 import Time
import sys
from PyQt5.QtGui import QMatrix2x2
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QWidget

#import command for everything else
import sqlite3
import datetime
from operator import itemgetter
connection = sqlite3.connect('user.db')
myCursor = connection.cursor()

## TODO GUI
# login - done
# Signup - done
# welcome - done
# rsvp - done
# edit User
# main menu - done
# vaccination - done
# covid19 status - done
# create vaccination center - done
# list vaccination center(list) - done
# sort user list(list)
# admin page - done
# view appointment - done


# creating class for gui

class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("1welcome.ui", self)
        self.login_button.clicked.connect(self.goToLogin)
        self.sign_up_button.clicked.connect(self.goToSignUp)
        self.admin_login_button.clicked.connect(self.goToAdminPage)
    
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

    def checkLogin(self): #what to do when user sign in
        phoneNumber = self.text_edit_phone_number.text()
        icNumber = self.text_edit_ic_number.text()

        # hannah's code
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
        # hannah's code

    def goToSignUp(self):
        sign_up = SignupPage()
        widget.addWidget(sign_up)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToMainMenu(self, icNumber):
        mainMenu = MainMenu(icNumber)
        widget.addWidget(mainMenu)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        
class SignupPage(QDialog):
    def __init__(self):
        super(SignupPage, self).__init__()
        loadUi("1signup_page.ui", self)
        self.signup.clicked.connect(self.userSignUp)
        self.btn_goTologin.clicked.connect(self.goToLoginPage)

    def userSignUp(self): #what to do when user sign up
        # hannah's code
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
        # hannah's code

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

class RSVP(QDialog):
    def __init__(self, icNumber):
        super(RSVP, self).__init__()
        loadUi("2rsvp.ui", self)
        self.submit_rsvp.clicked.connect(lambda: self.SubmitRSVP(icNumber))
        self.radioButton_no.setChecked(True)

    def goToMainMenu(self, icNumber):
        main_menu = MainMenu(icNumber)
        widget.addWidget(main_menu)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def SubmitRSVP(self, icNumber):
        # hakeem's code
        result = False
        if self.radioButton_yes.isChecked():
            result = True
            # update rsvp info into database(delete appointment details to give new appointment)
            myCursor.execute("UPDATE userdata SET rsvp = :result WHERE ic_number = :IC", {'result':result, 'IC':icNumber})
            connection.commit()
            self.goToMainMenu(icNumber)
        else:
            # update rsvp info into database(delete appointment details to give new appointment)
            myCursor.execute("UPDATE userdata SET rsvp = :result, vaccination_date = :None, vaccination_time = :None, vaccination_venue = :None WHERE ic_number = :IC", {'result':result, 'IC':icNumber, "None":None, "None":None, "None":None})
            connection.commit()
            self.goToMainMenu(icNumber)
        # hakeem's code

class MainMenu(QDialog):
    def __init__(self, icNumber):
        super(MainMenu, self).__init__()
        loadUi("3main_menu.ui", self)
        self.btn_vaccination.clicked.connect(lambda: self.goToVaccination(icNumber))
        self.btn_covid19_status.clicked.connect(lambda: self.goToCovid19Status(icNumber))
        self.btn_logout.clicked.connect(self.logout)
        # nabilah's code
        myCursor.execute("SELECT user_name, vaccination_date, priority, priority1, priority2 from userdata WHERE ic_number = :IC", {'IC':icNumber})
        USERDATA = myCursor.fetchone()
        NAME = USERDATA[0]
        DATE = USERDATA[1]
        PRIORITY = USERDATA[2]
        PRIORITY1 = USERDATA[3]
        PRIORITY2 = USERDATA[4]
        
        self.label_greeting.setAlignment(QtCore.Qt.AlignCenter)
        self.label_greeting.setText("Hello " + NAME + "!")

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

    def logout(self):
        welcome_screen = WelcomeScreen()
        widget.addWidget(welcome_screen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class ViewAppointment(QDialog):
    def __init__(self, icNumber):
        super(ViewAppointment, self).__init__()
        loadUi("3view_appointment.ui", self)
        # nabilah's code
        myCursor.execute("SELECT vaccination_date, vaccination_time, vaccination_venue FROM userdata WHERE ic_number = :IC", {'IC':icNumber})
        USERDATA = myCursor.fetchone()
        DATE = USERDATA[0]
        TIME = USERDATA[1]
        VENUE = USERDATA[2]
        print(DATE, TIME, VENUE)
        
        self.label_date.setAlignment(QtCore.Qt.AlignCenter)
        self.label_time.setAlignment(QtCore.Qt.AlignCenter)
        self.label_venue.setAlignment(QtCore.Qt.AlignCenter)
        if DATE != None:
            self.label_date.setText(DATE)
            self.label_time.setText(TIME)
            self.label_venue.setText(VENUE)
            self.btn_rsvp
            self.btn_rsvp.clicked.connect(lambda: self.goToRSVP(icNumber))
        # nabilah's code

    def goToRSVP(self, icNumber):
        rsvp = RSVP(icNumber)
        widget.addWidget(rsvp)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class Vaccination(QDialog):
    def __init__(self, icNumber):
        super(Vaccination, self).__init__()
        loadUi("3vaccination_page.ui",self)
        self.radioButton_5.setChecked(True)
        self.submit_vaccination.clicked.connect(lambda: self.submitVaccination(icNumber))
        self.btn_goToMainMenu.clicked.connect(lambda: self.goToMainMenu(icNumber))

    def goToMainMenu(self, icNumber):
        main_menu = MainMenu(icNumber)
        widget.addWidget(main_menu)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def submitVaccination(self, icNumber):
        # nabilah's code
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
        # nabilah's code

class Covid19Status(QDialog):
    def __init__(self, icNumber):
        super(Covid19Status, self).__init__()
        loadUi("3covid19_status.ui", self)

        self.submit_covid19_status.clicked.connect(lambda: self.submitCOVID19Status(icNumber))
        self.btn_goToMainMenu.clicked.connect(lambda: self.goToMainMenu(icNumber))

    def goToMainMenu(self, icNumber):
        main_menu = MainMenu(icNumber)
        widget.addWidget(main_menu)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def submitCOVID19Status(self, icNumber):
        # nabilah's code
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
        
        myCursor.execute("UPDATE userdata SET q2_1 = :Q1, q2_2 = :Q2, q2_3 = :Q3, q2_4 = :Q4, q2_5 = :Q5, q2_6 = :Q6, q2_7 = :Q7, priority2 = :priority2 WHERE ic_number = :IC", {'Q1':Q1, 'Q2':Q2, 'Q3':Q3, 'Q4':Q4, 'Q5':Q5, 'Q6':Q6, 'Q7':Q7, 'priority2':priority2, 'IC':icNumber})
        connection.commit()
        self.goToMainMenu(icNumber)
        # nabilah's code

class AdminPage(QDialog):
    def __init__(self):
        super(AdminPage, self).__init__()
        loadUi("4admin_page.ui", self)
        self.create_center_button.clicked.connect(self.goToCreateCenter)
        self.update_user_button.clicked.connect(self.goToUpdateUserInfo)
        self.assign_appointment_button.clicked.connect(self.goToAssignAppointment)
        self.sort_list_button.clicked.connect(self.goToSortList)
        self.view_appontment_button.clicked.connect(self.goToViewAppointment)
        self.logout_button.clicked.connect(self.goToLogout)

    def goToCreateCenter(self):
        createcenter = CreateCenterPage()
        widget.addWidget(createcenter)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def goToUpdateUserInfo(self):
        pass

    def goToAssignAppointment(self):
        pass

    def goToSortList(self):
        pass

    def goToViewAppointment(self):
        view_users_appointment = ViewUsersAppointment()
        widget.addWidget(view_users_appointment)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToLogout(self):
        pass

class CreateCenterPage(QDialog): 
    def __init__(self):
        super(CreateCenterPage, self).__init__()
        loadUi("4create_center.ui", self)
        self.create_center.clicked.connect(self.CreateCenter)
        self.back_admin_page.clicked.connect(self.goToAdminPage)

    def CreateCenter(self): #create vaccination center
        # ajwad's code
        NAME = self.text_edit_name.text()
        POSTCODE = self.text_edit_postcode.text()
        ADDRESS = self.text_edit_address.toPlainText()
        CAPHOUR = self.text_edit_caphour.text()
        CAPDAY = self.text_edit_capday.text()

        #insert data to database
        myCursor.execute("INSERT INTO vaccinationCenters (name, postcode, address, capacityHour, capacityDay) VALUES (?, ?, ?, ?, ?)", 
        (NAME, POSTCODE, ADDRESS, CAPHOUR, CAPDAY))
        connection.commit()

        print("Vaccination center succesfuly created!")
        # ajwad's code
    
    def goToAdminPage(self):
        adminpage = AdminPage()
        widget.addWidget(adminpage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class ViewUsersAppointment(QDialog):
    def __init__(self):
        super(ViewUsersAppointment, self).__init__()
        loadUi("4list_vaccination_centers.ui", self)
        # set header for tableWidget
        self.tableWidget.setColumnWidth(0, 150)
        self.tableWidget.setColumnWidth(1, 400)
        self.tableWidget.setColumnWidth(2, 120)
        self.tableWidget.setColumnWidth(3, 120)
        self.tableWidget.setColumnWidth(4, 100)
        self.tableWidget.setColumnWidth(5, 100)
        self.tableWidget.setColumnWidth(6, 120)
        self.tableWidget.setHorizontalHeaderLabels(["IC", "NAME", "PHONE", "DATE", "TIME", "RSVP", "RISK GROUP"])
        self.loaddata()

    def loaddata(self):
        # adding center name into combo box
        # ajwad's code
        vacc_center_list = []
        myCursor.execute("SELECT name FROM vaccinationCenters")
        vacc_name = myCursor.fetchall()
        for i in vacc_name:
            for j in i:
                vacc_center_list.append(j)
        self.comboBox_vacc_center.addItems(vacc_center_list)
        self.btn_show.clicked.connect(self.showdata)
        # ajwad's code

    def showdata(self):
        # ajwad's code
        venue = self.comboBox_vacc_center.currentText()
        self.tableWidget.setRowCount(50)
        tableRow = 0
        # display user at the center in a table
        myCursor.execute("SELECT ic_number, user_name, phone_number, vaccination_date, vaccination_time, rsvp, state FROM userdata WHERE vaccination_venue = :venue LIMIT 50", {'venue':venue})
        userdata = myCursor.fetchall()
        for row in userdata:
            self.tableWidget.setItem(tableRow, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.tableWidget.setItem(tableRow, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.tableWidget.setItem(tableRow, 2, QtWidgets.QTableWidgetItem(row[2]))
            self.tableWidget.setItem(tableRow, 3, QtWidgets.QTableWidgetItem(row[3]))
            self.tableWidget.setItem(tableRow, 4, QtWidgets.QTableWidgetItem(row[4]))
            self.tableWidget.setItem(tableRow, 5, QtWidgets.QTableWidgetItem(row[5]))
            self.tableWidget.setItem(tableRow, 6, QtWidgets.QTableWidgetItem(row[6]))
            tableRow += 1
        # ajwad's code
        
#show gui
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