"""
    UDP协议聊天室

"""
from socket import *
from threading import Thread,Event
from login import Login


class UdpServer:
    def __init__(self,addr):
        self.e= Event()
        self.server_addr=addr
        self.create_sock()
        self.bind()
        self.usre_list=[]
        self.login_db=Login()
        self.new_user=""
        self.new_user_addr=""

    def create_sock(self):
        self.sockfd=socket(AF_INET,SOCK_DGRAM)
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)

    def bind(self):
        self.sockfd.bind(self.server_addr)
        self.id=self.server_addr[0]
        self.port=self.server_addr[1]
    def register(self,data,addr):
        print("进入服务端　注册处理")
        msg=data.split("/")
        if len(msg)==2:
            if self.login_db.register(msg[0],msg[1]):
                self.sockfd.sendto(b"OK", addr)
            else:
                self.sockfd.sendto('账号已存在'.encode(), addr)
        else:
            self.sockfd.sendto('提交数据错误'.encode(), addr)

    def add_user(self):
        while True:

            self.e.wait()
            for item in self.usre_list:
                print(item)
                msg = "U/" + item[0]
                self.sockfd.sendto(msg.encode(), self.new_user_addr)
                msg = "U/" + self.new_user
                if item[0]!=self.new_user:
                    self.sockfd.sendto(msg.encode(), item[1])



            # self.l.release()
            self.e.clear()

    def login(self,data,addr):
        msg=data.split("/")
        if len(msg)==2:
            if self.login_db.login(msg[0],msg[1]):

                self.sockfd.sendto(b"OK",addr)
                self.usre_list.append((msg[0],addr))
                self.new_user=msg[0]
                self.new_user_addr=addr
                print(self.usre_list)
                self.e.set()
            else:
                self.sockfd.sendto('账号或密码错误'.encode(), addr)
        else:
            self.sockfd.sendto('提交数据错误'.encode(), addr)

    def send_message(self,msg):
        msg="M/"+msg
        for item in self.usre_list:
            self.sockfd.sendto(msg.encode(), item[1])



    def start_server(self):

        t = Thread(target=self.add_user)
        t.setDaemon(True)
        t.start()
        while True:
            data=self.sockfd.recvfrom(1024)
            msg=data[0].decode().split(" ")
            print("开始接受到数据")
            print(msg)
            if msg[0]=="R":
                print("进入到Ｒ处理")
                self.register(msg[-1],data[1])

            elif msg[0]=='L':
                self.login(msg[-1],data[-1])

            elif msg[0]=="P":
                msg=" ".join(msg[1:])
                self.send_message(msg)


            elif msg[0]=="Q":
                msg =msg[-1]
                print(msg)
                print(self.usre_list)
                for item in self.usre_list:
                    print("进入循环")
                    print(msg)
                    print(item[0])
                    if item[0]==msg:

                        self.usre_list.remove(item)
                        print("移除成功")
                print("客户端退出")



if __name__=='__main__':
    server_addr=("0.0.0.0",8888)
    udp_server=UdpServer(server_addr)
    udp_server.start_server()
