# -*- coding: utf-8 -*-
"""lane_detection_with_openCV.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PYX0wgkubg7HrCSIlb3WUHz0U82xmA68
"""

import cv2 
import numpy as np 
import matplotlib.pyplot as plt

def canny_edge_detector(img): 
  gray_img=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
  blurred_img = cv2.GaussianBlur(gray_img, (5, 5), 0)
  canny_img=cv2.Canny(blurred_img,70,160)
  return canny_img

def region_of_interest (img):
  height=img.shape[0]
  width=img.shape[1]
  vertices=np.array([[(0,height),(width*0.4375,height*0.42),(width*0.54,height*0.42),(width*0.92,height)]],dtype=np.int32)
  mask=np.zeros_like(img)
  cv2.fillPoly(mask,vertices,255)
  masked_img=np.bitwise_and(img,mask)
  return masked_img

def draw_lines(img, lines):
    img = np.copy(img)
    blank_image = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    cv2.fillPoly(blank_image, lines, (255,255,255))
    # for line in lines:
    #     for x1, y1, x2, y2 in line:
          
    #         cv2.line(blank_image, (x1,y1), (x2,y2), (0, 255, 0), thickness=10)

    return blank_image

from scipy import stats 

def avg(lines):
  x_pl=[]
  y_pl=[]
  x_pr=[]
  y_pr=[]
  for line in lines:
    for x1,y1,x2,y2 in line:
      if(abs(x1-x2)==0 or abs(y1-y2)==0 or ( abs(x2-x1)>0 and abs((y2-y1)/(x2-x1))<=0.2)):
        continue
      else:
        slope=(y2-y1)/(x2-x1)
        if slope>0:
          x_pl.append(x1)
          y_pl.append(y1)
          x_pl.append(x2)
          y_pl.append(y2)
        else:
          x_pr.append(x1)
          x_pr.append(x2)
          y_pr.append(y1)
          y_pr.append(y2)
  y1_pl,y2_pl=max(y_pl),min(y_pl)
  s_l,i_l,r,p,se=stats.linregress(x_pl, y_pl)
  y1_pr,y2_pr,x1_pr,x2_pr=720,720,0,0
  x1_pl=(int)((y1_pl-i_l)/s_l)
  x2_pl=(int)((y2_pl-i_l)/s_l)
  if(len(y_pr)!=0):
    y1_pr,y2_pr=max(y_pr),min(y_pr)
    s_r,i_r,r,p,se=stats.linregress(x_pr, y_pr)
    x1_pr=(int)((y1_pr-i_r)/s_r)
    x2_pr=(int)((y2_pr-i_r)/s_r)

  return np.array([[(x2_pl,y2_pl),(x1_pl,y1_pl),(x1_pr,y1_pr),(x2_pr,y2_pr)]])

def combine_all(img):
  canny_img=canny_edge_detector(img)
  cropped=region_of_interest(canny_img)
  lines=cv2.HoughLinesP(cropped,rho=2,theta=np.pi/180,threshold=100,minLineLength=40,maxLineGap=25)
  lines=avg(lines)
  final=draw_lines(img,lines)
  return final

import os
cap = cv2.VideoCapture("/content/drive/MyDrive/Lane detect test data.mp4")

from google.colab.patches import cv2_imshow
i=0
while cap.isOpened():
    ret, frame = cap.read()
    if frame is None :
      break
    directory = r'/content/train'
    os.chdir(directory)
    if i%5==0:

      frame=cv2.resize(frame,(1280,720))
      filename = 'train'+str(i)+'.jpg'
      # # Using cv2.imwrite() method 
      # # Saving the image 
      cv2.imwrite(filename,frame)
      filename = 'test'+str(i)+'.jpg'

      img=combine_all(frame)
      cv2.imwrite(filename, img) 

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    i+=1
cap.release()
cv2.destroyAllWindows()

directory = r'/content'
os.chdir(directory)

