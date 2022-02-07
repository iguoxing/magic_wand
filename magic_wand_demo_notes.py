import numpy as np
import cv2


def nothing(x):
    pass


def my_floodFill(image, thresh, seedpoint, connection_type=4, rect=None, mask=None):
    seedMark = np.zeros(image.shape[:2], dtype=np.uint8)
    # 八邻域
    if connection_type == 8:
        p = 8
        connection = [(-1, -1), (-1, 0), (-1, 1), (0, 1),
                      (1, 1), (1, 0), (1, -1), (0, -1)]
    elif connection_type == 4:
        p = 4
        connection = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    else:
        p = 8
        connection = [(-1, -1), (-1, 0), (-1, 1), (0, 1),
                      (1, 1), (1, 0), (1, -1), (0, -1)]

    seeds = [[seedpoint[1], seedpoint[0]]]
    lo = thresh
    interval = 2*lo

    # seeds内无元素时候生长停止
    while len(seeds) != 0:
        # 栈顶元素出栈
        # pt=(y,x),opencv中水平为x坐标，竖直为y坐标，seeds输入坐标为先竖直坐标，后水平坐标
        pt = seeds.pop(0)
        Ra, Ga, Ba = int(image[pt[0], pt[1], 0]), int(
            image[pt[0], pt[1], 1]), int(image[pt[0], pt[1], 2])
        for i in range(p):
            tmpX = pt[0] + connection[i][0]
            tmpY = pt[1] + connection[i][1]

            # 检测边界点
            if tmpX < 0 or tmpY < 0 or tmpX >= image.shape[0] or tmpY >= image.shape[1]:
                continue
            Rb, Gb, Bb = int(image[tmpX, tmpY, 0]), int(
                image[tmpX, tmpY, 1]), int(image[tmpX, tmpY, 2])
            if (seedMark[tmpX, tmpY] == 0) and (Ra-Rb+lo) <= interval and (Ga-Gb+lo) <= interval and (Ba-Bb+lo) <= interval:
                # if (R_min<R<R_max) and (G_min<G<G_max) and (B_min<B<B_max) and :
                seedMark[tmpX, tmpY] = 1
                seeds.append((tmpX, tmpY))
    return seedMark

# 我的填充


class Segment_my(object):
    def __init__(self):
        self.show_h, self.show_w = 600, 800  # 显示图片宽高
        self.horizontal, self.vertical = 0, 0  # 原图是否超出显示图片
        self.dx, self.dy = 0, 0  # 显示图片相对于原图的坐标
        self.scroll_w = 16  # 滚动条宽度
        self.sx, self.sy = 0, 0  # 滚动块相对于滚动条的坐标
        self.flag, self.flag_hor, self.flag_ver = 0, 0, 0  # 鼠标操作类型，鼠标是否在水平滚动条上，鼠标是否在垂直滚动条上
        self.x1, self.y1, self.x2, self.y2, self.x3, self.y3 = 0, 0, 0, 0, 0, 0  # 中间变量
        self.win_w, self.win_h = self.show_w + \
            self.scroll_w, self.show_h + self.scroll_w  # 窗口宽高
        self.seedx, self.seedy = -1, -1  # 种子点坐标
        self.param = [0, 0, 0, 0, 0, 0, 0]

    # 导入图片
    def init_image(self, image_file):
        self.image = cv2.imdecode(np.fromfile(image_file, dtype=np.uint8), 1)
        self.image_raw = self.image.copy()
        self.img_h, self.img_w = self.image.shape[0:2]  # 原图宽高
        self.mask = np.zeros((self.img_h+2, self.img_w+2), np.uint8)
        self.zero_image = np.zeros(self.image.shape, self.image.dtype)
        self.scroll_har, self.scroll_var = self.win_w * self.show_w / \
            self.img_w, self.win_h * self.show_h / self.img_h  # 滚动条水平垂直长度
        self.f1, self.f2 = (self.img_w - self.show_w) / (self.win_w - self.scroll_har), (self.img_h -
                                                                                         self.show_h) / (self.win_h - self.scroll_var)  # 原图可移动部分占滚动条可移动部分的比例
        if self.img_h <= self.show_h and self.img_w <= self.show_w:
            self.show_rect = self.image.copy()
            self.show_h, self.show_w = self.img_h, self.img_w
        else:
            if self.img_w > self.show_w:
                self.horizontal = 1
            if self.img_h > self.show_h:
                self.vertical = 1
            self.show_rect = self.image[self.dy:self.dy +
                                        self.show_h, self.dx:self.dx + self.show_w].copy()
        self.show_image = cv2.copyMakeBorder(
            self.show_rect, 0, self.scroll_w, 0, self.scroll_w, cv2.BORDER_CONSTANT, value=(255, 255, 255))

    def mouse(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if 0 <= x < self.show_w and 0 <= y < self.show_h:
                self.seedx, self.seedy = int(x)+self.dx, int(y)+self.dy
                self.update(self.param, True)

        if event == cv2.EVENT_LBUTTONDOWN:  # 左键点击
            if self.flag == 0:
                if self.horizontal and 0 < x < self.win_w and self.win_h - self.scroll_w < y < self.win_h:
                    self.flag_hor = 1  # 鼠标在水平滚动条上
                elif self.vertical and self.win_w - self.scroll_w < x < self.win_w and 0 < y < self.win_h:
                    self.flag_ver = 1  # 鼠标在垂直滚动条上
                if self.flag_hor or self.flag_ver:
                    self.flag = 1  # 进行滚动条垂直
                    # 使鼠标移动距离都是相对于初始滚动条点击位置，而不是相对于上一位置
                    self.x1, self.y1, self.x2, self.y2, self.x3, self.y3 = x, y, self.dx, self.dy, self.sx, self.sy
        # 按住左键拖曳
        elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):
            if self.flag == 1:
                if self.flag_hor:
                    w = (x - self.x1) / 2  # 移动宽度
                    self.dx = self.x2 + w * self.f1  # 原图x
                    if self.dx < 0:  # 位置矫正
                        self.dx = 0
                    elif self.dx > self.img_w - self.show_w:
                        self.dx = self.img_w - self.show_w
                    self.sx = self.x3 + w  # 滚动条x
                    if self.sx < 0:  # 位置矫正
                        self.sx = 0
                    elif self.sx > self.win_w - self.scroll_har:
                        self.sx = self.win_w - self.scroll_har
                if self.flag_ver:
                    h = y - self.y1  # 移动高度
                    self.dy = self.y2 + h * self.f2  # 原图y
                    if self.dy < 0:  # 位置矫正
                        self.dy = 0
                    elif self.dy > self.img_h - self.show_h:
                        self.dy = self.img_h - self.show_h
                    self.sy = self.y3 + h  # 滚动条y
                    if self.sy < 0:  # 位置矫正
                        self.sy = 0
                    elif self.sy > self.win_h - self.scroll_var:
                        self.sy = self.win_h - self.scroll_var
                self.dx, self.dy = int(self.dx), int(self.dy)
                self.show_rect = self.image[self.dy:self.dy + self.show_h,
                                            self.dx:self.dx + self.show_w].copy()  # 截取显示图片
        elif event == cv2.EVENT_LBUTTONUP:  # 左键释放
            self.flag, self.flag_hor, self.flag_ver = 0, 0, 0
            self.x1, self.y1, self.x2, self.y2, self.x3, self.y3 = 0, 0, 0, 0, 0, 0

        if self.horizontal and self.vertical:
            self.sx, self.sy = int(self.sx), int(self.sy)
            # 对dst1画图而非dst，避免鼠标事件不断刷新使显示图片不断进行填充
            self.show_image = cv2.copyMakeBorder(
                self.show_rect, 0, self.scroll_w, 0, self.scroll_w, cv2.BORDER_CONSTANT, value=[255, 255, 255])
            cv2.rectangle(self.show_image, (self.sx, self.show_h), (int(
                self.sx + self.scroll_har), self.win_h), (181, 181, 181), -1)  # 画水平滚动条
            cv2.rectangle(self.show_image, (self.show_w, self.sy), (self.win_w, int(
                self.sy + self.scroll_var)), (181, 181, 181), -1)  # 画垂直滚动条
        elif self.horizontal == 0 and self.vertical:
            self.sx, self.sy = int(self.sx), int(self.sy)
            self.show_image = cv2.copyMakeBorder(
                self.show_rect, 0, 0, 0, self.scroll_w, cv2.BORDER_CONSTANT, value=[255, 255, 255])
            cv2.rectangle(self.show_image, (self.show_w, self.sy), (self.win_w, int(
                self.sy + self.scroll_var)), (181, 181, 181), -1)  # 画垂直滚动条
        elif self.horizontal and self.vertical == 0:
            self.sx, self.sy = int(self.sx), int(self.sy)
            self.show_image = cv2.copyMakeBorder(
                self.show_rect, 0, self.scroll_w, 0, 0, cv2.BORDER_CONSTANT, value=[255, 255, 255])
            cv2.rectangle(self.show_image, (self.sx, self.show_h), (int(
                self.sx + self.scroll_har), self.win_h), (181, 181, 181), -1)  # 画水平滚动条

    def update(self, param, flag=False):
        thr, alpha, beta, hue, saturation, lightness, gamma = param
        if self.param != param or flag:
            alpha /= 100
            self.image = cv2.addWeighted(
                self.image_raw, alpha, self.zero_image, 1 - alpha, beta)
            if 0 <= self.seedx <= self.img_w and 0 <= self.seedy <= self.img_h:
                self.mask[:] = 0
                # cv2.floodFill(self.image,self.mask,(self.seedx,self.seedy),255,(thr,thr,thr),(thr,thr,thr),cv2.FLOODFILL_MASK_ONLY)
                mask = my_floodFill(self.image, thr, (self.seedx, self.seedy))
                contours, _ = cv2.findContours(
                    mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                if len(contours) > 0:
                    cv2.drawContours(self.image, contours,
                                     0, (0, 255, 0), 1, 8)
                else:
                    self.image[self.seedy, self.seedx] = [0, 255, 0]

        self.show_image[:self.show_h, :self.show_w] = self.image[self.dy:self.dy + self.show_h,
                                                                 self.dx:self.dx + self.show_w].copy()
        self.param = param


image_file = r"/Users/zhaoarden/Desktop/111.jpeg"
my_segment = Segment_my()
my_segment.init_image(image_file)
cv2.namedWindow('image', cv2.WINDOW_AUTOSIZE)
cv2.createTrackbar('Threshold', 'image', 1, 30, nothing)
cv2.createTrackbar('Contrast', 'image', 100, 300, nothing)

cv2.setMouseCallback('image', my_segment.mouse)

alpha, beta, hue, saturation, lightness, gamma = 100, 0, 100, 100, 100, 1

while(1):
    cv2.imshow('image', my_segment.show_image)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
    # # # get current positions of four trackbars
    thr = cv2.getTrackbarPos('Threshold', 'image')
    alpha = cv2.getTrackbarPos('Contrast', 'image')
    my_segment.update([thr, alpha, beta, hue, saturation, lightness, gamma])

cv2.waitKey()
cv2.destroyAllWindows()
