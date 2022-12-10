import socket
if __name__ == "__main__":
    HOST = 'localhost'  # The server's hostname or IP address
    PORT = 49521        # The port used by the server


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        flag = True
        flag_login = True
        flag_password = True
        while flag:
            if flag_login:
                print("Пожалуйста введите логин")
            elif flag_password:
                print("Пожалуйста введите пароль")
            message = str(input()).encode('UTF-8')
            s.send(message)
            data = s.recv(1024)
            if message == b'stop':
                flag = False
                break
            if data == b'True':
                if flag_login:
                    flag_login = False
                elif flag_password:
                    flag_password = False
                    data = s.recv(1024)
                    data = data.decode('UTF-8')
                    print(data)
                    flag = False
                    break
        s.close()