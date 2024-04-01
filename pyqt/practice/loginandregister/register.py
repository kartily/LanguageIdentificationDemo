# -*- coding: utf-8 -*-
import sys

import qtawesome
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt,pyqtSignal,QRegExp
from PyQt5.QtGui import QFont,QIcon,QRegExpValidator
from practice.loginandregister import service
import pickle

# 用户注册页面
class RegisterPage(QDialog):
    # 注册成功信号,传递列表信息
    successful_signal = pyqtSignal(list)
    #定义
    def __init__(self):
        super(RegisterPage, self).__init__()
        _translate = QtCore.QCoreApplication.translate

        # 设置窗口
        self.setWindowTitle('用户注册')
        self.setFixedSize(550,350)
        # self.setWindowOpacity(0.9)  # 窗口透明度

        # 设置图标
        self.setWindowIcon(QIcon('Amg.jpg'))  # 设置图标
        spin_icon = qtawesome.icon('fa5s.microphone-alt', color='black')
        # self.pushButton.setIcon(spin_icon)#设置图标
        self.setWindowIcon(spin_icon)

        # 标题
        self.title_label = QtWidgets.QLabel(self)  # 定义
        self.title_label.setGeometry(QtCore.QRect(75, 30, 400, 50))  # 布局
        self.title_label.setAlignment(Qt.AlignCenter)  # 居中
        self.title_label.setText(_translate("LoginPage", "欢迎注册"))  # 设置文本
        self.title_label.setFont(QFont('宋体', 20, QFont.Bold))  # 字体

        # 用户名密码
        self.name_label = QtWidgets.QLabel(self)
        self.name_label.setText(_translate("name_label", "用 户 名："))  # 设置文本
        self.name_label.setGeometry(QtCore.QRect(30, 80, 100, 50))
        self.name_label.setFont(QFont('宋体', 13, QFont.Bold))

        self.pwd1_label = QtWidgets.QLabel(self)
        self.pwd1_label.setText(_translate("name_label", "密    码："))  # 设置文本
        self.pwd1_label.setGeometry(QtCore.QRect(30, 140, 100, 50))
        self.pwd1_label.setFont(QFont('宋体', 13, QFont.Bold))

        self.pwd2_label = QtWidgets.QLabel(self)
        self.pwd2_label.setText(_translate("name_label", "确认密码："))  # 设置文本
        self.pwd2_label.setGeometry(QtCore.QRect(30, 200, 100, 50))
        self.pwd2_label.setFont(QFont('宋体', 13, QFont.Bold))

        # 单行文本输入框
        self.register_name = QtWidgets.QLineEdit(self)  # 输入用户名
        self.register_name.setGeometry(QtCore.QRect(160, 80, 330, 40))
        self.register_name.setStyleSheet('''QLineEdit{font-size:12pt;
                                                   font-weight:400;
                                                   font-family: Roman times;} 
                                            QLineEdit:hover{color:black;
                                                   border:2px solid #000000;
                                                   font-size:12pt;
                                                   font-weight:400;
                                                   font-family: Roman times;}''')
        self.register_pwd1 = QtWidgets.QLineEdit(self)  # 输入密码
        self.register_pwd1.setGeometry(QtCore.QRect(160, 140, 330, 40))
        self.register_pwd1.setStyleSheet('''QLineEdit{font-size:12pt;
                                                   font-weight:400;
                                                   font-family: Roman times;} 
                                           QLineEdit:hover{color:black;
                                                   border:2px solid #000000;
                                                   font-size:12pt;
                                                   font-weight:400;
                                                   font-family: Roman times;}''')
        self.register_pwd2 = QtWidgets.QLineEdit(self)  # 确认密码
        self.register_pwd2.setGeometry(QtCore.QRect(160, 200, 330, 40))
        self.register_pwd2.setStyleSheet('''QLineEdit{font-size:12pt;
                                                   font-weight:400;
                                                   font-family: Roman times;} 
                                           QLineEdit:hover{color:black;
                                                   border:2px solid #000000;
                                                   font-size:12pt;
                                                   font-weight:400;
                                                   font-family: Roman times;}''')
        self.line_init() # 初始化

        # 按钮
        self.register_btn = QtWidgets.QPushButton(self)
        self.register_btn.setText(_translate("register_btn", "注册"))
        self.register_btn.setGeometry(QtCore.QRect(100, 270, 130, 50))
        self.register_btn.setStyleSheet('''QPushButton{color:black;
                                                    font:33 11pt "宋体";
                                                    border:2px solid #000000;
                                                    border-radius:25px;}
                                            QPushButton:hover{color:white;
                                                    font:33 11pt "宋体";
                                                    border:2px solid #F3F3F5;
                                                    border-radius:25px;
                                                    background:darkGray;}''')
        self.cancel_btn = QtWidgets.QPushButton(self)
        self.cancel_btn.setText(_translate("cancel_btn", "取消"))
        self.cancel_btn.setGeometry(QtCore.QRect(320, 270, 130, 50))
        self.cancel_btn.setStyleSheet('''QPushButton{color:black;
                                                   font:33 11pt "宋体";
                                                   border:2px solid #000000;
                                                   border-radius:25px;}
                                           QPushButton:hover{color:white;
                                                   font:33 11pt "宋体";
                                                   border:2px solid #F3F3F5;
                                                   border-radius:25px;
                                                   background:darkGray;}''')
        self.pushbutton_init()  # 按钮初始化


    # 输入框初始化（用户名，密码）
    def line_init(self):
        # 单行文本输入框绑定按钮(只有三个输入框非空，才能点击注册)
        self.register_name.textChanged.connect(self.check_input)
        self.register_pwd1.textChanged.connect(self.check_input)
        self.register_pwd2.textChanged.connect(self.check_input)

        # 密码掩码显示
        self.register_pwd1.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.register_pwd2.setEchoMode(QLineEdit.PasswordEchoOnEdit)

        # 注册提示
        self.register_name.setPlaceholderText('输入用户名')
        self.register_pwd1.setPlaceholderText('输入密码')
        self.register_pwd2.setPlaceholderText('请再次确认密码！')

    # 按钮初始化方法
    def pushbutton_init(self):
        # 设置注册按钮为不可点击状态，绑定槽函数
        self.register_btn.setEnabled(False)
        self.register_btn.clicked.connect(self.register_func)
        # 取消按钮绑定取消注册槽函数
        self.cancel_btn.clicked.connect(self.cancel_func)

    # 检查输入方法,只有在三个文本输入框都有文字时，注册按钮才为可点击状态
    def check_input(self):
        if (self.register_name.text() and self.register_pwd1.text()
                and self.register_pwd2.text()):
            self.register_btn.setEnabled(True)
        else:
            self.register_btn.setEnabled(False)

    # 用户注册按钮 -- 连接数据库
    def register_func(self):
        # 检查两次密码是否输入一致
        username = self.register_name.text()
        password_1 = self.register_pwd1.text()
        password_2 = self.register_pwd2.text()
        if password_1 == password_2:  # 两次输入密码一致
            # 检查用户名是否重复（数据库）
            isNameRepeat = service.query("select * from tb_user where username = %s",username)
            print("isnamerepeat--",isNameRepeat)  #元祖形式存储
            if not(isNameRepeat):  # 不重复-保存进数据库-提示注册成功，是否跳转登录
                print("不重复--")
                # 向数据库中插入
                # result = exec("insert into tb_user(username,password) values (%s,%s)", ('qwe', 'qwe'))
                isinsert = service.exec("insert into tb_user(username,password) values (%s, %s)",(username,password_1))
                print("isinsert--",isinsert) #1
                choice = QMessageBox.information(self, '提示', '注册成功，是否登录？',
                                                 QMessageBox.Yes | QMessageBox.No)
                if choice == QMessageBox.Yes:  # 跳转
                    # 登录页面填充用户名密码
                    self.successful_signal.emit([self.register_name.text(),self.register_pwd1.text()])
                    # 关闭注册窗口
                    self.close()
                else:  # 不跳转，直接关闭
                    self.close()
            else:  # 重复 - 提示重复，清空输入框
                print("重复--")
                QMessageBox.warning(self, '警告', '用户名已被注册！')
                self.register_pwd1.setText('')  # 清空
                self.register_pwd2.setText('')
                self.register_name.setText('')
        else:  # 两次输入密码不一致
            QMessageBox.warning(self, '警告', '两次密码输入结果不一致！')
            self.register_pwd1.setText('')  # 清空
            self.register_pwd2.setText('')

    # 取消注册方法(如果用户在注册界面输入了数据，提示用户是否确认取消注册，如未输入数据则直接退出。)
    def cancel_func(self):
        if (self.register_name.text() or self.register_pwd1.text() or self.register_pwd2.text()):
            choice = QMessageBox.information(self,'提示','是否取消注册？', QMessageBox.Yes | QMessageBox.No)
            if choice == QMessageBox.Yes:
                self.close()
            else:
                return
        else:
            self.close()


if __name__ == '__main__':
    page = QApplication(sys.argv)
    window = RegisterPage()
    window.show()
    sys.exit(page.exec())