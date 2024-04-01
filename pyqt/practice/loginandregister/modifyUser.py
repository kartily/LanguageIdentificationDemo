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
class ModifyPage(QDialog):
    #定义
    def __init__(self):
        super( ModifyPage, self).__init__()
        _translate = QtCore.QCoreApplication.translate

        # 设置窗口
        self.setWindowTitle('用户信息修改')
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
        self.title_label.setText(_translate("ModifyPage", "用户信息修改"))  # 设置文本
        self.title_label.setFont(QFont('宋体', 20, QFont.Bold))  # 字体

        # 用户名密码
        self.name_label = QtWidgets.QLabel(self)
        self.name_label.setText(_translate("name_label", "用 户 名："))  # 设置文本
        self.name_label.setGeometry(QtCore.QRect(30, 80, 100, 50))
        self.name_label.setFont(QFont('宋体', 13, QFont.Bold))

        self.pwd1_label = QtWidgets.QLabel(self)
        self.pwd1_label.setText(_translate("pwd1_label", "原始密码："))  # 设置文本
        self.pwd1_label.setGeometry(QtCore.QRect(30, 140, 100, 50))
        self.pwd1_label.setFont(QFont('宋体', 13, QFont.Bold))

        self.pwd2_label = QtWidgets.QLabel(self)
        self.pwd2_label.setText(_translate("pwd2_label", "修改密码："))  # 设置文本
        self.pwd2_label.setGeometry(QtCore.QRect(30, 200, 100, 50))
        self.pwd2_label.setFont(QFont('宋体', 13, QFont.Bold))

        # 单行文本输入框
        self.username = QtWidgets.QLineEdit(self)  # 输入用户名
        self.username.setGeometry(QtCore.QRect(160, 80, 330, 40))
        self.username.setStyleSheet('''QLineEdit{font-size:12pt;
                                                   font-weight:400;
                                                   font-family: Roman times;} 
                                            QLineEdit:hover{color:black;
                                                   border:2px solid #000000;
                                                   font-size:12pt;
                                                   font-weight:400;
                                                   font-family: Roman times;}''')
        self.old_password = QtWidgets.QLineEdit(self)  # 输入密码
        self.old_password.setGeometry(QtCore.QRect(160, 140, 330, 40))
        self.old_password.setStyleSheet('''QLineEdit{font-size:12pt;
                                                   font-weight:400;
                                                   font-family: Roman times;} 
                                           QLineEdit:hover{color:black;
                                                   border:2px solid #000000;
                                                   font-size:12pt;
                                                   font-weight:400;
                                                   font-family: Roman times;}''')
        self.new_password = QtWidgets.QLineEdit(self)  # 确认密码
        self.new_password.setGeometry(QtCore.QRect(160, 200, 330, 40))
        self.new_password.setStyleSheet('''QLineEdit{font-size:12pt;
                                                   font-weight:400;
                                                   font-family: Roman times;} 
                                           QLineEdit:hover{color:black;
                                                   border:2px solid #000000;
                                                   font-size:12pt;
                                                   font-weight:400;
                                                   font-family: Roman times;}''')
        self.line_init() # 初始化

        # 按钮
        self.modify_btn = QtWidgets.QPushButton(self)
        self.modify_btn.setText(_translate("modify_btn", "修改"))
        self.modify_btn.setGeometry(QtCore.QRect(100, 270, 130, 50))
        self.modify_btn.setStyleSheet('''QPushButton{color:black;
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
        self.username.textChanged.connect(self.check_input)
        self.old_password.textChanged.connect(self.check_input)
        self.new_password.textChanged.connect(self.check_input)

        # 密码掩码显示
        self.old_password.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.new_password.setEchoMode(QLineEdit.PasswordEchoOnEdit)

        # service.userName = userName
        # print("username--",service.userName)

        # 注册提示
        self.username.setPlaceholderText('输入用户名')
        self.old_password.setPlaceholderText('输入密码')
        self.new_password.setPlaceholderText('输入新密码！')

    # 按钮初始化方法
    def pushbutton_init(self):
        # 设置注册按钮为不可点击状态，绑定槽函数
        self.modify_btn.setEnabled(False)
        self.modify_btn.clicked.connect(self.modify_func)
        # 取消按钮绑定取消注册槽函数
        self.cancel_btn.clicked.connect(self.cancel_func)

    # 检查输入方法,只有在三个文本输入框都有文字时，注册按钮才为可点击状态
    def check_input(self):
        if (self.username.text() and self.old_password.text()
                and self.new_password.text()):
            self.modify_btn.setEnabled(True)
        else:
            self.modify_btn.setEnabled(False)

    # 用户修改按钮 -- 连接数据库
    def modify_func(self):
        # 检查两次密码是否输入一致
        self.userName = self.username.text()
        self.old_password = self.old_password.text()
        self.new_password = self.new_password.text()
        print("username--",self.userName)
        print("newpwd--",self.new_password)
        # 查看原始用户名密码是否正确
        if self.userName and self.old_password: #非空
            # 向服务端发送登录请求-----------------数据可查询结果 -- 连接数据库查询
            result = service.query("select * from tb_user where username = %s and password = %s",self.userName,self.old_password)
            print("result1--",result)
            if result:  # 结果大于0
                print("111111111111111")
                #可以修改密码
                # result = exec("update tb_user set password =%s where username=%s ",('asd','bbb'))
                result2 = service.exec("update tb_user set password =%s where username=%s ",(self.new_password,self.userName))
                print("result2--",result2)
                # 如果记住密码 -- 删除
                is_remember = service.query("select * from tb_rem_data where username = %s and password = %s",self.userName,self.old_password)
                if is_remember:
                    is_delete = exec("delete from tb_user where username=%s ", service.userName)
                    print("is_delete--",is_delete)
                QMessageBox.information(self, '提示', '密码修改成功！')
            else:
                print("用户名或密码错误！")
                QMessageBox.information(self, '警告','用户名或密码错误！')
        else:
            QMessageBox.warning(self,'警告','请输入用户名和密码！')

    # 取消(如果用户在注册界面输入了数据，提示用户是否确认取消注册，如未输入数据则直接退出。)
    def cancel_func(self):
        self.close()


if __name__ == '__main__':
    page = QApplication(sys.argv)
    window = ModifyPage()
    window.show()
    sys.exit(page.exec())