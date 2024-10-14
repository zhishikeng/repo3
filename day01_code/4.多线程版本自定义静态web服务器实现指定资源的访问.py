import socket
import threading

def run(tcp_client_socket):
    # 5.接收客户端的请求信息 (请求报文)
    request_message = tcp_client_socket.recv(8192)

    if len(request_message) == 0:
        print("关闭浏览器了")
        tcp_client_socket.close()
    # 查看报文信息
    # print(request_message)
    request_message_list = request_message.decode(encoding="utf-8").split(" ", maxsplit=2)
    file_path = request_message_list[1]  # /images/%E8%B5%9B%E4%BA%8B_02.png


    # print(file_path,type(file_path))
    # file_path = file_path.decode(encoding = "utf-8")

    # if file_path == "/favicon.ico":
    #     pass

    # print(request_message_list)
    if file_path == "/":  # 根目录  则响应index.html默认资源
        # 6.读取请求对应的默认资源
        with open("lol/index.html", "rb") as r:
            file_data = r.read()
            # print(file_data)
        response_header = "HTTP/1.1 200 OK\r\n"
        # 7.2 响应行
        response_line = "Server: PWS1.0\r\n"
        # 7.3 响应体
        response_body = file_data
        response_data = (response_header + response_line + "\r\n").encode(encoding="utf-8") + response_body
        # 7.4 发送数据给客户端
        tcp_client_socket.send(response_data)
    else:
        try:
            with open("lol" + file_path, "rb") as r:
                file_data = r.read()
                # 7.组装响应报文
                # 7.1 响应头
                response_header = "HTTP/1.1 200 OK\r\n"
                # 7.2 响应行
                response_line = "Server: PWS1.0\r\n"
                # 7.3 响应体
                response_body = file_data
                response_data = (response_header + response_line + "\r\n").encode(encoding="utf-8") + response_body
                # 7.4 发送数据给客户端
                tcp_client_socket.send(response_data)
        except:
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
            tcp_client_socket.send(response_data)
        finally:
            # 7.5 释放资源
            tcp_client_socket.close()


if __name__ == '__main__':
    # 1, 创建socket对象 允许客户端浏览器进行建立连接
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 2.绑定端口
    tcp_server_socket.bind(("127.0.0.1",3344))
    # 3.设置监听
    tcp_server_socket.listen(128)

    while True:
        # 4.等待客户端链接
        tcp_client_socket,client_ip = tcp_server_socket.accept()

        # 当拿到客户端对象之和我们则需要开启多线程来处理请求
        thread = threading.Thread(target=run,args=(tcp_client_socket,))
        thread.setDaemon(True)
        thread.start()



