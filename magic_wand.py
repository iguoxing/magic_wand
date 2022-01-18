'''
Author: ArdenZhao
Date: 2022-01-14 11:22:36
LastEditors: Do not edit
LastEditTime: 2022-01-18 11:09:26
FilePath: /magic_wand/magic_wand.py
关键代码
'''

# 批量填充


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
