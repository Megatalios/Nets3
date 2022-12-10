import socket
from pathlib import Path


class Users(object):
    def __init__(self, login, password = "1111", value = "0"):
        self._login = login
        self._password = password
        self._value = value

    @property
    def login(self):
        return self._login

    @property
    def password(self):
        return self._password

    @property
    def value(self):
        return self._value

    def set_login(self, login):
        self._login = login

    def set_password(self, password):
        self._password = password

    def set_value(self, value):
        self._value = value

    def add_v(self):
        if not self._value.isdigit():
            self._value = "0"
        self._value = str(int(self._value) + 1)


if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 49521
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        print('Сервер запущен')
        flag = True
        list_users = []
        path1 = Path("login.txt")
        path2 = Path("password.txt")
        path3 = Path("value.txt")
        with open(path1, 'r') as logi, open(path2, 'r') as pword, open(path3, 'r') as val:
            for line in logi:
                list_users.append(Users(line.rstrip('\n'), pword.readline().rstrip('\n'), val.readline().rstrip('\n')))
            logi.close()
            pword.close()
            val.close()
        '''for element in list_users:
            print(element.login, end=' ')
            print(element.password, end=' ')
            print(element.value)'''
        while flag:
            conn, addr = s.accept()
            flag_login = True
            flag_password = True
            active_users = -1
            good_news = b'True'
            while True:
                print('Подключение к', addr)
                data = conn.recv(1024)
                data = data.decode('UTF-8')
                if data == 'stop':
                    flag = False
                    conn.send(b'Server stopped')
                    break
                if not data:
                    break
                if flag_login:
                    for element in list_users:
                        if data == element.login:
                            active_users = list_users.index(element)
                            flag_login = False
                            conn.sendall(good_news)
                            break
                    continue
                elif flag_password:
                    if data == element.password:
                        flag_password = False
                        conn.sendall(good_news)
                        list_users[active_users].add_v()
                        print(list_users[active_users].login + " зашел на сервер")
                        news = "Пользователь " + list_users[active_users].login + " посетил сервер уже: " + list_users[active_users].value + "\nServer stoped"
                        flag = False
                        with open(path3, 'w') as file:
                            for i in range(len(list_users)):
                                stroka = list_users[i].value + "\n"
                                file.write(stroka)
                            file.close()
                        conn.send(news.encode('UTF-8'))
                        break
                conn.sendall(b'LOL')
            conn.close()
        s.close()