import os
import cv2
import shutil
import numpy as np
from math import *
from tqdm import tqdm
from ppocr.utils.utility import get_image_file_list


# 利用绝对中位差排除异常Theta
def getMAD(s):
    median = np.median(s)
    # 这里的b为波动范围
    b = 1.4826
    mad = b * np.median(np.abs(s-median))

    # 确定一个值，用来排除异常值范围
    lower_limit = median - (3*mad)
    upper_limit = median + (3*mad)

    # print(mad, lower_limit, upper_limit)
    return lower_limit, upper_limit


# 通过霍夫变换计算角度
def CalcDegree(srcImage):
    midImage = cv2.cvtColor(srcImage, cv2.COLOR_BGR2GRAY)
    dstImage = cv2.Canny(midImage, 100, 200, 2, L2gradient=True)
    lineimage = srcImage.copy()


    # 通过霍夫变换检测直线
    # 第4个参数为阈值，阈值越大，检测精度越高
    lines = cv2.HoughLines(dstImage, 1, np.pi / 180, 400)
    # 由于图像不同，阈值不好设定，因为阈值设定过高导致无法检测直线，阈值过低直线太多，速度很慢
    sum = 0

    # 绝对中位差排除异常值
    thetaList = []
    for i in range(len(lines)):
        for rho, theta in lines[i]:
            thetaList.append(theta)

    lower_limit, upper_limit = getMAD(thetaList)

    num = 0
    for i in range(len(lines)):
        for rho, theta in lines[i]:
            if lower_limit <= theta <= upper_limit:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(round(x0 + 1000 * (-b)))
                y1 = int(round(y0 + 1000 * a))
                x2 = int(round(x0 - 1000 * (-b)))
                y2 = int(round(y0 - 1000 * a))
                # 只选角度最小的作为旋转角度
                sum += theta
                num = num + 1
                cv2.line(lineimage, (x1, y1), (x2, y2), (0, 0, 255), 2)

    #cv2.namedWindow("Imagelines", 0)
    #cv2.imshow("Imagelines", lineimage)
    #cv2.waitKey(0)

    average = sum / num
    res = average / np.pi * 180

    if res < 90:
        res = res + 90
    else:
        res = res - 90

    return res


# 逆时针旋转图像degree角度（原尺寸）
def rotateImage(src, degree):

    h, w = src.shape[:2]

    RotateMatrix = cv2.getRotationMatrix2D((w / 2.0, h / 2.0), degree, 1)

    rotate = cv2.warpAffine(src, RotateMatrix, (w, h), borderValue=(255, 255, 255))

    return rotate


def opencv_rotate(img, angle):
    h, w = img.shape[:2]
    center = (w / 2, h / 2)
    scale = 1.0
    # 2.1获取M矩阵

    M = cv2.getRotationMatrix2D(center, angle, scale)
    # 2.2 新的宽高，radians(angle) 把角度转为弧度 sin(弧度)
    new_H = int(w * fabs(sin(radians(angle))) + h * fabs(cos(radians(angle))))
    new_W = int(h * fabs(sin(radians(angle))) + w * fabs(cos(radians(angle))))
    # 2.3 平移
    M[0, 2] += (new_W - w) / 2
    M[1, 2] += (new_H - h) / 2
    rotate = cv2.warpAffine(img, M, (new_W, new_H), borderValue=(0, 0, 0))
    return rotate


def NMS(bounding_boxes, confidence_score, threshold=0.45):

    if len(bounding_boxes) == 0:
        return []

    # Bounding boxes
    boxes = np.array(bounding_boxes)
    boxes = boxes.astype("float")

    # coordinates of bounding boxes
    start_x = boxes[:, 0]
    start_y = boxes[:, 1]
    end_x = boxes[:, 2]
    end_y = boxes[:, 3]

    # Confidence scores of bounding boxes
    score = np.array(confidence_score)

    # Picked bounding boxes
    picked_boxes = []

    # Compute areas of bounding boxes
    areas = (end_x - start_x + 1) * (end_y - start_y + 1)

    # Sort by confidence score of bounding boxes
    order = np.argsort(score)

    # Iterate bounding boxes
    while order.size > 0:
        # The index of largest confidence score
        index = order[-1]

        # Pick the bounding box with largest confidence score
        picked_boxes.append(bounding_boxes[index])

        # Compute ordinates of intersection-over-union(IOU)
        x1 = np.maximum(start_x[index], start_x[order[:-1]])
        x2 = np.minimum(end_x[index], end_x[order[:-1]])
        y1 = np.maximum(start_y[index], start_y[order[:-1]])
        y2 = np.minimum(end_y[index], end_y[order[:-1]])

        # Compute areas of intersection-over-union
        w = np.maximum(0.0, x2 - x1 + 1)
        h = np.maximum(0.0, y2 - y1 + 1)
        intersection = w * h

        # Compute the ratio between intersection and union
        #ratio = intersection / (areas[index] + areas[order[:-1]] - intersection)
        ratio = intersection / (np.minimum(areas[index], areas[order[:-1]]))

        left = np.where(ratio < threshold)
        order = order[left]

    return picked_boxes


def edge_det(img):
    H, W, C = img.shape
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    _, mask = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY)
    #cv2.namedWindow('mask', 0)
    #cv2.imshow('mask', mask)
    #cv2.waitKey(0)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
    erode = cv2.erode(mask, kernel, iterations=4)
    #erode = cv2.bitwise_not(erode)
    #cv2.namedWindow('erode', 0)
    #cv2.imshow('erode', erode)
    #cv2.waitKey(0)

    contours, hierarchy = cv2.findContours(erode, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    boxes = []
    area = []

    for contour in contours:
        ar = cv2.contourArea(contour)
        if ar < 5000 or ar > 3000000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        boxes.append((x ,y, x+w, y+h))
        area.append(w * h)

    boxes = NMS(boxes, area)

    num = 0
    fir_area = 0
    cut_box = []
    for box in boxes:
        x, y, xx, yy = box

        if num == 0:
            fir_area = (xx - x) * (yy - y)
        elif num == 1:
            sec_area = (xx - x) * (yy - y)
            if sec_area / fir_area < 0.6:
                break
        elif num >= 2:
            break
        x1 = max(1, x - 100)
        y1 = max(1, y - 30)
        x2 = min(xx+30, W-1)
        y2 = min(yy+30, H-1)
        #cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 10)
        cut_box.append(img[y1:y2, x1:x2])
        num = num + 1

    #img = np.concatenate([cv2.cvtColor(erode, cv2.COLOR_GRAY2RGB), img], axis=1)
    #cv2.namedWindow('contour', 0)
    #cv2.imshow('contour', img)
    #cv2.waitKey(0)

    ans = None
    if len(cut_box) == 1:
        cur = cut_box[0]
        h, w, c = cur.shape
        print(w / h)
        if w / h < 2:
            ans = img
        else:
            ans = cut_box[0]
    elif len(cut_box) == 2:
        h1, w1, c1 = cut_box[0].shape
        h2, w2, c2 = cut_box[1].shape
        cur = cut_box[1]
        cur = cv2.resize(cur, (int(w2 * h1 / h2), h1))
        cur = np.concatenate((cut_box[0], cur), axis=1)
        ans = cur

    return ans


def cut_image(img):
    degree = CalcDegree(img)  # 求矩形主要方向与x轴的夹角degree
    rotate = opencv_rotate(img, degree)
    res = edge_det(rotate)

    return res


if __name__ == '__main__':
    image_file_list = get_image_file_list("/home/dachuang/workspace/Pjz/Project/driver_license")

    save_dir = "/home/dachuang/workspace/Pjz/Project/PaddleOCR-release-2.6/output_images/rotate/"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    else:
        shutil.rmtree(save_dir)
        os.mkdir(save_dir)

    for img_path in tqdm(image_file_list):
        img = cv2.imread(img_path)

        # 调整图像角度
        degree = CalcDegree(img)  # 求矩形主要方向与x轴的夹角degree
        rotate = opencv_rotate(img, degree)

        save_path = save_dir + img_path.split("/")[-1]
        cv2.imwrite(save_path, rotate)


        #res = edge_det(rotate)

        #cv2.namedWindow("pic", 0)
        #cv2.imshow("pic", res)
        #cv2.waitKey(0)


        #save_path = save_dir + img_path.split("\\")[-1]
        #cv2.imwrite(save_path, res)




































'''
#PCA旋转校正图片
import os
import time
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from ppocr.utils.utility import get_image_file_list


def hack_pca(filename):

    img_r = (plt.imread(filename)).astype(np.float64)

    # YOUR CODE HERE
    # begin answer
    # convert to gray image
    H, W, _ = np.shape(img_r)
    img_gray = np.dot(img_r, [0.299, 0.587, 0.114])


    # record the place not zero(or some threshold)

    threshold = 150
    data_points = np.argwhere(img_gray > threshold)

    cov_mat = np.cov(data_points.T)
    eig_val, eig_vec = np.linalg.eig(cov_mat)
    rot_mat = np.array([[eig_vec[0, 0], eig_vec[0, 1]],
                        [eig_vec[1, 0], eig_vec[1, 1]]]).T
    place_mat = np.zeros([H, W, 2], dtype=int)
    for i in range(H):
        for j in range(W):
            place_mat[i, j] = rot_mat.dot(np.array([i, j]))

    img_parallel = np.zeros([H, W, 3], dtype=float)
    mean_x = np.mean(place_mat[:, :, 0])
    mean_y = np.mean(place_mat[:, :, 1])
    place_mat = place_mat - np.array([mean_x - H/2, mean_y - W/2])
    place_mat = place_mat.astype(np.int64)


    for i in range(H):
        for j in range(W):
            if 0 <= place_mat[i, j, 0] < H and 0 <= place_mat[i, j, 1] < W:
                img_parallel[place_mat[i, j, 0], place_mat[i, j, 1]] = img_r[i, j]
    img_parallel = img_parallel / 255

    #plt.figure(1)
    #plt.imshow(img_parallel)
    #plt.show()
    return img_parallel, eig_vec, img_gray
    # end answer


if __name__ == "__main__":
    image_file_list = get_image_file_list(r"C:\\Users\12138\Desktop\project\driver_license")
    save_path = r"C:\\Users\12138\Desktop\project\rotate_image"
    threshold = [130, 170, 190, 210]

    for t in tqdm(threshold):
        save_path_cur = os.path.join(save_path, str(t))
        if not os.path.exists(save_path_cur):
            os.makedirs(save_path_cur)
        for img_path in tqdm(image_file_list):
            T1 = time.time()
            img, _, _ = hack_pca(img_path)
            img_name = img_path.split("\\")[-1]
            plt.imsave(os.path.join(save_path_cur, img_name), img)
            T2 = time.time()
            print("\nrotate one image costs: %s second \n" % (T2 - T1))

'''