import numpy as np
import cv2
from matplotlib import pyplot as plt
import heapq
from colorRectPaint import getRGB


def rectangle_maker(image_name, number_of_rectangles):
    img = cv2.imread(image_name)
    
    imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    plt.subplot(121),plt.imshow(imgray,cmap = 'gray')
    plt.title('Grayscale Image'), plt.xticks([]), plt.yticks([])
    
    
    imgray = cv2.adaptiveThreshold(imgray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,8)
    blur = cv2.GaussianBlur(imgray,(5,5),0.5)
    
    ret3,th3 = cv2.threshold(blur,127, 255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
    contours, hierarchy = cv2.findContours(th3,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    # Find the index of the 10 largest contours
    areas = [cv2.contourArea(c) for c in contours]
    print len(th3)
    print len(th3[0])
    print areas
    
    #max_index = np.argmax(areas)
    #cnt=contours[max_index]
    res = heapq.nlargest(10, areas)
    

    potential_rectangle_contours = []
    potential_x_coor = []
    potential_y_coor = []
    for index1 in range(len(areas)):
        desiredIndex = 0
        for index2 in range(1,len(res)): #don't want to include the rectangle enclosing the entire paper, which is the largest rectangle
            if res[index2] == areas[index1]:
                desiredIndex = index1
        potential_rectangle_contours.append(contours[desiredIndex])
        x,y,w,h = cv2.boundingRect(contours[desiredIndex])
        potential_x_coor.append(x)
        potential_y_coor.append(y)
    
    #array that has 1 where it is a rectangle, 0 where it is not
    isRectangle = []
    for i in xrange(0,len(potential_x_coor)):
        isRectangle.append(1)
    #real_rectangle_contours = potential_rectangle_contours
    #Get rid of bounding boxes that do not define actual rectangles
    for index1 in range(len(potential_x_coor)):
        for index2 in range(index1+1,len(potential_x_coor)):
            if len(potential_rectangle_contours[index1]) < 3:
                isRectangle[index1] = 0
            if len(potential_rectangle_contours[index2]) < 3:
                isRectangle[index2] = 0
            if (abs(potential_x_coor[index1] - potential_x_coor[index2]) < 4):
                isRectangle[index2] = 0
    
    num_rectangles_drawn = 0
    index = 0
    while (num_rectangles_drawn < number_of_rectangles) and (index < len(potential_rectangle_contours)):
        if isRectangle[index] == 1:
            current_contour = potential_rectangle_contours[index]
            x,y,w,h = cv2.boundingRect(current_contour)
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            #RGB = getRGB(img, x, x+w, y, y+h)
            #print RGB
            num_rectangles_drawn = num_rectangles_drawn+1
            #print current_contour
        index = index+1

    
    
    desiredIndex = 0
    for index in range(len(areas)):
        if res[3] == areas[index]:
            desiredIndex = index
            
    cnt1 = contours[desiredIndex]
    
    x,y,w,h = cv2.boundingRect(cnt1)
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
    
    
    cv2.imshow("Show",img)
    cv2.imwrite('new.jpg', img)
    #cv2.waitKey()
    #cv2.destroyAllWindows()