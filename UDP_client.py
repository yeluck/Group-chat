"""
    UDP聊天室客户端

"""
from socket import *
from threading import *
import sys
from PyQt5 import QtWidgets
import time

class ClientWindown(QtWidgets.QWidget):
    def __init__(self,udp_client):
        super().__init__()
        self.udp_client=udp_client
        self.start=False

    def closeEvent(self, event):
        """
            重写closeEvent方法，实现dialog窗体关闭时执行一些代码
            :param event: close()触发的事件
            :return: None
            """

        reply = QtWidgets.QMessageBox.question(self, '本程序', "是否要退出程序？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.udp_client.close_windows()
            event.accept()
        else:
            event.ignore()


    def main(self):
        self.resize(600, 500)
        self.setStyleSheet("background-color:rgb(255,255,255)")
        self.setWindowTitle("UDP在线聊天")

        self.login()


    def main_panel(self):
        """
        主要面板
        :return:
        """

        self.main_frame = self.frame(QtWidgets.QFrame(self), 0, 0, 600, 500, "background-color:rgb(155,155,155)")
        self.recv_frame = self.frame(QtWidgets.QTextBrowser(self.main_frame), 0, 0, 500, 350,"background-color:rgb(255,255,255)")
        self.title_lable = self.lable_frame("请输入", self.main_frame, 10, 355)
        self.send_input = self.frame(QtWidgets.QTextEdit(self.main_frame), 0, 380, 500, 90)
        self.user_fram=self.frame(QtWidgets.QTextBrowser(self.main_frame), 500, 0, 100, 500,"background-color:rgb(255,255,255)")


        self.send_button= self.frame(QtWidgets.QPushButton("发送", self.main_frame), 390, 475, 100, 20)
        self.send_button.clicked.connect(self.request)

    def login(self):
        """
        登录控制面板
        :return:
        """
        self.setWindowTitle("登录聊天室")
        self.login_frame=self.frame(QtWidgets.QFrame(self), 0, 0, 600, 500, "background-color:rgb(255,255,255)")
        self.login_title = self.lable_frame("请输入登录账号登录", self.login_frame, 220, 150)
        self.login_title_user = self.lable_frame("请输入账号", self.login_frame, 150, 200)
        self.login_title_pw = self.lable_frame("请输入密码", self.login_frame, 150, 240)
        self.login_user = self.frame(QtWidgets.QTextEdit(self.login_frame), 240, 195, 150, 30)
        self.login_pw = self.frame(QtWidgets.QTextEdit(self.login_frame), 240, 235, 150, 30)
        self.send_login = self.frame(QtWidgets.QPushButton("登录", self.login_frame), 170, 270, 100, 20)
        self.send_register = self.frame(QtWidgets.QPushButton("注册", self.login_frame), 290, 270, 100, 20)

        self.send_login.clicked.connect(self.login_request)

        self.send_register.clicked.connect(self.show_register)

    def show_register(self):
        """
        显示注册控制面板
        """
        self.login_frame.hide()
        self.register()
        self.register_frame.show()

    def register(self):
        """
        注册面板
        """
        self.setWindowTitle("注册聊天室账号")
        self.register_frame=self.frame(QtWidgets.QFrame(self), 0, 0, 600, 500, "background-color:rgb(255,255,255)")
        self.register_title = self.lable_frame("注册聊天室账号", self.register_frame, 220, 150)
        self.register_title_user = self.lable_frame("请输入账号", self.register_frame, 150, 200)
        self.register_title_pw = self.lable_frame("请输入密码", self.register_frame, 150, 240)
        self.register_user = self.frame(QtWidgets.QTextEdit(self.register_frame), 240, 195, 150, 30)
        self.register_pw = self.frame(QtWidgets.QTextEdit(self.register_frame), 240, 235, 150, 30)

        self.register_send_register = self.frame(QtWidgets.QPushButton("注册", self.register_frame), 240, 280, 150, 20)

        self.register_send_register.clicked.connect(self.register_request)

    def register_request(self):
        """
        注册请求处理
        """
        name=self.register_user.toPlainText()
        pw=self.register_pw.toPlainText()

        #如果输入框跟密码框不为空 则执行
        if name and pw:
            msg=self.udp_client.register(name,pw)
            if msg=='OK':
                self.register_frame.hide()
                self.login_frame.show()
            else:
                self.register_title.setText(msg)

    def login_request(self):
        """
        登录请求处理
        :return:
        """
        name = self.login_user.toPlainText()
        pw = self.login_pw.toPlainText()

        if name and pw:
            msg=self.udp_client.login(name,pw)
            if msg=="OK":
                self.main_panel()
                self.main_frame.show()

                t = Thread(target=self.recv_message)
                t.setDaemon(True)
                t.start()
            else:
                self.login_title.setText(msg)



    def request(self):
        """
        发送消息
        :return:
        """
        data=self.send_input.toPlainText()
        if data:
            self.udp_client.send_message(data)
            self.send_input.clear()


    def recv_message(self):
        """
        线程接收服务端信息程序
        :return:
        """
        while True:
            print("进入线程")
            msg, addr = self.udp_client.sockfd.recvfrom(1024)
            msg=msg.decode().split("/")
            if msg[0]=="M":
                msg=time.strftime("%H:%M:%S", time.localtime()) + '  '+ msg[1] +':\n'+ msg[2]
                self.recv_frame.append(msg)
            elif msg[0]=="U":
                self.user_fram.append(msg[1])




    def frame(self,qtype, x, y, width, height,style=""):
        # 框架
        _frame = qtype
        # 参数填:x,y,宽，高
        _frame.setGeometry(x, y, width, height)

        _frame.setStyleSheet(style)


        return _frame

    def lable_frame(self,str_name,frame,x,y):
        _frame=QtWidgets.QLabel(str_name, frame)
        _frame.move(x,y)
        return _frame



class UdpClient:
    def __init__(self,addr):
        self.server_addr=addr
        self.usre_name=""
        self.create_sock()

    def create_sock(self):
        self.sockfd=socket(AF_INET,SOCK_DGRAM)

    def register(self,name,pw):
        """
        处理注册请求
        :param name: 注册名称
        :param pw: 注册密码
        :return: 状态
        """
        data = "R " + name + "/" + pw
        self.sockfd.sendto(data.encode(), self.server_addr)
        data, addr = self.sockfd.recvfrom(1024)
        if data == b"OK":
            return "OK"
        else:
            return data.decode()

    def login(self,name,pw):
        print("进入登录客户端")

        user = name
        data = "L " + name + "/"+ pw
        self.sockfd.sendto(data.encode(), self.server_addr)
        data, addr = self.sockfd.recvfrom(1024)
        if data == b"OK":
            self.usre_name=user
            # t = Thread(target=self.recv_message)
            # t.setDaemon(True)
            # t.start()
            return "OK"

        else:
            return data.decode()

    def send_message(self,data):
        """
        聊天面板发送信息处理
        :param data:
        :return:
        """
        data = "P " + self.usre_name + "/" + data
        self.sockfd.sendto(data.encode(), self.server_addr)

    def close_windows(self):

        data = "Q " + self.usre_name
        self.sockfd.sendto(data.encode(), self.server_addr)





if __name__=='__main__':
    server_addr=("0.0.0.0",8888)
    udp_client=UdpClient(server_addr)

    app = QtWidgets.QApplication(sys.argv)
    client_windown = ClientWindown(udp_client)
    client_windown.main()
    client_windown.show()

    app.exec_()
