from datetime import datetime
class Thing:
    def __init__(self, pid, cx, cy):
        self.id = pid
        self.x = cx
        self.y = cy
        # 第一次和最后一次出现时的Y坐标
        self.by = cy
        self.ey = cy
        # 初始化开始时间和结束时间
        self.birth = datetime.now()
        self.end = datetime.now()
        #判断是否检测结束
        self.isend = False
        # 判断是否被改变的元素
        # 初始值为True（从无到有当然是改变了）
        self.ischanged = True

    def getId(self):
        return self.id

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getAge(self):
        age =(datetime.now()-self.birth).total_seconds()
        return age

    def getIsEnd(self):
        return self.isend

    def getIsChanged(self):
        return self.ischanged

    def minus(self):
        self.id -= 1

    def setEnd(self):
        self.ey = self.y
        self.end = datetime.now()
        self.isend = True

    def getYTrack(self):
        return self.ey-self.by

    def getLiveAge(self):
        age =(self.end-self.birth).total_seconds()
        return age

    def updateCoords(self, cx, cy):
        self.x = cx
        self.y = cy
        self.ischanged = True

    def resetChanged(self):
        self.ischanged = False