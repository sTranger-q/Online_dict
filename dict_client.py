"""
在线词典客户端
"""
import sys
from socket import *
import datetime

server_addr = ("127.0.0.1", 65534)


# V
class User:
    def __init__(self):
        self.sockfd = socket(AF_INET, SOCK_STREAM)
        self.sockfd.connect(server_addr)

        # 界面控制
        self.page = 1

        self.username = None

    def start(self):

        while True:

            if self.page == 1:
                self.handle_pageone()
            elif self.page == 2:
                self.handle_pagetwo()

    def handle_pageone(self):
        print("""
            -----------------------------
            |        Hello Word         |
            |          1.登录            |
            |          2.注册            |
            |          3.退出            |
            -----------------------------
                        """)
        oder = input(">>>")
        if oder == "1":
            self.log_in()
        elif oder == "2":
            self.register_user()
        elif oder == "3":
            self.sockfd.close()
            sys.exit("Bye~")

    def log_in(self):
        username = input("请输入用户名：")
        password = input("请输入密码：")
        msg = "L-%s-%s" % (username, password)
        self.sockfd.send(msg.encode())
        response = self.sockfd.recv(1024).decode()
        print(response)
        if response == "Login successfully":
            self.username = username
            self.page = 2

    def register_user(self):
        username = input("请输入用户名：")
        password = input("请输入密码：")
        msg = "R-%s-%s" % (username, password)
        self.sockfd.send(msg.encode())
        response = self.sockfd.recv(1024).decode()
        if response == "positive":
            print("""
                    -------------------
                          注册成功
                        1.使用此用户登录
                        2.返回登录界面
                    --------------------
           """)
            order = input(">>>")
            if order == "1":
                self.username = username
                self.page = 2
        else:
            print("用户名已存在")

    def handle_pagetwo(self):
        print("""
            -----------------------------
                    Hello %s           
                     1.查询单词         
                     2.历史记录         
                     3.注销         
            -----------------------------
                        """ % self.username)
        order = input(">>>")
        if order == "1":
            self.search_word()
        elif order == "2":
            self.look_history()
        elif order == "3":
            self.username = None
            self.page = 1

    def search_word(self):
        word = input("请输入需要查询的单词: ")
        msg = "S-%s-%s" % (self.username, word)
        self.sockfd.send(msg.encode())
        response = self.sockfd.recv(1024).decode()
        format_title = "{:<15}{:<30}"
        print(format_title.format("word", "mean"))
        print(format_title.format(word, response))

    def look_history(self):
        msg = "H-%s" % self.username
        self.sockfd.send(msg.encode())
        response = self.sockfd.recv(1024 * 10).decode()
        if response == "negative":
            print("历史记录为空")
        else:
            list_history = eval(response)  # -->datetime.datetime(2020, 5, 25, 14, 19, 6)
            format_title = "{:^25}{:^15}{:^30}"
            print(format_title.format("time", "word", "mean"))
            print("=" * 70)
            for w in list_history:
                t = "%s" % w[2]
                print(format_title.format(t, w[0], w[1]))
                print("-" * 70)


if __name__ == '__main__':
    user = User()
    user.start()
