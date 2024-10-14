import socket
import threading
from pymysql import *
from ConnectionConfig import *


import sys
class http_web_server(object):

    tcp_server_socket = None
    port = None

    def __init__(self,port):
        # 1, 创建socket对象 允许客户端浏览器进行建立连接
        tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 2.绑定端口
        tcp_server_socket.bind(("127.0.0.1", port))
        # 3.设置监听
        tcp_server_socket.listen(128)
        self.tcp_server_socket = tcp_server_socket

    # 谁在调用 主线程
    def start(self):
        while True:
            # 1.通过self获取tcpserver对象
            new_socket,client_ip = self.tcp_server_socket.accept()
            # 2.创建线程开启新任务
            thread_handler = threading.Thread(target=handler_client_result,args=(new_socket,))
            # 3.设置守护线程
            thread_handler.setDaemon(True)
            # 4.开启线程
            thread_handler.start()


def handler_client_result(new_socket):
    # 5.接收客户端的请求信息 (请求报文)
    request_message = new_socket.recv(8192)
    if len(request_message) == 0:
        print("关闭浏览器了")
        new_socket.close()
    # 查看报文信息

    request_message_list = request_message.decode(encoding="utf-8").split(" ", maxsplit=2)
    # print(request_message_list)

    # 判断请求方式
    request_method = request_message_list[0]
    request_url = request_message_list[1]
    if request_url != "/login.html" and request_method == "GET" and  "/login" in request_url:
        # 表示从地址栏获取用户名以及密码 登录
        get_params = request_message_list[1].split("?")[1]
        username = get_params.split("&")[0].split("=")[1]
        password = get_params.split("&")[1].split("=")[1]
        # print(username,password)
        conn = getConnection()
        sql = f"select * from t_users where username = \"{username}\" and password = \"{password}\""
        conn.select_db("demo01")
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        if result == None:
            response_error(new_socket)
            return
        if len(result) > 0:
            # 登录成功跳转到登录页面
            with open("web/index.html", "rb") as r:
                file_data = r.read()
            response_ok(file_data, new_socket)



    if request_method == "POST" and request_url in "/register":
        # 表示从请求体获取用户名以及密码 注册
        post_params = request_message_list[len(request_message_list) - 1].split("\r\n")[-1]
        username = post_params.split("&")[0].split("=")[1]
        password = post_params.split("&")[1].split("=")[1]
        # print(username,password)
        conn = getConnection()
        sql = f"insert into t_users(username,password) values(\"{username}\",\"{password}\")"
        conn.select_db("demo01")
        cursor = conn.cursor()
        cursor.execute(sql)
        # 注册成功跳转到登录页面
        with open("web/login.html", "rb") as r:
            file_data = r.read()
        response_ok(file_data, new_socket)


    file_path = request_message_list[1]  # /images/%E8%B5%9B%E4%BA%8B_02.png
    # print(request_message_list)
    if file_path == "/":  # 根目录  则响应index.html默认资源
        # 6.读取请求对应的默认资源
        with open("web/login.html", "rb") as r:
            file_data = r.read()
        response_ok(file_data, new_socket)
    else:
        try:
            with open("web" + file_path, "rb") as r:
                file_data = r.read()
            response_ok(file_data, new_socket)
        except:
            response_error(new_socket)
        finally:
            # 7.5 释放资源
            new_socket.close()


def response_ok(file_data, new_socket):
    # 7.组装响应报文
    # 7.1 响应头
    response_header = "HTTP/1.1 200 OK\r\n"
    # 7.2 响应行
    response_line = "Server: PWS1.0\r\n"
    # 7.3 响应体
    response_body = file_data
    response_data = (response_header + response_line + "\r\n").encode(encoding="utf-8") + response_body
    # 7.4 发送数据给客户端
    new_socket.send(response_data)


def response_error(new_socket):
    with open("web/error.html", "rb") as r:
        file_data = r.read()
    # 响应404
    response_header = "HTTP/1.1 404 OK\r\n"
    # 7.2 响应行
    response_line = "Server: PWS1.0\r\n"
    # 7.3 响应体
    response_body = file_data
    response_data = (response_header + response_line + "\r\n").encode(encoding="utf-8") + response_body
    # 7.4 发送数据给客户端
    new_socket.send(response_data)


def main():
    # params = sys.argv
    # # print(params)
    # port = 0
    # if len(params) == 0:
    #     port = 8000
    # if len(params) >= 2:
    #     port = int(params[1])
    port = 9999
    hwserver = http_web_server(port)
    hwserver.start()

if __name__ == '__main__':

    main()














