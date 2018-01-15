```
app author: FENG SiBo  sibofeng@mail.bnu.edu.cn
app version: handcraft-image-python-v-0.0
develop date: 2018/1/15
coding language: python-2.7
relevant package: tkinter pillow PyQt-5.0
```

### 工具功能

点击图片：该图片会删除

点击合并按钮：左面文件夹图像向右文件夹合并

下一条：处理下一条内容


### 软件配置文件AppSettings.config写入要求

e.g.

app_name=处理图片
image_scale=0.25

#### 说明：

app_name:软件名字 这个不需要改

image_scale:图片放缩系数 软件显示图片大小是按照每个文件夹第一张图片大小为基本尺寸乘以放缩系数作为显示图片的大小
可以调节这个放缩系数改变软件显示图片大小


### 软件处理的日志文件message.txt写入要求

e.g.

type|500;folderA|G:/hwFaceRec/1400_8116016070005296;folderB|G:/hwFaceRec/004185_8116015120009892;score|969
type|500;folderA|G:/hwFaceRec/1400_9224564562155296;folderB|G:/hwFaceRec/004185_6316015120009892;score|954
...

#### 说明:

type:类型 这个版本随意填写
folderA：第一个要处理的文件夹路径 软件对应显示左面
folderB：第二个要处理的文件夹路径 软件对应显示右边
score：得分 这个版本随意填写


### ！！！！！！！使用注意！！！！！！！！！！！！！！

0. 工具包括四个个文件：主程序
    main.exe 主程序
    AppSettings.config 配置文件
    message.txt 日志文件
    README.md 此文件

1. message.txt文件里面的路径要是用**绝对路径**

2. 退出时要记得，**点击File菜单里面的Exit**，不要直接点×关闭，目的是将未处理的日志重新写入文件，删除处理过的日志
不要直接点×，点×除了增加了下次的工作量之外，对数据没什么影响。。。

