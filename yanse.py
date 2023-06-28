# -*- coding: utf-8 -*-
import os
import cv2
import cv2
import colorList

path = r"D:\Desktop\pingan_project\yolov5-5.0\runs\detect\exp2"         # jpg图片和对应的生成结果的txt标注文件，放在一起
path3 = r"D:\Desktop\pingan_project\yolov5-5.0\cutpictures"    # 裁剪出来的小图保存的根目录
w = 1920                       # 原始图片resize
h = 1080
img_total = []
txt_total = []

file = os.listdir(path)
for filename in file:
    first,last = os.path.splitext(filename)
    if last == ".jpg":                      # 图片的后缀名
        img_total.append(first)
    #print(img_total)
    else:
        txt_total.append(first)

for img_ in img_total:
    if img_ in txt_total:
        filename_img = img_+".jpg"          # 图片的后缀名
        # print('filename_img:', filename_img)
        path1 = os.path.join(path,filename_img)
        img = cv2.imread(path1)
        img = cv2.resize(img,(w,h),interpolation = cv2.INTER_CUBIC)        # resize 图像大小，否则roi区域可能会报错
        filename_txt = img_+".txt"
        # print('filename_txt:', filename_txt)
        n = 1
        countred = 0
        countblue = 0
        with open(os.path.join(path,filename_txt),"r+",encoding="utf-8",errors="ignore") as f:
            for line in f:
                aa = line.split(" ")
                x_center = w * float(aa[1])       # aa[1]左上点的x坐标
                y_center = h * float(aa[2])       # aa[2]左上点的y坐标
                width = int(w*float(aa[3]))       # aa[3]图片width
                height = int(h*float(aa[4]))      # aa[4]图片height
                lefttopx = int(x_center-width/2.0)
                lefttopy = int(y_center-height/2.0)
                roi = img[lefttopy+1:lefttopy+height+3,lefttopx+1:lefttopx+width+1]   # [左上y:右下y,左上x:右下x] (y1:y2,x1:x2)需要调参，否则裁剪出来的小图可能不太好
                                        # 如果不resize图片统一大小，可能会得到有的roi为[]导致报错
                filename_last = img_+"_"+str(n)+".jpg"    # 裁剪出来的小图文件名
                # print(filename_last)
                path2 = os.path.join(path3,"roi")           # 需要在path3路径下创建一个roi文件夹
                                                            # 裁剪小图的保存位置
                cv2.imwrite(os.path.join(path2,filename_last),roi)
                n = n + 1

                frame = cv2.imread(fr'D:\Desktop\pingan_project\yolov5-5.0\cutpictures\roi\{filename_last}')
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                maxsum = 0
                color = None
                color_dict = colorList.getColorList()
                for d in color_dict:
                    mask = cv2.inRange(hsv, color_dict[d][0], color_dict[d][1])
                    binary = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)[1]
                    binary = cv2.dilate(binary, None, iterations=2)
                    cnts = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
                    sum = 0
                    for c in cnts:
                        sum += cv2.contourArea(c)
                    # print("%s  , %d" %(d, sum ))
                    if sum > maxsum:
                        maxsum = sum
                        color = d


                if color == 'red':
                    countred = countred+1
                if color == 'blue':
                    countblue = countblue+1
        frame = cv2.imread(f'D:\Desktop\pingan_project\yolov5-5.0\data\image\{img_}.jpg')
        frame = cv2.resize(frame, (600, 600))

        cv2.imshow(f'{img_}', frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print(f'{img_}',f'一共有{countblue+countred}人',f'蓝色上衣人数：{countblue}',f'红色上衣人数：{countred}')


    else:
        continue
