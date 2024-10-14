import socket
import threading
import json

class http_web_server(object):

    tcp_server_socket = None

    def __init__(self):
        # 1, 创建socket对象 允许客户端浏览器进行建立连接
        tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 2.绑定端口
        tcp_server_socket.bind(("127.0.0.1", 9527))
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
    # print(request_message)
    request_message_list = request_message.decode(encoding="utf-8").split(" ", maxsplit=2)
    file_path = request_message_list[1]  # /images/%E8%B5%9B%E4%BA%8B_02.png
    print(file_path)

    request_method = request_message_list[0]
    request_url = request_message_list[1]
    if request_method == "GET" and "/register" in request_url:
        # 表示从地址栏获取用户名以及密码 登录
        get_params = request_message_list[1].split("?")[1]
        # '{%22username%22:%22tom%22,%22password%22:18}'
        get_params = get_params.replace("%22","\"")
        json_data = json.loads(get_params)
        print(json_data) # 解析成功
        result_json = json.dumps(json_data)
        response_ok(result_json,new_socket)


def response_ok(file_data, new_socket):
    # 7.组装响应报文
    # 7.1 响应头
    response_header = "HTTP/1.1 200 OK\r\n"
    response_header += "Content-Type: application/json\r\n"
    response_header += "Access-Control-Allow-Origin: *\r\n"
    # 7.2 响应行
    response_line = "Server: PWS1.0\r\n"
    # 7.3 响应体
    response_body = file_data
    response_data = ((response_header + response_line + "\r\n") + response_body ).encode(encoding="utf-8")
    # 7.4 发送数据给客户端
    new_socket.send(response_data)


def response_error(new_socket):
    with open("lol/error.html", "rb") as r:
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
    hwserver = http_web_server()
    hwserver.start()

if __name__ == '__main__':
    main()














