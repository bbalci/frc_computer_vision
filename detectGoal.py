import cv2
import numpy as np
import math

H, S, V = 262/2, 12*255/100, 35*255/100

goalCount = 0
oldX, oldY = 0, 0
distance = [0,0,0]

frame = cv2.imread('frc2013.png')

r = 720.0 / frame.shape[1]
dim = (720, int(frame.shape[0] * r))
frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

blur = cv2.GaussianBlur(frame,(3,3),0)

hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

lower_color = np.array([H-25,S-25,V-25])
upper_color = np.array([H+25,S+25,V+25])

mask = cv2.inRange(hsv, lower_color, upper_color)

edges = cv2.Canny(mask,0,100)

cnt,hierarchy = cv2.findContours(edges, 1, 2)

for a in cnt:
      epsilon = 0.05*cv2.arcLength(a,True)
      approx = cv2.approxPolyDP(a,epsilon,True)
      if(cv2.contourArea(approx) > 2000):
         x,y,w,h = cv2.boundingRect(approx)
         if(abs(oldX-x) > 5 or abs(oldY-y) > 5):
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)
            oldX, oldY = x, y
            goalCount += 1
            print 'Goal #',goalCount,x+w/2,y+h/2
            cv2.circle(frame, (x+w/2,y+h/2), 2, (0,255,0),1)
            cv2.putText(frame,str(x+w/2)+","+str(y+h/2), (x+w/2,y+h/2), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255))
            distance[goalCount-1]=(1.5748/w)*720*1/2*math.tan(math.radians(35))
         
print goalCount
print distance

cv2.imshow('Goruntu', frame)

k = cv2.waitKey(0) & 0xFF
if k == 27:
   cv2.destroyAllWindows()