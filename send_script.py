#!/usr/bin/env python

# import rclpy
import os
import sys
sys.path.append('/home/robot/colcon_ws/install/tm_msgs/lib/python3.6/site-packages')
# from tm_msgs.msg import *
# from tm_msgs.srv import *

import cv2
import numpy as np
from math import pi,tan,sin,cos
import math
import matplotlib.pyplot as plt
from copy import deepcopy

def binarize(image , threshold):
    bin_image=cv2.threshold(image, threshold, 255,cv2.THRESH_BINARY)[1]
    return bin_image

# arm client
def send_script(script):
    arm_node = rclpy.create_node('arm')
    arm_cli = arm_node.create_client(SendScript, 'send_script')

    while not arm_cli.wait_for_service(timeout_sec=1.0):
        arm_node.get_logger().info('service not availabe, waiting again...')

    move_cmd = SendScript.Request()
    move_cmd.script = script
    arm_cli.call_async(move_cmd)
    arm_node.destroy_node()

# gripper client
def set_io(state):
    gripper_node = rclpy.create_node('gripper')
    gripper_cli = gripper_node.create_client(SetIO, 'set_io')

    while not gripper_cli.wait_for_service(timeout_sec=1.0):
        gripper_node.get_logger().info('service not availabe, waiting again...')
    
    io_cmd = SetIO.Request()
    io_cmd.module = 1
    io_cmd.type = 1
    io_cmd.pin = 0
    io_cmd.state = state
    gripper_cli.call_async(io_cmd)
    gripper_node.destroy_node()
    # print("io in")
def rotation(x,y,angle):
    angle = angle * (pi / 180)
    # print((x*cos(angle)+y*sin(angle), x*(-1)*sin(angle)+y*cos(angle)))
    return np.array((x*cos(angle)+y*sin(angle), x*(-1)*sin(angle)+y*cos(angle)))

def division(start,end,number):
    dx = (end[0] - start[0] )/number
    dy = (end[1] - start[1] )/number
    return [(start[0]+i*dx,start[1]+i*dy) for i in range(number)] + [end]
def main(args=None):

    # rclpy.init(args=args)
    # targetP1 = "100.00 , 150.00 , 400.00 , 180.00 , 0.00 , 0.00"
    # targetP1 = "230.00, 230, 730, -180.00, 0.0, 135.00"
    # set_io(0.0)
    # targetP1 = "230.00, 230, 730, -180.00, 0.0, 135.00"
    # script = "PTP(\"CPP\","+targetP1+",100,200,0,false)"
    # send_script(script)
    
    # send_script("Vision_DoJob(job1)")

    imagePath = "./result1.png"
    # if os.path.isfile(imagePath):
    #     os.remove(imagePath)
    
    # img = None
    # while img is None:
    #     img = cv2.imread(imagePath)
    img = cv2.imread(imagePath)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # blur = cv2.GaussianBlur(gray, (5, 5), cv2.BORDER_DEFAULT)

    ret, binarized = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY_INV)

    binarized = cv2.bitwise_not(binarized)
    # cv2.imwrite("binarize.png", binarized)

    contours, _ = cv2.findContours(binarized, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # blank = np.zeros(binarized.shape[:2], dtype='uint8')

    # cv2.drawContours(blank, contours, -1, (255, 0, 0), 1)
    # cv2.imwrite("./contours.png", blank)

    # fig,ax = plt.subplots()
    # ax.imshow(img,cmap='gray',extent=[0,len(img[0]),len(img),0])

    corners = []
    pose = []
    board = np.zeros(binarized.shape[:2], dtype='uint8')
    for i in contours:
        (cx, cy), (width, height), angle = rect = cv2.minAreaRect(i)
        if width*height > 200000:
            box =  cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(board, [box], -1, (255, 0, 0), 1)
            # cv2.circle(test, (int(cx), int(cy)), 7, (255), 1)
            # cv2.imwrite("./contour.png", test)
            pose.append(((cx, cy), (width, height), angle))
    
    #print("pose", pose)
    (cx, cy), (width, height), angle = pose[-1]
    # cv2.circle(blank, (int(cx), int(cy)), 7, (255), 1)
    
   
    if width>height:
        height,width= max(height,width),min(width,height)
        angle = 90 - angle
     k = width/82
    print(angle)
    #棋盤上的座標順時針旋轉90-angle 即為 image座標
    # print(f'before rotation {height/2,width/2}')
    center = np.array([cx,cy])
    corners.append(center+ rotation((height/2)-3*k, (width/2)-k, 90-angle)) # 右下
    corners.append(center+ rotation((height/2)-3*k, -(width/2)+k, 90-angle)) # 右上
    corners.append(center+ rotation(-(height/2)+3*k, -(width/2)+k, 90-angle)) # 左上
    corners.append(center+ rotation(-(height/2)+3*k, (width/2)-k, 90-angle)) #左下

    corners = [(int(array[0]),int(array[1])) for array in corners]
    corner_img = deepcopy(board)
    for corner in corners:
        cv2.circle(corner_img, corner, 7, (255), 1)
    cv2.imwrite("./corner.png", corner_img)
    
    # # print(corners)
    edges = [division(corners[0],corners[1],8),division(corners[1],corners[2],9),division(corners[2],corners[3],8),division(corners[3],corners[0],9)]
    coordinates = []
    for idx, start in enumerate(edges[0]):
        coordinates.extend(division(start,edges[2][-1*idx-1],9)) 
    coordinate_img = deepcopy(board)
    for coordinate in coordinates:
        cv2.circle(coordinate_img, (int(coordinate[0]), int(coordinate[1])), 7, (255), 1)
    cv2.imwrite("./coordinate.png", coordinate_img)
    
    board_map = {}
    
    # height = 130


    # plt.savefig(f"analyze_result.png")

    # for i in range(len(corners)):
    #     x =  - 0.362710668 * corners[i][1] + 0.355763769 * corners[i][0] + 250.233006
    #     y =  - 0.367113114* corners[i][1] - 0.367337069 * corners[i][0] + 707.051254
    #     angle = 45

    #     # x = 0.355763769 * r_centers[i] - 0.362710668 * c_centers[i] + 250.233006
    #     # y = -0.367337069 * r_centers[i]- 0.367113114 * c_centers[i] + 707.051254
    #     print("X: {0}, Y: {1}, Angle: {2}".format(x, y, angle))

    #     targetP1 = str(x) + "," + str(y) + ", 150.00 , 180.00 , 0.00 , " + str(angle)
    #     script = "PTP(\"CPP\"," + targetP1 + ",100,200,0,false)"
    #     send_script(script)


        # print("X: {0}, Y: {1}, Angle: {2}".format(x, y, angle))

        # targetP1 = str(x-16) + "," + str(y+1) + ", 150.00 , 180.00 , 0.00 , " + str(angle)
        # script = "PTP(\"CPP\"," + targetP1 + ",100,200,0,false)"
        # send_script(script)

        # targetP1 = str(x-16) + "," + str(y+1) + ", 110.00 , 180.00 , 0.00 , " + str(angle)
        # script = "PTP(\"CPP\"," + targetP1 + ",100,200,0,false)"
        # send_script(script)

        # set_io(1.0)

        # targetP1 = str(x-16) + "," + str(y+1) + ", " + str(height+(15*(len(cxs)+2))) + " , 180.00 , 0.00 , " + str(angle)
        # script = "PTP(\"CPP\"," + targetP1 + ",100,200,0,false)"
        # send_script(script)

        # targetP1 = str(centerx-16) + "," + str(centery+1) + ", " + str(height+(15*(len(cxs)+2))) + ".00 , 180.00 , 0.00 , " + str(angle)
        # script = "PTP(\"CPP\"," + targetP1 + ",100,200,0,false)"
        # send_script(script)

        # targetP1 = str(centerx-16) + "," + str(centery+1) + ", " + str(115+(25*i)) + ".00 , 180.00 , 0.00 , " + str(angle)
        # script = "PTP(\"CPP\"," + targetP1 + ",100,200,0,false)"
        # send_script(script)

        # height += 20

        


    # rclpy.shutdown()


if __name__ == '__main__':
    main()