# -*- coding: utf-8 -*-
import sys
import pickle
import qtawesome
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt,pyqtSignal,QRegExp
from PyQt5.QtGui import QFont,QIcon,QRegExpValidator
from practice.loginandregister import service
from practice.loginandregister import register
from practice.mainpage import mainPage
# 用户登录页面
class LoginPage(QWidget):
    def __init__(self):
        super(LoginPage,self).__init__()
        _translate = QtCore.QCoreApplication.translate
        # 设置窗口标题
        self.setWindowTitle("系统登录")
        self.setWindowOpacity(0.95)  # 窗口透明度
        # 设置窗口大小，固定大小
        self.setFixedSize(550,350)

        # 设置图标
        self.setWindowIcon(QIcon('Amg.jpg'))  # 设置图标
        spin_icon = qtawesome.icon('fa5s.microphone-alt', color='black')
        # self.pushButton.setIcon(spin_icon)#设置图标
        self.setWindowIcon(spin_icon)

        # 标题
        self.title_label = QtWidgets.QLabel(self) #定义
        self.title_label.setGeometry(QtCore.QRect(75, 30, 400, 50))  #布局
        self.title_label.setAlignment(Qt.AlignCenter) #居中
        self.title_label.setText(_translate("LoginPage", "语种识别"))  #设置文本
        self.title_label.setFont(QFont('宋体', 20, QFont.Bold)) #字体

        # 用户名与密码
        self.name_label = QtWidgets.QLabel(self)
        self.name_label.setText(_translate("name_label", "用户名："))  #设置文本
        self.name_label.setGeometry(QtCore.QRect(30,90,80,50))
        self.name_label.setFont(QFont('宋体', 13, QFont.Bold))

        self.password_label = QtWidgets.QLabel(self)
        self.password_label.setText(_translate("name_label", "密  码："))  # 设置文本
        self.password_label.setGeometry(QtCore.QRect(30, 150, 80, 50))
        self.password_label.setFont(QFont('宋体', 13, QFont.Bold))

        #文本输入框
        self.name_line = QtWidgets.QLineEdit(self)  # 输入用户名
        self.name_line.setGeometry(QtCore.QRect(140,100,330,40))
        self.password_line = QtWidgets.QLineEdit(self)  # 输入密码
        self.password_line.setGeometry(QtCore.QRect(140, 155, 330, 40))
        self.line_init()  # 初始化

        # 复选框
        self.remember_password = QtWidgets.QCheckBox(self)
        self.remember_password.setText(_translate("remember_password", "记住密码"))
        self.remember_password.setGeometry(QtCore.QRect(400, 200, 150, 50))
        self.checkbox_init()  # 初始化

        # 登录按钮
        self.login_btn = QtWidgets.QPushButton(self)
        self.login_btn.setText(_translate("login_btn", "登录"))
        self.login_btn.setGeometry(QtCore.QRect(41, 270, 100, 50))
        self.login_btn.setStyleSheet('''QPushButton{color:black;
                            font:33 11pt "宋体";
                            border:2px solid #000000;
                            border-radius:25px;}
                        QPushButton:hover{color:white;
                            font:33 11pt "宋体";
                            border:2px solid #F3F3F5;
                            border-radius:25px;
                            background:darkGray;}''')
        # 注册按钮
        self.register_btn = QtWidgets.QPushButton(self)
        self.register_btn.setText(_translate("register_btn", "注册"))
        self.register_btn.setGeometry(QtCore.QRect(224, 270, 100, 50))
        self.register_btn.setStyleSheet('''QPushButton{color:black;
                                        font:33 11pt "宋体";
                                        border:2px solid #000000;
                                        border-radius:25px;}
                                QPushButton:hover{color:white;
                                        font:33 11pt "宋体";
                                        border:2px solid #F3F3F5;
                                        border-radius:25px;
                                        background:darkGray;}''')
        # 取消按钮
        self.exit_btn = QtWidgets.QPushButton(self)
        self.exit_btn.setText(_translate("exit_btn", "退出"))
        self.exit_btn.setGeometry(QtCore.QRect(407, 270, 100, 50))
        self.exit_btn.setStyleSheet('''QPushButton{color:black;
                                        font:33 11pt "宋体";
                                        border:2px solid #000000;
                                        border-radius:25px;}
                            QPushButton:hover{color:white;
                                    font:33 11pt "宋体";
                                    border:2px solid #F3F3F5;
                                    border-radius:25px;
                                    background:darkGray;}''')
        self.pushbutton_init()  # 初始化

    # 文本输入框初始化
    def line_init(self):
        # 设置提示语
        self.name_line.setPlaceholderText('输入用户名')
        self.password_line.setPlaceholderText('输入密码')
        # 设置字体样式
        self.name_line.setStyleSheet('''QLineEdit{font-size:12pt;
                                    font-weight:400;
                                    font-family: Roman times;} 
                            QLineEdit:hover{color:black;
                                    border:2px solid #000000;
                                    font-size:12pt;
                                    font-weight:400;
                                    font-family: Roman times;}''')
        self.password_line.setStyleSheet('''QLineEdit{font-size:12pt;
                                        font-weight:400;
                                        font-family: Roman times;} 
                                QLineEdit:hover{color:black;
                                        border:2px solid #000000;
                                        font-size:12pt;
                                        font-weight:400;
                                        font-family: Roman times;}''')
        # 密码掩码显示
        self.password_line.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        # # 设置检查单行文本输入框输入状态
        self.name_line.textChanged.connect(self.check_input)
        self.password_line.textChanged.connect(self.check_input)
        # 输入好用户名后--查看是否记住密码
        self.name_line.editingFinished.connect(self.insert_pwd)

    #检查文本输入框
    def check_input(self):
        # 当用户名及密码输入框均有内容时，设置登录按钮为可点击状态，或者不可点击。
        if self.name_line.text() and self.password_line.text():
            self.login_btn.setEnabled(True)
        else:
            self.login_btn.setEnabled(False)

    #自动填充密码
    def insert_pwd(self):
        name = self.name_line.text()
        password = service.query("select password from tb_rem_data where username = %s", name)
        print("password--",password)  # password-- (('aaa',),)
        if password:
            pwd = password[0][0]
        else:
            pwd=''
        # print("pwd--",pwd)  # pwd-- aaa
        if password:
            self.password_line.setText(pwd)

    # 按钮初始化
    def pushbutton_init(self):
        # # 先设置登录按钮为不可点击状态，当用户输入用户名及密码时才变为可点击状态
        self.login_btn.setEnabled(False)
        # 按钮点击绑定槽函数
        self.login_btn.clicked.connect(self.do_login)
        self.register_btn.clicked.connect(self.do_register)
        self.exit_btn.clicked.connect(self.close)

    # 复选框初始化
    def checkbox_init(self):
        self.remember_password.setStyleSheet('''QCheckBox{font-size:12pt;
                                                        font-weight:400;
                                                        font-family: Roman times;} ''')
        # 将复选框按钮状态变化信号绑定槽函数
        self.remember_password.stateChanged.connect(self.remember_password_func) #记住密码
        pass

    # 登录按钮
    def do_login(self):
        # 获取用户输入的用户名及密码
        service.userName =self.name_line.text()  # 全局变量，记录用户名
        self.password = self.password_line.text()  # 密码
        # print("username--",service.userName)
        # print("password--",self.password)
        if service.userName and self.password: #非空
            # 向服务端发送登录请求-----------------数据可查询结果 -- 连接数据库查询
            result = service.query("select * from tb_user where username = %s and password = %s",service.userName,self.password)
            print("result--",result)
            if result:  # 结果大于0
                # QMessageBox.information(self, '提示', '登录成功！')
                main_page = mainPage.MainWindow()
                main_page.exec()
            else:
                print("用户名或密码错误！")
                QMessageBox.information(self, '警告','用户名或密码错误！')
        else:
            QMessageBox.warning(self,'警告','请输入用户名和密码！')

    # 注册按钮 -- 向服务端发送注册请求 -- 跳转注册页面
    def do_register(self):
        register_page = register.RegisterPage()
        register_page.exec()

    # 记住密码 -- 用户名密码保存到数据库
    def remember_password_func(self): # 点击记住密码--输入用户名自动填充密码
        if self.remember_password.isChecked():
            #保存到数据库tb_rem_data中
            name = self.name_line.text()
            password = self.password_line.text()
            isNameExit = service.query("select * from tb_user where username = %s", name)
            if isNameExit:
                if name and password:  # 数据非空
                    isinsert = service.exec("insert into tb_rem_data(username,password) values (%s, %s)", (name, password))
                    print("isinsert to tb_rem_data--", isinsert)
                else:
                    pass


if __name__ == '__main__':
    page = QApplication(sys.argv)
    window = LoginPage()
    window.show()
    sys.exit(page.exec())
