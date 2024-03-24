#!/usr/bin/env python3
# -- coding: utf-8 -- 
import numpy as np
from PIL import Image, ImageChops
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math


def read_yuv_seq_and_process(seq_name, width, height):
    yuv_file = open(seq_name + '.yuv', 'rb')

    y_data = np.zeros((height, width), dtype = np.uint8)
    for y in range(height):
        for x in range(width):
            y_byte  = yuv_file.read(1) #read one byte data
            y_value = int.from_bytes(y_byte, byteorder = 'big')
            y_data[y, x] = y_value
    yuv_file.close()

    img = Image.fromarray(y_data)
    yuv_img = img.convert('YCbCr')
    return yuv_img


def frame_padding_zero(frame, ctu_size):
    width, height   = frame.size
    width_ctu_nums  = math.ceil(width / ctu_size)
    height_ctu_nums = math.ceil(height / ctu_size)

    pad_frame = np.zeros((height_ctu_nums * ctu_size, width_ctu_nums * ctu_size))
    
    for x in range(height):
        for y in range(width):
            pad_frame[x, y] = frame.getpixel((y, x))[0]
    img         = Image.fromarray(pad_frame)
    pad_frame   = img.convert('YCbCr')
    return pad_frame


def frame_partition(test_seq, unit, yuv_img, frame_width, frame_height, ctu_size):
    width_ctu_nums  = math.ceil(frame_width / ctu_size)
    height_ctu_nums = math.ceil(frame_height / ctu_size)
    ctu_num         = width_ctu_nums * height_ctu_nums

    # Dispaly y image
    fig, ax = plt.subplots(figsize = (10, 6))
    fig.suptitle("H.266(VTM) Luma CTU Partition @codec2021")
    ax.imshow(yuv_img)

    # Draw CTU partition
    for y in range(height_ctu_nums):
        for x in range(width_ctu_nums):
            rect = patches.Rectangle((x * ctu_size, y * ctu_size), ctu_size, ctu_size, linewidth = 2, edgecolor = 'red', facecolor = 'none')
            ax.add_patch(rect)

    # Draw CU partition
    for i in range(0, ctu_num):
        f = open("./CTU/" + unit + '_%d.txt'%(i), "r")
        for line in f:
            row = line.split(" ")
            startx, starty, height, width = int(row[0]), int(row[1]), int(row[2]), int(row[3])
            if startx == 0 and starty == 0 and height == 0 and width == 0:
                continue
            rect = patches.Rectangle((startx, starty), width, height, linewidth = 0.1, edgecolor = 'blue', facecolor = 'none')
            ax.add_patch(rect)
    plt.show()


if __name__ == "__main__":
    seq_name  = "Johnny_1280x720_60_0" #Input the YUV420 frame corresponding to CTU_x.txt
    width     = 1280                   #Set the VTM Encoder width
    height    = 720                    #Set the VTM Encoder height
    ctu_size  = 128                    #Set the VTM Encoder ctu size
    frame_num = 0

    yuv_img = read_yuv_seq_and_process(seq_name, width, height)
    pad_img = frame_padding_zero(yuv_img, ctu_size)
    frame_partition(seq_name, "CTU", pad_img, width, height, ctu_size)
