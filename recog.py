import numpy as np
import cv2
from datetime import datetime
from Thing import Thing
cap = cv2.VideoCapture('../test.mp4')
# cap = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows = True)#创建背景图
kernelOp = np.ones((3,3),np.uint8)
kernelCl = np.ones((11,11),np.uint8)

# 变量
font = cv2.FONT_HERSHEY_SIMPLEX
things = []
pid = 1
areaTH = 500 #最小轮廓大小
while(cap.isOpened()):
    # 读入框架
    ret, frame = cap.read()
    fgmask = fgbg.apply(frame)
    try:
        ret, imbin = cv2.threshold(fgmask, 250, 255, cv2.THRESH_BINARY)
        # 打开
        mask = cv2.morphologyEx(imbin, cv2.MORPH_OPEN, kernelOp)
        # 收缩
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernelCl)
    except:
        for p in things:
            print(p.getId())
            print(p.getX())
            print(p.getY())
            print(p.getAge())
            print("---------------")
        # print(eof)
        break

    # 这一帧检测的开始进行之前元素的初始化
    for i in things:
        i.resetChanged()

    _, contours0, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours0:
        area = cv2.contourArea(cnt)
        if area > areaTH:
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            x,y,w,h = cv2.boundingRect(cnt)

            new = True
            for i in things:
                # 从没有结束的对象里面找
                if i.getIsEnd()==False and abs(x-i.getX()) <= w and abs(y-i.getY()) <= h:
                    # 如果新探测到的接近前一帧探测到的
                    new = False
                    i.updateCoords(cx, cy) #更新那个接近的坐标顺便记录此元素这一次被改变了
                    break
            if new == True:
                # 如果确定有新的
                p = Thing(pid, cx, cy)
                things.append(p)
                pid += 1
            cv2.circle(frame, (cx,cy), 5, (0,0,225), -1)#小红点
            img = cv2.rectangle(frame, (x,y), (x+w, y+h), (0,225,0), 2)
            cv2.drawContours(frame, cnt, -1, (0,255,0), 3)

    # 检查之后的物品
    for i in things:
        if i.getIsEnd()==False:
            # 如果在尚存物品中发现本轮未改变的或者发现超出范围的物品 立即将其结束
            if i.getIsChanged()==False or i.getY()>=850:
                i.setEnd();

    i=0
    while i<=(len(things)-1):
        # 如果在已经结束的物品中发现出现时间小于一定值或在Y方向上移动距离过小 
        # 则将之视作干扰项 将其删除出list 在这个之后标号的物品id-1
        if things[i].getIsEnd()==True and (things[i].getLiveAge()<=2.2 or things[i].getYTrack()<=200):
            things.pop(i)
            # 将其之后标记的物品的id以及pid都减一
            j=i
            while j<=(len(things)-1):
                things[j].minus()
                j += 1
            pid -= 1
        else:
            i = i+1

    for i in things:
        # 如果物品在当前帧中未结束查找
        if i.getIsEnd()==False:
            cv2.putText(frame, str(i.getId()), (i.getX(), i.getY()), font, 1, (0,0,255), 2)

    cv2.imshow('frame', frame)

    # 按下'Q'或者esc退出
    k = cv2.waitKey(3) & 0xff
    if k==27:
        break

cap.release()
cv2.destroyAllWindows()