# tkinter
from tkinter import *
from PIL import Image, ImageTk
import os

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("处理图片")

        self.pack(fill=BOTH, expand=1)

        # 实例化一个Menu对象，这个在主窗体添加一个菜单
        self.menu = Menu(self.master)
        self.master.config(menu=self.menu)

        # 创建File菜单，下面有Save和Exit两个子菜单
        file = Menu(self.menu)
        file.add_command(label='Open', command=self.readLog)
        # file.add_command(label='show image', command=self.showImg)
        file.add_command(label='Exit', command=self.client_exit)
        self.menu.add_cascade(label='File', menu=file)

        # # 创建Edit菜单，下面有一个Undo菜单
        # edit = Menu(self.menu)
        # edit.add_command(label='Undo')
        # # edit.add_command(label='Show  Image', command=self.showImg)
        # edit.add_command(label='Show  Text', command=self.showTxt)
        # self.menu.add_cascade(label='Edit', menu=edit)

        # combinBtn = Button(self.master, text='合并').pack()

    def client_exit(self):
        exit()

    def readLog(self):
        file_name = 'message.txt'
        if os.path.exists(file_name) and os.path.getsize(file_name) != 0:
            with open(file_name, 'r') as file:
                self.lines = file.readlines()
            self.addButton()
            self.showFolder(self.lines[0])
        else:
            self.showTxt('日志文件不存在或者为空！')

    def showFolder(self, line):
        values = line.split(';')
        # type folderA folderB score
        self.dict = {}
        for value in values:
            key, value = value.split('|')
            self.dict[key] = value


    def getImageList(self, path):
        parents = os.listdir(path)
        for parent in parents:
            child = os.path.join(path, parent)
            if os.path.isdir(child):
                self.getImageList(child)
            else:
                print(child)

    def addButton(self):
        self.combineBtn = Button(self.master, text='合并').pack()
        self.nextPage = Button(self.master, text='下一条').pack()
        # self.master.config(button)

    def showImg(self):
        load = Image.open('7.png')
        render = ImageTk.PhotoImage(load)

        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)

    def showTxt(self, t):
        text = Label(self, text=t)
        text.pack()

root = Tk()
root.geometry("400x300")
app = Window(root)
root.mainloop()