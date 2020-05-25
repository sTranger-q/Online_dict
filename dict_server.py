"""
在线词典服务端
"""
import pymysql
from socket import *
from select import *

# 全局变量
server_addr = ("0.0.0.0", 65534)


# M
class DictSql:
    def __init__(self):
        # 链接数据库
        self.db = pymysql.connect(user="root",
                                  password="z03104299",
                                  database="dict",
                                  charset="utf8")
        self.cur = self.db.cursor()

    def close(self):
        self.cur.close()
        self.db.close()

    def add_user(self, name, password):
        """
        将用户提交的用户名和密码插入到数据库的users表中
        :param name:
        :param password:
        :return: 如果插入成功，返回True  失败则返回None
        """
        try:
            sql = "insert into users(username,password) values(%s,%s);"
            self.cur.execute(sql, [name, password])
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return

    def verify_user(self, name, password):
        """
        通过用户提交的用户名和密码，验证用户名是否存在，以及密码是否正确
        :param name:
        :param password:
        :return:
        """
        sql = "select password from users where username=%s; "
        self.cur.execute(sql, [name])
        result = self.cur.fetchone()  # result-->tuple-->(password,)
        if not result:
            return "The username is not exist"  # 用户名不存在
        if password == result[0]:
            return "Login successfully"  # 验证成功
        return "Wrong password"  # 密码错误

    def search_word(self, word, username):
        """
        通过单词，查找并返回单词含义
        :param word:
        :param username:
        :return:
        """
        sql = "select mean from words where word=%s;"
        self.cur.execute(sql, [word])
        mean = self.cur.fetchone()  # mean-->(mean,)
        if not mean:
            return "No word find"
        # 将查找记录添加到history表中
        self.add_history(username, word, mean[0])
        return mean[0]

    def add_history(self, username, word, wmean):
        """
        将用户名，查找单词，单词含义，添加到history表中，生成历史记录
        :param username:
        :param wid:
        :param wmean:
        :return:
        """
        try:
            sql = "insert into history(username,word,wmean) values(%s,%s,%s);"
            self.cur.execute(sql, [username, word, wmean])
            self.db.commit()
        except:
            self.db.rollback()

    def look_history(self, username):
        """
        用过用户名，在history表中查找所有历史记录，并返回
        :param username:
        :return: tuple类型 返回历史记录，若没有，则返回空
        """
        sql = "select word,wmean,stime from history where username=%s;"
        self.cur.execute(sql, [username])
        result = self.cur.fetchall()  # result-->((word,wmean,stime),(word,wmean)....)
        if not result:
            return
        return result


# c
class DictServer:
    def __init__(self):
        self.sockfd = socket(AF_INET, SOCK_STREAM)
        self.sql = DictSql()

        # 套接字配置
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # 测试端口复用
        # 设置非阻塞
        self.sockfd.setblocking(False)
        self.sockfd.bind(server_addr)

        # IO监听列表
        self.rlist = []
        self.wlist = []
        self.xlist = []

    def start(self):
        self.sockfd.listen(5)
        self.rlist.append(self.sockfd)
        while True:
            rs, ws, xs = select(self.rlist, self.wlist, self.xlist)
            for fd in rs:
                if fd == self.sockfd:
                    connfd, addr = fd.accept()
                    print("Connect from:", addr)
                    # 设置非阻塞
                    connfd.setblocking(False)
                    self.rlist.append(connfd)
                else:
                    msg = fd.recv(1024).decode()
                    print(msg)
                    if not msg:
                        fd.close()
                        self.rlist.remove(fd)
                    request = msg.split("-")
                    if request[0] == "R":
                        self.register_user(fd, request[1], request[2])
                    elif request[0] == "L":
                        self.log_in(fd, request[1], request[2])
                    elif request[0] == "S":
                        self.search_wordmean(fd, request[1], request[2])
                    elif request[0] == "H":
                        self.search_history(fd, request[1])

    def register_user(self, fd, username, password):
        result = self.sql.add_user(username, password)
        if not result:
            fd.send(b"negative")
        fd.send(b"positive")

    def log_in(self, fd, username, password):
        result = self.sql.verify_user(username, password)
        fd.send(result.encode())

    def search_wordmean(self, fd, username, word):
        result = self.sql.search_word(word, username)
        fd.send(result.encode())

    def search_history(self, fd, username):
        result = self.sql.look_history(username)
        if not result:
            fd.send(b"negative")
        else:
            msg = "%s" % list(result)
            fd.send(msg.encode())


def main():
    ds = DictServer()
    ds.start()


if __name__ == '__main__':
    main()
