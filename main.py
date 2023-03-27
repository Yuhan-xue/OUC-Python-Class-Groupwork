import os
import shutil
import tkinter as tk
from ftplib import FTP

import cftime
import cartopy.crs as ccrs
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset


def getdata():
    global file_dir, file_list, window, var, forma
    '''
    说明：
    1、本模块数据来源：中国Argo实时资料中心网站（或自然资源部杭州全球海洋Argo系统野外科学观测研究站）
    2、版权所属：自然资源部第二海洋研究所中国Argo实时资料中心
    3、编写者对用户因使用此模块产生的损失和不良后果不负任何法律责任。
    4、本模块采用匿名登录ftp方式下载数据。
    5、已知bug：受制于主机和服务器的带宽有一定概率下载失败，如果没有显示 '下载完毕。' 则一致认定为下载失败。
    WRITE BY YuHanxue in 2021.12.1 in OUC
    联系邮箱：hanxueyu555@gmail.com
    '''
    window.destroy()
    window = tk.Tk()
    window.geometry("500x500")
    window.iconbitmap(r".\lib\ico\IDisk HD ALT.ico")
    window.title('FTP模块')
    tk.Label(window, text='已启动FTP下载模块', font=('Arial', 12)).place(x=0, y=0)
    ftpserver = 'data.argo.org.cn'
    ftpath = '/pub/ARGO/BOA_Argo/NetCDF'
    localpath = './data/'
    ftp = FTP()
    try:
        ftp.connect(ftpserver, 21)
        ftp.login()
        ftp.cwd(ftpath)
    except:
        raise IOError('FTP数据连接失败，请检查您的网络环境')
    else:
        tk.Label(window, text=f'{ftpserver}欢迎信息:{ftp.getwelcome()}', font=(
            'Arial', 12)).place(x=0, y=20)
        tk.Label(window, text='FTP连接成功', font=('Arial', 12)).place(x=0, y=40)
        tk.Label(window, text=f'成功进入FTP服务器：{ftp.pwd()}', font=(
            'Arial', 12)).place(x=0, y=60)
    file_list = list(ftp.nlst())
    for i in range(14):
        file_list.pop()
    file_sta = (file_list[0]).split('_')
    file_end = (file_list[-1]).split('_')
    tk.Label(window, text=f'NC文件记录时间从{file_sta[2]:4}年{file_sta[3][0:2]:2}月\
            到{file_end[2]:4}年{file_end[3][0:2]:2}月', font=('Arial', 12)).place(x=0, y=80)
    # 下载数据
    if not os.path.exists(localpath):
        os.makedirs(localpath)
    tk.Label(window, text='请问需要单个数据还是批量数据？',
             font=('Arial', 12)).place(x=0, y=100)
    print()

    def single():
        global file_dir, file_list, window, var, forma

        def get():
            global file_dir, file_list, window, var, forma
            year = e_year.get()
            mon = e_mon.get()
            filename = 'BOA_Argo_'+str(year)+'_'+str(mon).zfill(2)+'.nc'
            bufsize = 1024
            path = os.path.join(localpath, filename)
            with open(path, 'wb') as fid:
                tk.Label(window, text='正在下载：').grid(row=3, column=1)
                window.update()
                ftp.retrbinary('RETR {0}'.format(filename), fid.write, bufsize)
                tk.Label(window, text='下载完毕。').grid(row=4, column=1)
                tk.Button(window, text='进入可视化', command=printfil).grid(
                    row=5, column=1)
        window.destroy()
        window = tk.Tk()
        window.geometry("300x500")
        window.iconbitmap(r".\lib\ico\IDisk HD ALT.ico")
        window.title('ARGO数据单项下载')
        l_year = tk.Label(window, text='年：(2004-2021)')
        l_year.grid(row=0)
        e_year = tk.Entry(window)
        e_year.grid(row=0, column=1)
        l_mon = tk.Label(window, text='月：(1-12)')
        l_mon.grid(row=1)
        e_mon = tk.Entry(window)
        e_mon.grid(row=1, column=1)
        b_sure = tk.Button(window, text='确定', command=get)
        b_sure.grid(row=2, column=1)

    def batch():
        global file_dir, file_list, window, var, forma

        def get():
            global file_dir, file_list, window, var, forma
            tk.Label(window, text='正在下载，请不要退出').grid(row=6)
            window.update()
            year1 = e_year.get()
            mon1 = e_mon.get()
            year2 = e_year2.get()
            mon2 = e_mon2.get()
            file_down_start = 'BOA_Argo_' + \
                str(year1)+'_'+str(mon1).zfill(2)+'.nc'
            file_down_start_index = file_list.index(file_down_start)
            file_down_end = 'BOA_Argo_'+str(year2)+'_'+str(mon2).zfill(2)+'.nc'
            file_down_end_index = file_list.index(file_down_end)
            i = 7
            for filename in file_list[file_down_start_index:file_down_end_index+1]:
                bufsize = 1024
                path = os.path.join(localpath, filename)
                with open(path, 'wb') as fid:
                    tk.Label(window, text=f'正在下载：{filename}').grid(row=i)
                    window.update()
                    ftp.retrbinary('RETR {0}'.format(
                        filename), fid.write, bufsize)
                    tk.Label(window, text=f'{filename}文件下载结束').grid(row=i+1)
                    window.update()
                    i += 2
                if filename == file_list[file_down_end_index]:
                    window.destroy()
                    window = tk.Tk()
                    window.geometry("300x500")
                    window.iconbitmap(r".\lib\ico\IDisk HD ALT.ico")
                    window.title('ARGO数据结束下载')
                    tk.Button(window, text='进入可视化', command=printfil).pack()
        window.destroy()
        window = tk.Tk()
        window.geometry("300x500")
        window.iconbitmap(r".\lib\ico\IDisk HD ALT.ico")
        window.title('ARGO数据批量下载')
        l_year = tk.Label(window, text='起始年份：(2004-2021)')
        l_year.grid(row=0)
        e_year = tk.Entry(window)
        e_year.grid(row=0, column=1)
        l_mon = tk.Label(window, text='起始月份：(1-12)')
        l_mon.grid(row=1)
        e_mon = tk.Entry(window)
        e_mon.grid(row=1, column=1)
        l_year2 = tk.Label(window, text='起始年份：(2004-2021)')
        l_year2.grid(row=2)
        e_year2 = tk.Entry(window)
        e_year2.grid(row=2, column=1)
        l_mon2 = tk.Label(window, text='起始月份：(1-12)')
        l_mon2.grid(row=3)
        e_mon2 = tk.Entry(window)
        e_mon2.grid(row=3, column=1)
        b_sure = tk.Button(window, text='确定', command=get)
        b_sure.grid(row=4, column=1)

    b = tk.Button(window, text='单个数据', command=single, width=35)
    c = tk.Button(window, text='批量数据', command=batch, width=35)
    b.place(x=0, y=120)
    c.place(x=250, y=120)
    window.mainloop()


def ftp():
    global file_dir, file_list, window, var, forma
    file_dir = './data'
    if os.path.exists(file_dir):
        shutil.rmtree('./data')
        os.makedirs('./data')
    getdata()


def demo():
    global file_dir, file_list, window, var, forma
    file_dir = './demo_data'
    printfil()

def getnc(fl):
    a=[]
    for i in fl:
        if i[-2:]=='nc':
            a.append(i)
    return a

def selfdata():
    global file_dir, file_list, window, var, forma
    file_dir = './self_data'
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    window.destroy()
    window = tk.Tk()
    window.geometry("300x500")
    window.iconbitmap(r".\lib\ico\IDisk HD ALT.ico")
    window.title('自定义文件')
    tk.Label(window, text='请将文件放入self_data文件夹内', font=('Arial', 12)).pack()
    tk.Label(window, text='文件必须是BOA_Argo_yyyy_mm.nc格式，y指年份，m指月份',
             font=('Arial', 12)).pack()
    tk.Label(window, text='放置结束请按结束键', font=('Arial', 12)).pack()
    tk.Button(window, text='结束放置', command=printfil).pack()


def printfil():
    global file_dir, file_list, window, var, forma
    file_list = list(os.listdir(file_dir))
    for i in range(len(file_list)):
        file_list[i] = file_dir+'/'+file_list[i]
    file_list=getnc(file_list)
    window.destroy()
    window = tk.Tk()
    window.geometry("300x500")
    window.title('文件确认')
    window.iconbitmap(r".\lib\ico\IDisk HD ALT.ico")
    tk.Label(window, text='您将处理以下文件：', font=('Arial', 12)).pack()
    for i in file_list:
        tk.Label(window, text=i, font=('Arial', 12)).pack()
    tk.Button(window, text='进入可视化', command=choose).pack()


def choose():
    global file_dir, file_list, window, var, forma
    window.destroy()
    window = tk.Tk()
    window.title('请选择温度或盐度')
    window.geometry("300x500")
    window.iconbitmap(r".\lib\ico\IDisk HD ALT.ico")
    la1 = tk.Label(window, text='请选择可视化对象', font=('Arial', 12))
    la1.place(y=0)
    b = tk.Button(window, text='温度', command=temp, width=20)
    c = tk.Button(window, text='盐度', command=salt, width=20)
    b.place(x=0, y=20)
    c.place(x=150, y=20)


def salt():
    global file_dir, file_list, window, var, forma
    window.destroy()
    window = tk.Tk()
    window.title('已选择盐度')
    window.geometry("300x500")
    window.iconbitmap(r".\lib\ico\IDisk HD ALT.ico")
    var = 'salt'
    la1 = tk.Label(window, text='请选择可视化格式', font=('Arial', 12))
    la1.place(y=0)
    b = tk.Button(window, text='GIF 动图', command=forma_gif, width=20)
    c = tk.Button(window, text='JPG 图片', command=forma_jpg, width=20)
    b.place(x=0, y=20)
    c.place(x=150, y=20)


def temp():
    global file_dir, file_list, window, var, forma
    window.destroy()
    window = tk.Tk()
    window.title('已选择温度')
    window.geometry("300x500")
    window.iconbitmap(r".\lib\ico\IDisk HD ALT.ico")
    var = 'temp'
    la1 = tk.Label(window, text='请选择可视化格式', font=('Arial', 12))
    la1.place(y=0)
    b = tk.Button(window, text='GIF 动图', command=forma_gif, width=20)
    c = tk.Button(window, text='JPG 图片', command=forma_jpg, width=20)
    b.place(x=0, y=20)
    c.place(x=150, y=20)


def forma_gif():
    global file_dir, file_list, window, var, forma
    forma = gifmake
    window.destroy()
    window = tk.Tk()
    window.title('GIF制作')
    window.geometry("300x500")
    window.iconbitmap(r".\lib\ico\IDisk HD ALT.ico")
    for fil in file_list:
        file_name = var+'_of_'+fil.split('/')[-1]
        data = Dataset(fil)
        lon = data.variables['lon']
        lat = data.variables['lat']
        data1 = np.array(data.variables[var])
        data1[data1>2000.0]=np.nan
        data1[data1<-2000.0]=np.nan
        lat = slice(np.nanmin(lat), np.nanmax(lat)+lat[1]-lat[0], lat[1]-lat[0])
        lon = slice(np.nanmin(lon), np.nanmax(lon)+lon[1]-lon[0], lon[1]-lon[0])
        Lat, Lon = np.mgrid[lat, lon]
        tk.Label(
            window, text=f'正在可视化{file_name[:-3]}', font=('Arial', 12)).pack()
        window.update()
        forma(Lon, Lat, data1, file_name[:-3])
    end()


def forma_jpg():
    global file_dir, file_list, window, var, forma
    forma = picmake
    window.destroy()
    window = tk.Tk()
    window.title('JPG制作')
    window.geometry("300x500")
    window.iconbitmap(r".\lib\ico\IDisk HD ALT.ico")
    for fil in file_list:
        file_name = var+'_of_'+fil.split('/')[-1]
        data = Dataset(fil)
        lon = data.variables['lon']
        lat = data.variables['lat']
        data1 = np.array(data.variables[var])
        data1[data1>2000.0]=np.nan
        data1[data1<-2000.0]=np.nan
        lat = slice(np.min(lat), np.max(lat)+lat[1]-lat[0], lat[1]-lat[0])
        lon = slice(np.min(lon), np.max(lon)+lon[1]-lon[0], lon[1]-lon[0])
        Lat, Lon = np.mgrid[lat, lon]
        tk.Label(window, text=f'正在可视化{file_name}', font=('Arial', 12)).pack()
        window.update()
        forma(Lon, Lat, data1, file_name[:-3])
    end()


def picmake(Lon, Lat, data1, name):
    global file_dir, file_list, window, var, forma
    for i in range(np.shape(data1)[1]):
        plt.cla()
        plt.figure(figsize=(20, 10))
        ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=180))
        ax.coastlines()
        data_drew = data1[0, i, :, :]
        plt.contour(Lon, Lat, data_drew, np.linspace(np.nanmin(data1),np.nanmax(data1),10), alpha=0.75, linewidths=0.5,
                    colors='black', transform=ccrs.PlateCarree(central_longitude=0))
        c = plt.contourf(Lon, Lat, data_drew, np.linspace(np.nanmin(data1),np.nanmax(data1),40),
                         transform=ccrs.PlateCarree(central_longitude=0),cmap='RdBu_r')
        plt.colorbar(c,orientation="horizontal",extend='both',shrink=0.7)
        plt.title(f'depth={i}', fontsize='xx-large')
        name1 = './pic/'+name+f'_depth={i}.jpg'
        plt.savefig(name1, dpi=200)
        plt.close()


def gifmake(Lon, Lat, data1, name):
    global file_dir, file_list, window, var, forma
    name = './gif/'+name+'.gif'
    fig = plt.figure(figsize=(20, 10))

    def updatefig(num):
        plt.cla()
        ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=180))
        ax.coastlines()
        data_drew = data1[0, num, :, :]
        #print(np.linspace(np.nanmin(data1),np.nanmax(data1),10))
        c=ax.contourf(Lon, Lat, data_drew, np.linspace(np.nanmin(data1),np.nanmax(data1),40),
                    transform=ccrs.PlateCarree(central_longitude=0),cmap='RdBu_r')
        ax.contour(Lon, Lat, data_drew, np.linspace(np.nanmin(data1),np.nanmax(data1),10), 
                   linewidths=0.5, alpha=0.75,
                   colors='black', transform=ccrs.PlateCarree(central_longitude=0))
        plt.colorbar(c,orientation="horizontal",extend='both',shrink=0.7)
        plt.title(f'depth={num}', fontsize='xx-large')
        return ax
    ani = animation.FuncAnimation(
        fig, updatefig, frames=range(np.shape(data1)[1]))
    ani.save(name, fps=15)


def end():
    global file_dir, file_list, window, var, forma
    window.destroy()
    window = tk.Tk()
    window.title('结束')
    window.iconbitmap(r".\lib\ico\IDisk HD ALT.ico")
    if forma == picmake:
        tk.Label(window, text=f'制作完毕，请于pic文件夹内查看', font=('Arial', 12)).pack()
    elif forma == gifmake:
        tk.Label(window, text=f'制作完毕，请于gif文件夹内查看', font=('Arial', 12)).pack()
    tk.Button(window, text='结束程序', command=endgui).pack()


def endgui():
    window.destroy()


global file_dir, file_list, ishit, window
window = tk.Tk()
window.title('ARGO数据可视化')
window.geometry("300x500")
window.iconbitmap(r".\lib\ico\IDisk HD ALT.ico")
la1 = tk.Label(window, text='请选择数据来源', font=('Arial', 12))
la1.place(y=0)
ishit = 0
b = tk.Button(window, text='ftp', command=ftp, width=13)
c = tk.Button(window, text='demo', command=demo, width=13)
d = tk.Button(window, text='self', command=selfdata, width=13)
#b.grid(column=10, row=10)
b.place(x=0, y=20)
c.place(x=100, y=20)
d.place(x=200, y=20)
window.mainloop()
