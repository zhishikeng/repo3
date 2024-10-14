from pymysql import Connection
# Connection  就是Python语言与mysql之间的桥梁(通道)
# 呵呵 你看我成功了把!!!
# 你了不起
connection_list = [] #连接池  容器
for i in range(1,5):
    connection = Connection(
        user = "root",
        password = "root",
        host = "127.0.0.1",
        port = 3306,
        autocommit=True
    )
    connection_list.append(connection)
# 从容器中获取一个连接
def getConnection():
    return connection_list.pop()

# 归还
def releaseConnection(connection):
    connection_list.append(connection)
