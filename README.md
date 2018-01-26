```

app author: FENG Si-Bo  sibofeng@mail.bnu.edu.cn

app version: handcraft-image-python-v-1.0

develop date: 2018/1/25

coding language: python-3.6

relevant package: PyQt-5.0

```

### 软件说明：
该版本软件分为两个 one-column的是处理一个文件夹的 two-column的是处理两个文件夹的 两个功能类似 操作相似

点击图片：删除该图片
合并（限two-column）：文件夹左向右合并
保存：保存未处理的日志
 
### 使用方法：

打开软件
S1：选择日志文件（写法见下），选择后程序自动解析，判断文件写的是否正确
S2：软件的上一排是设置UI界面的参数 可以更改 输入非数字之外的字符无效
放缩系数不要太大：超出界面显示大小 软件会崩溃 每个区域显示数量没有要求看文件夹所有图片 可以设置小点 软件显示图片速度会提升
要显示文件夹所有图片 设置一个超级大的数
中间是显示文件夹图片的界面 尽量不要点击空白处（此处有bug，暂未解决）
下面是操作按钮 绑定有快捷键 按相应的字符或数字即可
软件所有删除文件全部保存在软件同级目录cache下面 如有误删手动找回（暂未有撤销功能）
S3：退出软件点击退出键 以保存日志（程序设定每15次操作自动保存日志）

### 日志写法
四个字段 errortype：一个文件夹写400 两个文件夹写500 folderA folderB：用绝对路径 score：暂时没用
处理一个文件夹:
errortype|400;folderA|G:/hwFaceRec/Debug/IR_FACE_PHOTOS_DST/yuv/id_length_4/1005_8116015120010324;folderB|;score|995

处理两个文件夹：
errortype|500;folderA|G:/hwFaceRec/Debug/IR_FACE_PHOTOS_DST/yuv/id_length_4/1005_8116015120010324;folderB|G:/hwFaceRec/Debug/des_image/yuv/id_length_4/004781_8116015120009945;score|995

可以把一个文件夹写成两个文件夹日志形式 同时处理两个文件夹