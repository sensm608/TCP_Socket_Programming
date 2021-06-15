from socket import *
import tkinter as tk
from functools import partial
from tkinter.scrolledtext import ScrolledText
from threading import *

class Quizclient:
    client_socket = None
    image_color = ['blue.png','brown.png','green.png','pink.png','red.png','yellow.png']
    players = 0
    another_color = list()
    another_name = list()
    player_name = ''
    color_idx = 0
    quiz_list = list()
    chg_idx = 100

    def __init__(self, ip, port, idx, name):
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect((ip, port))
        self.player_name = name
        self.color_idx = idx
        self.set_gui()

    def set_gui(self):
        self.w = tk.Tk()
        self.w.title('시작')
        self.w.geometry('1500x800-200+100')
        self.w.resizable(width=False, height=False)
        self.w.bind('<Return>', self.enter_pressed)

        self.lFrame = tk.Frame(self.w, borderwidth=1, relief='solid', width=400)  # 왼쪽
        self.lFrame.pack(fill='both', expand=True, side='left')
        self.mFrame = tk.Frame(self.w, borderwidth=1, relief='solid', width=700)  # 가운데
        self.mFrame.pack(fill='both', expand=True, side='left')
        self.rFrame = tk.Frame(self.w, borderwidth=1, relief='solid', width=400)  # 오른쪽
        self.rFrame.pack(fill='both', expand=True, side='right')
        self.border_Frame = tk.Frame(self.mFrame, borderwidth=2, relief='solid', bg='white', width=600, height=400) #보드
        self.border_Frame.place(x=50, y=50)

        self.default_lbl = list()
        self.players_lbl = list()
        self.image_default = tk.PhotoImage(file='images/default.png', width=200, height=130)
        self.color_image = list()
        for i in range(0, 6):
            self.color_image.append(tk.PhotoImage(file='images/'+self.image_color[i], width=200, height=130))
        for i in range(0, 2):
            for j in range(0, 3):
                if i == 0:
                    self.default_lbl.append(tk.Label(self.lFrame, image=self.image_default, borderwidth=2, relief='solid'))
                    self.default_lbl[j].place(x=100, y=50 + (250 * j))
                    self.players_lbl.append(tk.Label(self.lFrame, text='', width=22, font=('',13)))
                    self.players_lbl[j].place(x=100, y=200 + (250 * j))
                else:
                    self.default_lbl.append(tk.Label(self.rFrame, image=self.image_default, borderwidth=2, relief='solid'))
                    self.default_lbl[j + 3].place(x=100, y=50 + (250 * j))
                    self.players_lbl.append(tk.Label(self.rFrame, text='', width=22, font=('', 13)))
                    self.players_lbl[j + 3].place(x=100, y=200 + (250 * j))

        self.quiz_lbl = list()
        for i in range(0, 10):
            self.quiz_lbl.append(tk.Label(self.mFrame, bg='white',text='', font=('',14)))
            if i < 3:  # 0,1,2
                self.quiz_lbl[i].place(x=150 * (i + 1) - 30, y=100)
            elif i < 7:  # 3,4,5,6
                self.quiz_lbl[i].place(x=120 * (i - 2) - 30, y=200)
            else:  # 7,8,9
                self.quiz_lbl[i].place(x=150 * (i - 6) - 30, y=300)

        self.start_btn = tk.Button(self.mFrame, text='게임 시작', command=self.start_game, width=10, height=3)
        self.start_btn.place(x=300, y=0)

        self.chat_area = ScrolledText(self.mFrame, width=74, height=10, borderwidth=2, relief='solid', font=('', 13), state='disabled')
        self.chat_area.place(x=50, y=520)
        self.chat_entry = tk.Entry(self.mFrame, width=74, borderwidth=2, relief='solid', font=('', 13))
        self.chat_entry.place(x=50, y=690)

        t = Thread(target=self.receive, args=(self.client_socket,))
        t.start()

    def start_game(self):
        if len(self.quiz_list) > 0:
            return
        self.client_socket.send('start'.encode())

    def receive(self, sock):
        self.client_socket.send(self.image_color[self.color_idx].encode())
        self.client_socket.send(self.player_name.encode())
        while True:
            messages = sock.recv(256)
            if not messages:
                break
            messages = messages.decode()
            if '\n' in messages:
                templist = messages.split('\n')
                self.quiz_list[int(templist[1])] = templist[2]  # 맞춘 문제 교체
                messages = templist[0]
                self.quiz_refresh()
            if ':' in messages: # 일반 채팅
                self.send_messages(messages)
            elif 'color' in messages: # 색
                self.another_color = messages[:-5].split(',')
            elif 'name' in messages: # 이름
                self.another_name = messages[:-4].split(',')
                self.players = len(self.another_name)
                self.send_messages(self.another_name[-1] + "님이 입장하셨습니다.")
            elif 'fin' in messages:
                xnum = int(messages[:-3])
                self.players = self.players - 1
                try:
                    self.send_messages(self.another_name[xnum] + "님이 퇴장하셨습니다.")
                    self.default_lbl[self.players].configure(image=self.image_default)
                    self.players_lbl[self.players].configure(text='')
                    del self.another_color[xnum]
                    del self.another_name[xnum]
                except:
                    pass
            elif 'quiz' in messages:
                self.quiz_list = messages[:-4].split(',')
                self.send_messages('게임 시작!')
                self.quiz_refresh()
            self.player_refresh()
        sock.close()

    def send_messages(self, message):
        self.chat_area.configure(state='normal')
        self.chat_area.insert('end',message+'\n')
        self.chat_entry.delete(0,'end')
        self.chat_area.configure(state='disabled')
        self.chat_area.see('end')

    def player_refresh(self):
        if self.players != len(self.another_name):
            return
        for i in range(0, 6):
            if i < self.players:
                cimage = self.color_image[self.image_color.index(self.another_color[i])]
                self.default_lbl[i].configure(image=cimage)
                self.players_lbl[i].configure(text=self.another_name[i])

    def quiz_refresh(self):
        for i in range(0,10):
            self.quiz_lbl[i].configure(text=self.quiz_list[i])

    def enter_pressed(self, e):
        message = self.player_name + ':' + self.chat_entry.get()
        for i in range(0,10):
            if len(self.quiz_list) < 1:
                break
            if message[message.index(':') + 1:] in self.quiz_list[i]: #정답 맞출 경우
                message = message + '\n' + str(i) #일반 채팅이랑 맞춘 레이블 번호 반환.
        self.client_socket.sendall(message.encode())

image_color = ['blue.png', 'brown.png', 'green.png', 'pink.png', 'red.png', 'yellow.png']

def start_gui():
    selw = tk.Tk()
    selw.geometry('938x400-200+100')
    selw.resizable(width=False, height=False)
    title_lbl = tk.Label(selw, text='어려운 글자 치기', font=('',30))
    title_lbl.grid(row=0, column=0, columnspan=6)
    name_lbl = tk.Label(selw, text='사용할 닉네임을 설정해주세요:',font=('',15))
    name_lbl.place(x=180, y=300)
    name_entry = tk.Entry(selw ,font=('',15))
    name_entry.place(x=477, y=300)
    btn_list = list()
    image_list = list()
    for i in range(0, 6):
        image_list.append(tk.PhotoImage(file='images/' + image_color[i], width=150, height=150))
        btn_list.append(tk.Button(selw, image=image_list[i], command=partial(ready_start, [i, name_entry, selw])))
        btn_list[i].grid(row=2, column=i)
    explain_lbl = tk.Label(selw, text='원하는 닉네임을 입력하시고 사용할 색깔 버튼을 눌러주세요.')
    explain_lbl.grid(row=1, column=0, columnspan=6)
    tk.mainloop()

def ready_start(inform):
    name = inform[1].get().strip().replace(':','')
    if name == '':
        name = 'player'
    inform[2].destroy()
    Quizclient(ip, port, inform[0], name)
    tk.mainloop()

if __name__ == "__main__":
    ip = input("server IP addr: ")
    if ip == '':
        ip = '127.0.0.1'
    port = 2505
    start_gui()