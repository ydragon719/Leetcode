import os
from pathlib import WindowsPath
from tkinter import *
import tkinter as tk
from PIL import Image,ImageTk
import cv2

def plus(str):
    return str.zfill(8)
# 获取水印图片的每一个像素值,i：指定要检查的像素点的逻辑X轴坐标。j：指定要检查的像素点的逻辑Y轴坐标。
def getcode(watermark):
    str1 = ""
    for i in range(watermark.size[0]):
        for j in range(watermark.size[1]):
            # 获取每个像素的RGB值
            rgb = watermark.getpixel((i, j))
            str1 = str1 + plus(bin(rgb[0]).replace('0b', ''))
            str1 = str1 + plus(bin(rgb[1]).replace('0b', ''))
            str1 = str1 + plus(bin(rgb[2]).replace('0b', ''))
    # print (str)
    return str1
#打开并显示原图
def checkEmbed(filePath):    
    if(os.path.exists(filePath)):
        img = cv2.imread(filePath)
        if img is None:
            text.insert(END, filePath +'格式不正确！\n')
        else:
            global embedImage #修改sourseImage
            cv2.imshow('image',img)  #显示图片,[图片窗口名字，图片]
            text.insert(END, '水印嵌入图'+filePath +'读取成功！\n')       

            #将图片显示在窗口中
            photo = Image.open(filePath)  #括号里为需要显示在图形化界面里的图片
            photo = photo.resize((140,140))  #规定图片大小          
            embedImage = ImageTk.PhotoImage(photo)
            
            imageLable1.configure(image = embedImage)
            imageLable1.image = embedImage
            embedImage = Image.open(filePath)
    else:
        text.insert(END, filePath +'路径不存在！\n')
#打开并显示水印
def checkWaterMark(filePath):    
    if(os.path.exists(filePath)):
        img = cv2.imread(filePath)
        if img is None:
            text.insert(END, filePath +'格式不正确！\n')
        else:
            global waterMark #修改waterMark
            cv2.imshow('waterMark',img)  #显示图片,[图片窗口名字，图片]

            text.insert(END, '水印'+ filePath +'读取成功！\n')

            photo = Image.open(filePath)  #括号里为需要显示在图形化界面里的图片
            photo = photo.resize((140,140))  #规定图片大小
            waterMark = ImageTk.PhotoImage(photo)
            #将图片显示在窗口中
            imageLable2.configure(image = waterMark)
            imageLable2.image = waterMark
            waterMark = Image.open(filePath)
    else:
        text.insert(END, filePath +'路径不存在！\n')
#水印嵌入并保存到指定路径
def embedWaterMark(filePath):
    if(not os.path.exists(filePath)):
        text.insert(END, '未输入有效路径！\n')
    elif(sourseImage==emptyImg):
        text.insert(END, '未输入有效原图！\n')
        return
    elif(sourseImage==emptyImg):
        text.insert(END,'未输入有效水印！')
        return
    elif(sourseImage.width*sourseImage.height<8*waterMark.width*waterMark.height):
        text.insert(END,'水印图过大或者原图太小！')
        return
    #符合嵌入条件
    global embedImage
    #提取水印图代码
    code = getcode(waterMark.convert("RGB"))
    # 计数器
    count = 0
    codelen = len(code)
    #水印嵌入图初始化
    embedImage = sourseImage
    #print (codelen)
    for i in range(embedImage.size[0]):
        for j in range(embedImage.size[1]):
            # 获取每个像素的RGB值
            data = embedImage.getpixel((i, j))
            if count == codelen:
                break
            r = data[0]
            g = data[1]
            b = data[2]
            # print (r)
            # print(codelen)#24
            r = (r - r % 2) + int(code[count])
            count += 1

            if count == codelen:
                embedImage.putpixel((i, j), (r, g, b))
                break
            
            g = (g - g % 2) + int(code[count])
            count += 1
            if count == codelen:
                embedImage.putpixel((i, j), (r, g, b))
                break

            b = (b - b % 2) + int(code[count])
            count += 1
            if count == codelen:
                embedImage.putpixel((i, j), (r, g, b))
                break
                # 每3次循环表示一组RGB值被替换完毕，可以进行写入
            if count % 3 == 0:
                embedImage.putpixel((i, j), (r, g, b))

    #保存到filePath指定的路径
    embedImage.save(filePath)

    #将图片显示在窗口中
    photo = embedImage
    photo = photo.resize((140,140))  #规定图片大小          
    embedImage = ImageTk.PhotoImage(photo)    
    imageLable3.configure(image = embedImage)
    imageLable3.image = embedImage
    embedImage = Image.open(filePath)
    text.insert(END, filePath+'水印嵌入成功！\n')
    #打开图片
    img = cv2.imread(filePath)
    cv2.imshow('watermark_im',img) 
    text.insert(END, '水印宽：%d,水印高：%d'%(waterMark.width,waterMark.height))
#提取水印
def extractWatermark(img, length):
    width = im.size[0]
    height = im.size[1]
    # 计数器
    count = 0
    wt = ""

    for i in range(width):
        for j in range(height):
            # 获取像素点的值
            rgb = img.getpixel((i, j))
            # 提取R通道的附加值
            if count % 3 == 0:
                count += 1
                wt = wt + str(rgb[0] % 2)
                if count == length:
                    break

                    # 提取G通道的附加值
            if count % 3 == 1:
                count += 1
                wt = wt + str(rgb[1] % 2)
                if count == length:
                    break

                    # 提取B通道的附加值
            if count % 3 == 2:
                count += 1
                wt = wt + str(rgb[2] % 2)
                if count == length:
                    break
        if count == length:
            break
    return wt


global waterMark          #水印
global embedImage         #水印嵌入图
global emptyImg           #空白图

#主窗体
window = Tk()
window.geometry('640x480')
window.title('LSB水印提取')

#初始化
photo = Image.open("LSB+DCT\empty.png")
photo = photo.resize((140,140))  #规定图片大小
emptyImg = ImageTk.PhotoImage(photo)
waterMark = emptyImg
embedImage = emptyImg

#提示框
lable1 = Label(window, text='请输入嵌入水印图的文件路径')
lable1.place(relx=0, rely=0.0, relwidth=0.4, relheight=0.1)
#提示框
lable2 = Label(window, text='请输入水印的文件路径')
lable2.place(relx=0, rely=0.3, relwidth=0.4, relheight=0.1)

imageLable1 = Label(window,image = embedImage)
imageLable1.place(relx=0.41, rely=0.05)
imageLable2 = Label(window,image = waterMark)
imageLable2.place(relx=0.41, rely=0.35)



#水印路径输入
embedEntry = Entry(window)
embedEntry.place(relx=0.05, rely=0.1, relwidth=0.3, relheight=0.1)
#查看水印按钮
embedCheakButton = Button(window, text='查看水印嵌入图', command=lambda:checkEmbed(embedEntry.get()))
embedCheakButton.place(relx=0.05, rely=0.2, relwidth=0.3, relheight=0.1)

#嵌入水印图按钮
embedEntry = Entry(window)
embedEntry.place(relx=0.05, rely=0.4, relwidth=0.3, relheight=0.1)
#嵌入水印按钮
embedButton = Button(window, text='嵌入水印', command=lambda:embedWaterMark(embedEntry.get()))
embedButton.place(relx=0.05, rely=0.5, relwidth=0.3, relheight=0.1)

# 在窗体垂直自上而下位置60%处起，布局相对窗体高度40%高的文本框
text = Text(window)
text.place(relx=0.7, relheight=1,relwidth=0.3)

window.mainloop()
