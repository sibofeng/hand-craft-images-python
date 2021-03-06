'''
for python 3.6
'''
# -*- coding: utf-8 -*-
# tkinter
from tkinter import *
from PIL import Image, ImageTk
import os
import shutil


class Window(Frame):
    def __init__(self, master, screen_width, screen_height, file_path='message.txt', image_scale=0.2):
        Frame.__init__(self, master)
        self.master = master
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image_scale = image_scale
        self.file_name = file_path
        self.dict = {}
        self.image_infor = []
        self.line_index = 0  # 行引索 表示现在处理的是多少行
        self.line_nums = 0  # 一共有多少行
        self.widgetA = []
        self.widgetB = []
        self.widget_text = []
        self.init_window()

    def init_window(self):
        self.master.title("处理图片")

        self.pack(fill=BOTH, expand=1)

        # 实例化一个Menu对象，这个在主窗体添加一个菜单
        self.menu = Menu(self.master)
        self.master.config(menu=self.menu)

        # 创建File菜单，下面有Save和Exit两个子菜单
        file = Menu(self.menu)
        file.add_command(label='save log', command=self.save_logfile)
        file.add_command(label='Exit', command=self.client_exit)

        self.menu.add_cascade(label='File', menu=file)
        self.master.bind('<Key>', self.listen_kerboard)
        self.readLog()

    def client_exit(self):
        self.save_logfile()
        sys.exit()

    def save_logfile(self):
        if os.path.exists(self.file_name):
            os.remove(self.file_name)
            with open(self.file_name, 'w') as file:
                for i in range(self.line_index, self.line_nums):
                    file.writelines(self.lines[i])

    # 读取日志文件 并且执行程序 程序入口程function
    def readLog(self):
        if os.path.exists(self.file_name) and os.path.getsize(self.file_name) != 0:
            with open(self.file_name, 'r') as file:
                self.lines = file.readlines()
                self.line_nums = self.lines.__len__()
            self.addButton()
            self.showFolder(self.lines[self.line_index])
        else:
            self.show_text('日志文件不存在或者为空！')

    def showFolder(self, line):
        values = line.split(';')
        # type folderA folderB score
        for value in values:
            key, value = value.split('|')
            self.dict[key] = value
        self.folderA_list = self.getImageList(os.path.normpath(self.dict['folderA']))
        self.folderB_list = self.getImageList(os.path.normpath(self.dict['folderB']))
        if not self.folderA_list.__len__() == 0:
            sample_img = Image.open(self.folderA_list[0])
            img_width, img_height = sample_img.size
        elif not self.folderB_list.__len__() == 0:
            sample_img = Image.open(self.folderB_list[0])
            img_width, img_height = sample_img.size
        else:
            self.auto_next_page()

        new_img_size = (int(img_width * self.image_scale), int(img_height * self.image_scale))
        # print new_img_size
        img_row_num = int(self.screen_width / 2. / new_img_size[0])
        img_col_num = int(self.screen_height / new_img_size[1])
        self.image_group(self.folderA_list, self.widgetA, start_x=0, start_y=0,
                         img_row_num=img_row_num, img_col_num=img_col_num, new_img_size=new_img_size)
        self.image_group(self.folderB_list, self.widgetB, start_x=int(self.screen_width / 2), start_y=0,
                         img_row_num=img_row_num, img_col_num=img_col_num, new_img_size=new_img_size)

    # 显示图片组
    def image_group(self, image_list, widget, start_x=0, start_y=0, img_row_num=5, img_col_num=3,
                    new_img_size=(48, 64)):
        x = start_x
        y = start_y
        w = new_img_size[0]
        h = new_img_size[1]
        img_list = image_list
        screen_show_num = img_row_num * img_col_num
        list_len = img_list.__len__()
        if list_len > screen_show_num:
            list_len = screen_show_num
        if list_len != 0:
            for i, img in zip(range(list_len), img_list):
                if os.path.isfile(img):
                    widget.append(self.show_image(img, x=x, y=y))
                else:
                    self.show_text('没有该图片', x, y)
                # print x, y, w, h
                infor_tuple = (img, x, y, w, h)
                self.image_infor.append(infor_tuple)
                # 更改每个图片的位置
                x += w
                if (i + 1) % img_row_num == 0:
                    y += h
                    x = start_x
                    # self.master.bind("<Button-1>", self.click_master) #绑定全局点击事件, 判断是否点击到该图片
        else:
            self.auto_next_page()

    def addButton(self):
        combineBtn = Button(self.master, text='合并(快捷键c或者1)')
        combineBtn.pack()
        nextPageBtn = Button(self.master, text='下一条(快捷键n或者3)')
        nextPageBtn.pack()
        # combineBtn.bind("<ButtonRelease-1>", self.folder_combine)
        combineBtn.bind("<Key>", self.folder_combine)
        nextPageBtn.bind("<ButtonRelease-1>", self.next_page)
        # self.master.config(button)

    # 合并两个文件夹里面的文件
    def folder_combine(self, events):
        for path in self.folderA_list:
            end = path.split(os.path.normpath(self.dict['folderA']))[-1]
            new_path = os.path.normpath(self.dict['folderB'] + end)
            shutil.copy(path, new_path)
            os.remove(path)
            self.do_same_with_RGB(path, new_path)
        self.clean_all_widge()
        self.next_page(events)

    def listen_kerboard(self, events):
        keyboard_char = events.char
        print(keyboard_char)
        if keyboard_char == 'c' or keyboard_char == '0':
            self.folder_combine(events)
        elif keyboard_char == 'u' or keyboard_char == '1':
            self.up_page(events)
        elif keyboard_char == 'n' or keyboard_char == '3':
            self.next_page(events)
        elif keyboard_char == 's' or keyboard_char == '4':
            self.save_logfile()
        elif keyboard_char == 'q' or keyboard_char == '7':
            self.client_exit()

    def do_same_with_RGB(self, path, new_path):
        path.replace('yuv', 'rgb')
        new_path.replace('yuv', 'rgb')
        if os.path.isdir(path) and os.path.isdir(new_path):
            shutil.copy(path, new_path)
            os.remove(path)

    def up_page(self, events):
        self.clean_all_widge()
        self.line_index -= 1
        if self.line_index > 0:
            self.showFolder(self.lines[self.line_index])
        else:
            self.showFolder("没有再上上一项了")

    def next_page(self, events):
        self.clean_all_widge()
        self.line_index += 1
        if self.line_index <= self.line_nums:
            self.showFolder(self.lines[self.line_index])
        else:
            self.show_text('没有下一项了，日志文件已经处理完！')
            # pass

    def auto_next_page(self):
        self.clean_all_widge()
        self.line_index += 1
        if self.line_index < self.line_nums:
            self.showFolder(self.lines[self.line_index])
        else:
            self.show_text('没有下一项了，日志文件已经处理完！')

    # 删除所有显示图像的组件
    def clean_all_widge(self):
        for i in self.widgetA:
            i.destroy()
        for i in self.widgetB:
            i.destroy()
        for i in self.widget_text:
            i.destroy()
        del self.widgetA
        del self.widgetB
        del self.widget_text
        self.widgetA = []
        self.widgetB = []
        self.widget_text = []

    # 显示单张图片
    def show_image(self, path, x=0, y=0):
        load = Image.open(path)
        m, n = load.size
        new_size = (int(m * self.image_scale), int(n * self.image_scale))
        load = load.resize(new_size)
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        # img.bind("<Button-1>", self.click_image)
        img.image = render
        img.place(x=x, y=y)
        return img

    # 点击删除图片
    def click_master(self, events):
        print(events.x, events.y)
        for inf in self.image_infor:
            if self.check_point(events.x, events.y, inf[1], inf[2], inf[3], inf[4]):
                events.widget.destroy()
                image_path = inf[0]
                print(inf)
                # os.remove(image_path)
                break

    # 检测点击事件是否在box里面
    def check_point(self, eventx, eventy, x, y, w, h):
        if x <= eventx and eventx <= x + w and y <= eventy and eventy <= y + h:
            return True
        else:
            return False

    def show_text(self, t, x=0, y=0):
        for i in self.widget_text:
            i.destroy()
        del self.widget_text
        self.widget_text = []
        text = Label(self, text=t)
        text.place(x=x, y=y)
        text.pack()
        self.widget_text.append(text)

    def getImageList(self, path):
        img_list = []
        if os.path.isdir(path):
            parents = os.listdir(path)
            for parent in parents:
                child = os.path.join(path, parent)
                if os.path.isdir(child):
                    self.getImageList(child)
                elif child.endswith('.jpg') or child.endswith('.JPG'):
                    img_list.append(child)
        else:
            self.show_text('找不到指定路径:' + path)
        return img_list


'''
从AppSettings.config读取配置文件
image_scale 显示图片放缩尺寸
log_path 待处理日志的路径
'''

with open('AppSettings.config', encoding='gb18030') as config:
    lines = config.readlines()
    settings = {}
    for line in lines:
        key, value = line.split('=')
        settings[key] = value

root = Tk()
root.title(settings['app_name'])
screenWidth, screenHeight = root.maxsize()  # 获取显示器分辨率
geometryParam = '%dx%d+%d+%d' % (screenWidth, (screenHeight - 100), 0, 0)  # 默认全屏显示
root.geometry(geometryParam)

app = Window(root, screenWidth, screenHeight, file_path=settings['log_path'],
             image_scale=float(settings['image_scale']))
root.mainloop()
