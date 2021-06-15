from socket import *
from threading import *
import ranword as rdw

class Quizserver:
    clients = list() #접속한 클라이언트의 정보 리스트
    clients_colors = list()
    clients_names = list()
    re_message = ''
    quizlist = list()
    chg_idx = 100

    def __init__(self):
        self.s_sock = socket(AF_INET, SOCK_STREAM)
        self.ip = ''
        self.port = 2505
        self.s_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.s_sock.bind((self.ip, self.port))
        print("유저 기다리는 중...")
        self.s_sock.listen(6)
        self.c_accept() #클라이언트 접속

    def c_accept(self):
        while True:
            client = c_socket, (ip, port) = self.s_sock.accept()
            if client not in self.clients: #기존 클라이언트 아닐 경우
                self.clients.append(client)
            print(ip, ':', str(port), '연결.')
            t = Thread(target=self.m_receive, args=(c_socket,)) #계속 받는 상태로
            t.start() # 실행.

    def m_receive(self, c_socket):
        while True:
            try:
                message = c_socket.recv(1024)
                if not message:
                    break
            except:
                continue
            else:
                self.re_message = message.decode('utf-8')
                if len(self.clients) != len(self.clients_colors): # 각 플레이어 색 반환
                    self.clients_colors.append(self.re_message)
                    self.re_message = ','.join(self.clients_colors) + 'color'
                elif len(self.clients) != len(self.clients_names): # 각 플레이어 이름 반환
                    self.clients_names.append(self.re_message)
                    self.re_message = ','.join(self.clients_names) + 'name'
                if self.re_message == 'start': # 게임시작 누르면
                    for i in range(0,10):
                        self.quizlist.append(rdw.ranword())
                if '\n' in self.re_message: # 정답 맞출 경우
                    self.chg_idx = int(self.re_message[self.re_message.index('\n')+1:])
                    self.quizlist[self.chg_idx] = rdw.ranword()
                    self.re_message += '\n' + self.quizlist[self.chg_idx]
                self.send_all(c_socket)

        c_socket.close()

    def send_all(self,c_sock):
        for client in self.clients:
            socket, (ip, port) = client
            try:
                if self.re_message == 'start':
                    self.re_message = ','.join(self.quizlist) + 'quiz'
                socket.sendall(self.re_message.encode())

            except: # 클라가 꺼질 경우.
                idx = self.clients.index(client)
                self.clients.remove(client)
                for client in self.clients:
                    sock, (ip, port) = client
                    sock.send((str(idx) + 'fin').encode())
                del self.clients_names[idx]
                del self.clients_colors[idx]
                print("{0}: {1} 연결 종료.".format(ip, port))

if __name__ == "__main__":
    Quizserver()