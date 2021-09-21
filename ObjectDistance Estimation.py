#Import All required Libraries 
import cv2
import numpy as np
import matplotlib.pyplot as plt
import imutils
import os 
import glob
from PIL import Image

#Get center of each object
def get_center(image):
    result = cv2.dilate(image, np.ones((3,3), np.uint8), iterations = 1) #Apply dilation to enhacne the object
    cnts = cv2.findContours(image, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #Find contours in the image
    cnts = imutils.grab_contours(cnts)   #Gather all contours

    for c in cnts:
        (x,y,w,h) = cv2.boundingRect(c)  #Get attributes of each contour
        
    center = (x+w/2,y+h/2) #Find the center of object
    return (center,w)

#Calculate distance of an object from the Camera
def calc_distance(left,right,values):
    for image in (left,right):
        hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV) #Convert Image to HSV 
        blur = cv2.GaussianBlur(hsv,(5,5),0) #Apply Gaussian Smoothing to remove noise
        obj = cv2.inRange(hsv,values[0],values[1]) #Extract object in hsv range
        center,width = get_center(obj) #Call for center of object
        
    D = 453*300*37.8/width #Calculate the distance of object from Camera
    return (np.round(D),center)

# This function is use to find which object is moving in straigth line
def check_straight(center):
    
    #Calculating distance to check that the points are collinear or not
    dist1 = np.sqrt(np.square(center[16][0]-center[28][0])+np.square(center[16][1]-center[28][1]))
    dist2 = np.sqrt(np.square(center[28][0]-center[38][0])+np.square(center[28][1]-center[38][1]))
    dist2 = dist1+dist2
    dist = np.sqrt(np.square(center[16][0]-center[38][0])+np.square(center[16][1]-center[38][1]))
    
    if np.round(dist2) == np.round(dist):
        return True
    else:
        return False
        
if __name__ == "__main__":

    path = '/Users/data/dataset/' #Path to Directory

    # Color Ranges for each object
    orange = ((9,239,166),(25,255,255))
    white = ((0,0,21),(0,0,245))
    blue = ((109,255,158),(150,255,240))
    red = ((0,239,151),(0,255,229))
    l_blue = ((75,255,108),(118,255,213))
    yellow = ((24,255,145),(36,255,219))
    green = ((48,240,140),(89,255,240))
    
    print('Frame\t Identity\tDistance')
    centers_o = []
    centers_w = []
    centers_r = []
    centers_b = []
    centers_lb = []
    centers_g = []
    centers_y = []
    
    # Iterate through each left and right Image
    for i in range(4,45):
        I1 = cv2.imread(path+'left-0'+str(i)+'.png')
        I2 = cv2.imread(path+'right-0'+str(i)+'.png')

        dist,center = calc_distance(I1,I2,orange) #Call function for calculating distance from camera
        centers_o.append(center) #Combine all centers for future processing 
        print(str(i)+'\t','Orange\t\t'+str(dist))

        dist,center = calc_distance(I1,I2,white)
        centers_w.append(center)
        print(str(i)+'\t','White\t\t'+str(dist))
        
        dist,center =calc_distance(I1,I2,blue)
        centers_b.append(center)
        print(str(i)+'\t','Blue\t\t'+str(dist))
        
        dist,center =calc_distance(I1,I2,red)
        centers_r.append(center)
        print(str(i)+'\t','Red\t\t'+str(dist))
        
        dist,center =calc_distance(I1,I2,l_blue)
        centers_lb.append(center)
        print(str(i)+'\t','l_blue\t\t'+str(dist))
        
        dist,center =calc_distance(I1,I2,yellow)
        centers_y.append(center)
        print(str(i)+'\t','Yellow\t\t'+str(dist))
        
        dist,center =calc_distance(I1,I2,green)
        centers_g.append(center)
        print(str(i)+'\t','Green\t\t'+str(dist))
        print('\n')
        
    #Display which object is moving in straight line
    print('UFO: ')
    if check_straight(centers_o) == True:
        print("Orange")
    if check_straight(centers_b) == True:
        print("Blue")
    if check_straight(centers_y) == True:
        print("Yellow")
    if check_straight(centers_lb) == True:
        print("Light Blue")
    if check_straight(centers_r) == True:
        print("Red")
    if check_straight(centers_g) == True:
        print("Green")
    if check_straight(centers_w) == True:
        print("White")
