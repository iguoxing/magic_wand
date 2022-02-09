'''
Author: ArdenZhao
Date: 2022-01-14 11:22:36
LastEditors: Do not edit
LastEditTime: 2022-02-08 15:51:30
FilePath: /magic_wand/magic_wand_notes.py
关键代码
'''

# 批量填充

# 定义函数使用def 关键字  flood 大量  thresh 脱粒  seedpoint 初始点  connection_type 八邻域  rect 区域  mask 掩码


def my_floodFill(image, thresh, seedpoint, connection_type=4, rect=None, mask=None):
    # 函数zeros创建一个由0组成的数组，数组的形状为image.shape[:2]  uint8是用来存储图像的数据类型（为什么用Unit8来存储对象？）
    # 图像的大小可以通过其shape属性来获取，shape返回的是一个tuple元组，第一个元素表示图像的高度，第二个表示图像的宽度，第三个表示像素的通道数。
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

    seeds = [[seedpoint[1], seedpoint[0]]]  # 初始点坐标互换
    lo = thresh
    interval = 2*lo  # 间隔，

    # seeds内无元素时候生长停止
    while len(seeds) != 0:  # Python len() 方法返回对象（字符、列表、元组等）长度或项目个数
        # 栈顶元素出栈
        # pt=(y,x),opencv中水平为x坐标，竖直为y坐标，seeds输入坐标为先竖直坐标，后水平坐标
        pt = seeds.pop(0)
        Ra, Ga, Ba = int(image[pt[0], pt[1], 0]), int(
            image[pt[0], pt[1], 1]), int(image[pt[0], pt[1], 2])
        for i in range(p):  # range() 函数可创建一个整数列表，找到八个邻域的坐标
            tmpX = pt[0] + connection[i][0]
            tmpY = pt[1] + connection[i][1]

            # 检测边界点
            if tmpX < 0 or tmpY < 0 or tmpX >= image.shape[0] or tmpY >= image.shape[1]:
                continue
            Rb, Gb, Bb = int(image[tmpX, tmpY, 0]), int(  # 邻域坐标的像素值
                image[tmpX, tmpY, 1]), int(image[tmpX, tmpY, 2])
            if (seedMark[tmpX, tmpY] == 0) and (Ra-Rb+lo) <= interval and (Ga-Gb+lo) <= interval and (Ba-Bb+lo) <= interval:  # 满足魔法点的条件
                # if (R_min<R<R_max) and (G_min<G<G_max) and (B_min<B<B_max) and :
                seedMark[tmpX, tmpY] = 1  # 赋值后，继续检测
                seeds.append((tmpX, tmpY))  # append() 方法用于在列表末尾添加新的对象。
    return seedMark
