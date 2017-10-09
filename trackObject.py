import cv2
import numpy as np

H, S, V = 76/2, 53*255/100, 60*255/100

cap = cv2.VideoCapture(0)

while True:
   _, frame = cap.read()
   
   r = 720.0 / frame.shape[1]
   dim = (720, int(frame.shape[0] * r))
   frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

   # blur the content
   blur = cv2.GaussianBlur(frame,(3,3),0)

   # Convert BGR to HSV
   hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

   # define range of blue color in HSV - !!! [Calibration must be done here!]
   lower_color = np.array([H-25,S-25,V-25])
   upper_color = np.array([H+25,S+25,V+25])

   # Threshold the HSV image to get only blue colors
   mask = cv2.inRange(hsv, lower_color, upper_color)
   
   # Detect edges
   edges = cv2.Canny(mask,100,200)

   cnt,hierarchy = cv2.findContours(edges, 1, 2)
   
   if cnt != []:
      max, maxArea = [], 0
      for a in cnt:
         if(cv2.contourArea(a)>maxArea):
            maxArea = cv2.contourArea(a)
            max = a
      if(max != []):
         (x,y),radius = cv2.minEnclosingCircle(max)
         center = (int(x),int(y))
         radius = int(radius)
         cv2.circle(frame,center,radius,(0,255,0),2)
         print x, y

   # Display the resulting frame
   cv2.imshow('frame',frame)
   if cv2.waitKey(1) & 0xFF == ord('q'):
     break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

