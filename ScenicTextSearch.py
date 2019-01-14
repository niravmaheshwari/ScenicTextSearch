#import required libraries
import cv2

from imutils.object_detection import non_max_suppression

import numpy as np

import pytesseract

from googlesearch import search

import webbrowser

#read the image using opencv
img=cv2.imread('images/1.jpg')
#make a copy of the input image
orig=img.copy()


#layers name to the last 2 output layers of EAST model
layerNames = [
	"feature_fusion/Conv_7/Sigmoid",
	"feature_fusion/concat_3"]

#load the EAST text detector model from the .pb file
net=cv2.dnn.readNet('frozen_east_text_detection.pb')

#resize the image
(origH, origW) = img.shape[:2]
# set the new width and height and then determine the ratio in change
# for both the width and height
(newW, newH) = (320,320)
rW = origW / float(newW)
rH = origH / float(newH)
 
# resize the image and grab the new image dimensions
img = cv2.resize(img, (newW, newH))
(H, W) = img.shape[:2]

#define a function to threshhold the detected boxes
def decode_boxes(scores,geometry):
    
    #extract the number of rows and columns
    (numRows, numCols) = scores.shape[2:4]
    
    #initialize the rectangles and cofidences
    rectangles=[]
    confidences=[]
    
    #loop over the number of rows
    for y in range(0,numRows):
        
        #extract the scores
        scoresdata=scores[0,0,y]
        
        #extract the coordinates
        x0=geometry[0,0,y]
        x1=geometry[0,1,y]
        x2=geometry[0,2,y]
        x3=geometry[0,3,y]
        angles=geometry[0,4,y]
        
        #loop over the number of columns
        for x in range(0,numCols):
            
            #reject the boxes with score less than the threshold confidence
            if scoresdata[x]<0.5:
                continue
            
            #multiply the values of x and y by 4 as the EAST model reduce the size of input by a factor of 4
            X=x*4.0
            Y=y*4.0
            
            #calculate the sin and cosine of rotation angle
            angle=angles[x]
            cos=np.cos(angle)
            sin=np.sin(angle)
            
            #compute the height and width of the bounding box
            h=x0[x]+x2[x]
            w=x1[x]+x3[x]
            
            #compute the box coordinates using X,Y and the sin and cosines of the angle of rotation
            endX = int(X + (cos * x1[x]) + (sin * x2[x]))
            endY = int(Y - (sin * x1[x]) + (cos * x2[x]))
            startX = int(endX - w)
            startY = int(endY - h)
            
            #append the bounding box coordinates and probability score
            rectangles.append((startX,startY,endX,endY))
            confidences.append(scoresdata[x])
            
    
    return (rectangles,confidences)


#contruct a blob from input image and then do a forward pass to obtain the two output layers of the model
#it does mean subtraction,scaling and optionally channel swapping
blob = cv2.dnn.blobFromImage(img, 1.0, (W, H),
	(123.68, 116.78, 103.94), swapRB=True, crop=False)

net.setInput(blob)

(scores, geometry) = net.forward(layerNames)

#decoding the predictions made by the model
(rectangles,confidences)=decode_boxes(scores,geometry)
        
#perform non max suppression to suppress all the not needed boxes
boxes=non_max_suppression(np.array(rectangles),probs=confidences)

#initialize the results
results=[]

#loop over the bounding boxes
for (startX,startY,endX,endY) in boxes:
    
    #scaling the bounding box
    startX=int(startX*rW)
    startY=int(startY*rH)
    endX=int(endX*rW)
    endY=int(endY*rH)
    
    #calculate the padding for the boxes and the user can change the padding level accordingly
    dX=int((endX-startX)*0.05)
    dY=int((endY-startY)*0.05)
    
    #apply padding to image
    startX=max(0,startX-dX)
    startY=max(0,startY-dY)
    endX=min(origW,endX+2*dX)
    endY=min(origH,endY+2*dY)
    
    #extract the padded block
    paddedimage=orig[startY:endY,startX:endX]
    
    #apply tesseract V4 to the OCR
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
    config = ("-l eng --oem 1 --psm 7")
    text = pytesseract.image_to_string(paddedimage, config=config)
    
    #apend the results
    results.append(((startX,startY,endX,endY),text))
    
    
results = sorted(results, key=lambda r:r[0][1])

output = orig.copy()
# loop over the results
for ((startX, startY, endX, endY), text) in results:
	# display the text OCR'd by Tesseract
	print("{}\n".format(text))
 
	# strip out non-ASCII text so we can draw the text on the image
	# using OpenCV, then draw the text and a bounding box surrounding
	# the text region of the input image
	text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
	
	cv2.rectangle(output, (startX, startY), (endX, endY),
		(0, 0, 255), 2)
	cv2.putText(output, text, (startX, startY - 20),
		cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
 
	# show the output image
cv2.imshow("Text Detection", output)


#append the string together
string=str(object='')
for ((startX, startY, endX, endY), text) in results:
    string=string + ' ' + text
    
#search for the string on google and display it on the python terminal
for j in search(string, tld='co.in', lang='en', num=10, start=0, stop=1, pause=1.0, only_standard=False):
    print(j+'\n')
    
#run this code to open the results page
url = "https://www.google.com.tr/search?q={}".format(string)
webbrowser.open_new(url)






    
    
    

    
 



    
