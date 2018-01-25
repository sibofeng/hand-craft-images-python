# -*- coding:utf-8 -*-

__author__ = 'FENG Si-Bo'

import sys, os, shutil
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QGroupBox, QPushButton, QLabel, \
    QHBoxLayout, QVBoxLayout, QGridLayout, QLineEdit, QTextEdit, QScrollArea, \
    QMessageBox, QFileDialog, QSlider


class GUI(QWidget):
    class myLabel(QLabel):
        def __init__(self, index, folder, path, parent=None):
            self.index = index
            self.folder = folder
            self.path = path
            self.cache_path = 'cache'
            if not os.path.exists(self.cache_path):
                os.mkdir(self.cache_path)
            super(GUI.myLabel, self).__init__(parent)

        def mousePressEvent(self, e):  ##重载一下鼠标点击事件
            # print(self.path)
            if os.path.isfile(self.path):
                shutil.move(self.path, self.cache_path)

    def __init__(self):
        super(GUI, self).__init__()

        self.name = "HW craft image"

        # self.file_name = 'G:/hwFaceRec/handcraftImage/logphp/message.txt'
        file_name = QFileDialog.getOpenFileName(self, "选取待处理日志文件", "G:\hwFaceRec\Debug\logphp",
                                                "Txt files(*.txt)")
        self.file_name = file_name[0]
        self.line_index = 0
        self.dict = {}
        self.left_label_class = []
        self.right_label_class = []
        self.click_x = 0
        self.click_y = 0

        # 在同级目录下创建暂存的文件夹
        self.cache_path = 'cache'
        if not os.path.exists(self.cache_path):
            os.mkdir(self.cache_path)

        # 撤销操作的相关 暂时不会
        self.operate_info = []
        self.operate_index = 0

        self.readLog()

        self.initUi()
        self.setWindowTitle(self.name)

    def initUi(self):
        # 获取显示器的宽高
        desktop = QtWidgets.QApplication.desktop()
        self.desktop_width = desktop.width()
        self.desktop_height = desktop.height()
        self.setGeometry(10, 30, self.desktop_width - 20, self.desktop_height - 80)

        # 创建窗口
        self.createBoxes()

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.top_box)

        hboxLayout = QHBoxLayout()
        # hboxLayout.addStretch()

        self.scroll_left = QScrollArea()
        self.scroll_left.setWidget(self.left_grid_box)
        self.scroll_left.setAutoFillBackground(True)
        self.scroll_left.setWidgetResizable(True)

        # self.scroll_right = QScrollArea()
        # self.scroll_right.setWidget(self.right_grid_box)
        # self.scroll_right.setAutoFillBackground(True)
        # self.scroll_right.setWidgetResizable(True)

        hboxLayout.addWidget(self.scroll_left)
        # hboxLayout.addWidget(self.scroll_right)
        mainLayout.addLayout(hboxLayout)
        mainLayout.addWidget(self.bottom_box)
        self.setLayout(mainLayout)

    def mouseReleaseEvent(self, e):
        self.freshen('folderA', self.left_grid_box, self.left_layout, self.left_label_class)
        # self.freshen('folderB', self.right_grid_box, self.right_layout, self.right_label_class)

    def keyPressEvent(self, e):
        print(e)

    # 读取日志文件 并且执行程序 程序入口程function
    def readLog(self):
        if os.path.exists(self.file_name) and os.path.getsize(self.file_name) != 0:
            with open(self.file_name, 'r') as file:
                self.lines = file.readlines()
                self.line_nums = self.lines.__len__()
        else:
            self.show_info("Warning", "没有找到日志文件！请检查文件或文件路径")

    # 创建左右两个layout
    def createBoxes(self):
        self.dict_line()
        self.creatTopBox()
        self.createLeftBox()
        # self.createRightBox()
        self.createBottomBox()
        self.create_image()

    # 创建顶部的layout
    def creatTopBox(self):
        self.top_box = QGroupBox("参数设置")

        self.scale_label = QLabel(self)
        self.scale_label.setText("图片放缩")
        self.scale_edit = QLineEdit()
        self.scale_edit.setText("0.25")
        self.scale_edit.textChanged.connect(self.create_image)

        self.nums_label = QLabel(self)
        self.nums_label.setText("每个区域显示的图片数")
        self.nums_edit = QLineEdit()
        self.nums_edit.setText("15")
        self.nums_edit.textChanged.connect(self.create_image)

        slider = QSlider(Qt.Horizontal, self)

        # self.button = QPushButton("执行")
        # self.button.clicked.connect(self.create_image)
        layout = QHBoxLayout()
        layout.addWidget(self.scale_label)
        layout.addWidget(self.scale_edit)
        layout.addWidget(self.nums_label)
        layout.addWidget(self.nums_edit)
        layout.addWidget(slider)
        # layout.addWidget(self.button)

        self.top_box.setLayout(layout)

    # 创建左边的GUI界面
    def createLeftBox(self):
        self.left_grid_box = QGroupBox(self.dict['folderA'])
        self.left_layout = QGridLayout()
        self.left_grid_box.setLayout(self.left_layout)

    # def createRightBox(self):
    #     self.right_grid_box = QGroupBox(self.dict['folderB'])
    #     self.right_layout = QGridLayout()
    #     self.right_grid_box.setLayout(self.right_layout)


    # 根据传来的参数更改显示ui大小
    def create_image(self):
        scale = self.scale_edit.text()
        nums = self.nums_edit.text()

        if (scale.isdigit() or self.is_float(scale)) and not scale == '0' and nums.isdigit():
            self.image_scale = float(self.scale_edit.text())
            self.area_image_nums = int(self.nums_edit.text())

            for item in self.left_label_class:
                item.clear()
            # for item in self.right_label_class:
            #     item.clear()

            self.show_images('folderA', self.left_grid_box, self.left_layout, self.left_label_class)
            # self.show_images('folderB', self.right_grid_box, self.right_layout, self.right_label_class)
        else:
            print("不是数字")

    # 判断字符串是否为小数
    def is_float(self, s):
        s = str(s)
        if s.count('.') == 1:
            s_left = s.split('.')[0]
            s_right = s.split('.')[1]
            if s_left.isdigit() and s_right.isdigit():
                return True
            elif s_left.startswith('-') and s_left.count('-') == 1 and s_right.isdigit():
                if s_left.split('-')[1].isdigit():
                    return True
        return False

    # 在左右两个group box中显示图片, type='up' or 'down'
    def show_images(self, folder, box, layout, widge_class, type=None):
        box.setTitle(self.dict[folder])
        img_list = self.getImageList(self.dict[folder])
        print(img_list)
        if img_list.__len__() == 0:
            if type == 'up':
                self.auto_up_page()
            else:
                self.auto_next_page()

        show_num = self.area_image_nums
        if img_list.__len__() < self.area_image_nums or self.area_image_nums == -1:
            show_num = img_list.__len__()

        row_index = 0
        col_index = 0
        for i in range(show_num):
            # imgLabel = QLabel()
            imgLabel = GUI.myLabel(i, folder, img_list[i])
            pixMap = QPixmap(img_list[i])
            image_size = pixMap.size()
            # print(image_size.width(), image_size.height())
            new_width = int(image_size.width() * float(self.image_scale))
            new_height = int(image_size.height() * float(self.image_scale))

            self.spacing = 5  # 图片之间的间隔
            num_per_row = int(self.desktop_width / (new_width + self.spacing))

            pixMap = pixMap.scaled(new_width, new_height)
            imgLabel.setPixmap(pixMap)

            layout.setSpacing(self.spacing)
            widge_class.append(imgLabel)

            # 控件名，行，列，占用行数，占用列数，对齐方式
            layout.addWidget(imgLabel, row_index, col_index, 1, 1, alignment=Qt.AlignTop)
            layout.setColumnStretch(2, 10)
            col_index += 1
            if col_index % num_per_row == 0:
                row_index += 1
                col_index = 0

    # 创建底部的按钮box
    def createBottomBox(self):
        self.bottom_box = QGroupBox()

        bottom_layout = QHBoxLayout()

        self.del_left_btn = QPushButton("删除左文件夹")
        self.del_left_btn.clicked.connect(self.del_left_folder)
        # self.del_right_btn = QPushButton("删除右文件夹")
        # self.del_right_btn.clicked.connect(self.del_right_folder)
        self.up_page_btn = QPushButton("上一页")
        self.up_page_btn.clicked.connect(self.auto_up_page)
        self.next_page_btn = QPushButton("下一页")
        self.next_page_btn.clicked.connect(self.auto_next_page)
        self.combine_btn = QPushButton("合并")
        self.combine_btn.clicked.connect(self.folder_combine)
        self.save_btn = QPushButton("保存已处理日志")
        self.save_btn.clicked.connect(self.save_logfile)
        self.quit_btn = QPushButton("保存并退出")
        self.quit_btn.clicked.connect(self.quit_exe)

        bottom_layout.addWidget(self.del_left_btn)
        # bottom_layout.addWidget(self.del_right_btn)
        bottom_layout.addWidget(self.up_page_btn)
        bottom_layout.addWidget(self.next_page_btn)
        bottom_layout.addWidget(self.combine_btn)
        bottom_layout.addWidget(self.save_btn)
        bottom_layout.addWidget(self.quit_btn)

        self.bottom_box.setLayout(bottom_layout)

    # 退出软件且保存日志
    def quit_exe(self):
        self.save_logfile()
        sys.exit()

    # 保存日志文件（从当前处理的条目开始保存，处理过的删除掉）
    def save_logfile(self):
        if os.path.exists(self.file_name):
            os.remove(self.file_name)
            with open(self.file_name, 'w') as file:
                for i in range(self.line_index, self.line_nums):
                    file.writelines(self.lines[i])

    # 删除左边整个文件夹
    def del_left_folder(self):
        if os.path.exists(self.dict['folderA']):
            shutil.move(self.dict['folderA'], self.cache_path)
        self.auto_next_page()

    # def del_right_folder(self):
    #     if os.path.exists(self.dict['folderB']):
    #         shutil.move(self.dict['folderB'], self.cache_path)
    #     self.auto_next_page()

    # 合并两个文件夹里面的文件
    def folder_combine(self):
        if os.path.exists(self.dict['folderA']) and os.path.exists(self.dict['folderB']):
            shutil.move(self.dict['folderA'], self.dict['folderB'])
        self.do_same_with_RGB(self.dict['folderA'], self.dict['folderB'])
        self.auto_next_page()

    # 在RGB文件夹中做同样的事情
    def RGB_combine(self, src, dst):
        src.replace('yuv', 'rgb')
        dst.replace('yuv', 'rgb')
        if os.path.exists(src) and os.path.exists(dst):
            shutil.move(src, dst)

    # 重新排列文件夹中的图片
    def freshen(self, folder, box, layout, label_class):
        for item in label_class:
            item.clear()
        self.show_images(folder, box, layout, label_class)

    # 向上翻页
    def auto_up_page(self):
        self.clean_all_widge()
        self.line_index -= 1
        if self.line_index >= 0:
            self.dict_line()
            self.show_images('folderA', self.left_grid_box, self.left_layout, self.left_label_class, type='up')
            # self.show_images('folderB', self.right_grid_box, self.right_layout, self.right_label_class, type='up')
        else:
            # 显示提示
            self.show_info("Warning", "没有更多的上一页了！")

    # 向下翻页
    def auto_next_page(self):
        self.clean_all_widge()
        self.line_index += 1
        if self.line_index < self.line_nums:
            self.dict_line()
            self.show_images('folderA', self.left_grid_box, self.left_layout, self.left_label_class)
            # self.show_images('folderB', self.right_grid_box, self.right_layout, self.right_label_class)
        else:
            # 显示日志文件已经读取完
            self.show_info("Warning", "没有更多的下一页了！")

    # 清除所有组件 清除list 清除dict
    def clean_all_widge(self):
        for item in self.left_label_class:
            item.clear()
        for item in self.right_label_class:
            item.clear()

        self.dict.clear()

    # 解析日志
    def dict_line(self):
        values = self.lines[self.line_index].split(';')
        # type; folderA; folderB; score
        for value in values:
            key, value = value.split('|')
            if key == "errortype" or key == "folderA" or key == "folderB" or key == "score":
                self.dict[key] = value
            else:
                self.show_info("Warning", "日志文件Key有错误！")

    # 获取文件夹中的文件列表（有递归）
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
            pass
        return img_list

    # 显示信息提示框
    def show_info(self, title, message):
        QMessageBox.information(self, title, self.tr(message))
        self.quit_exe()


# if __name__ == '__main__':
app = QApplication(sys.argv)
ex = GUI()
ex.show()
sys.exit(app.exec_())
