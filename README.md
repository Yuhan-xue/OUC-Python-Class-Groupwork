# 2021秋python周一三上机班ARGO数据小组源程序说明界面

这是中国海洋大学本科Python初学者的课程项目  
感谢中国海洋大学基础课：**[008501101119]Python程序设计**  
感谢王璐老师

## 功能说明

### 1、数据下载

内部编写了来自中国Argo实时资料中心网站的FTP下载模块

### 2、数据处理

可以处理大气科学应用广泛的netCDF4(.nc)格式文件

### 3、数据可视化

能够可视化数据生成**PNG**，**GIF**格式的可视化结果

## 源代码运行说明

### PYTHON环境版本(ANACONDA)

3.9.7

### 程序module依赖

PYTHON**内置库**

+ os  
+ shutil
+ tkinter
+ ftplib

PYTHON**第三方库**

+ cartopy(只推荐conda安装方式)
+ matplotlib
+ numpy
+ netCDF4

### 需要的其他操作

+ 以下文件夹需要与源程序在同一目录下  
  + self_data <存放用户自定义的NC文件>
  + data <存放FTP模块下载的NC文件>
  + demo_data <存放用于演示的NC文件>
  + lib <存放GUI图标文件>
  + pic <存放可视化后的JPG文件>
  + gif <存放可视化后的JPG文件>

小小的吐槽一下，这个小组作业是我一个人写的😅  
