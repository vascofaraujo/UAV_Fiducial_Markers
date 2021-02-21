import cv2 as cv
import sys
import numpy as np
from operator import itemgetter, attrgetter
import cv2.aruco as aruco




#function that calculates the sum of angles of a 4 line object
def quad_sum(cnt):
    sum_angles = 0

    p1 = np.array([cnt[0][0], cnt[0][1]])
    p2 = np.array([cnt[1][0], cnt[1][1]])
    p3 = np.array([cnt[2][0], cnt[2][1]])
    p4 = np.array([cnt[3][0], cnt[3][1]])

    p12 = p1-p2
    p23 = p2-p3
    p34 = p3-p4
    p41 = p4-p1

    cosine_angle1 = np.dot(p12, p23) / (np.linalg.norm(p12) * np.linalg.norm(p23))
    angle1 = np.degrees(np.arccos(cosine_angle1))

    cosine_angle2 = np.dot(p23, p34) / (np.linalg.norm(p23) * np.linalg.norm(p34))
    angle2 = np.degrees(np.arccos(cosine_angle2))

    cosine_angle3 = np.dot(p34, p41) / (np.linalg.norm(p34) * np.linalg.norm(p41))
    angle3 = np.degrees(np.arccos(cosine_angle3))

    cosine_angle4 = np.dot(p41, p12) / (np.linalg.norm(p41) * np.linalg.norm(p12))
    angle4 = np.degrees(np.arccos(cosine_angle4))

    sum_angles = angle1+angle2+angle3+angle4
    return sum_angles


#function that performs non-maximum supression
def non_max_supression(boxes, overlapThresh):
    i = len(boxes)-1

    if i > 1:
        while i > 0:	
            last = i - 1

            areaLast = boxes[last][4]
            areaNew = boxes[i][4]

            overlap = np.minimum(areaNew/areaLast, areaLast/areaNew)

            if overlap > overlapThresh:
                del boxes[i]

            i = i-1

    return boxes

#function that checks if there are three shapes in a row
def match_templates(patches):
    findMatch = 0
    for i in range(len(patches)-1):
        nextI = i+1
        patch = cv.cvtColor(patches[i], cv.COLOR_BGR2GRAY)
        patchNext = cv.cvtColor(patches[nextI], cv.COLOR_BGR2GRAY)
        try:
            match = cv.matchTemplate(patchNext, patch, cv.TM_CCOEFF_NORMED)
            if (len(match) != 0):
                print("FIND")
                findMatch = findMatch+1
            else:
                findMatch = 0
                print("NOT")
            if findMatch == 1:#it should be number of objects-1
                cv.imshow("a", patch)
                cv.imshow("b", patchNext)
                return 1, i, 
        except:
            print("An exception ocurred")
    return 0, 0	

def match_warped(squares):
    markers = []
    k = 0
    for i in range(len(squares)):
        contours = squares[i][6]
        for cnt in contours:
            cnt_len = cv.arcLength(cnt, True)
            cnt = cv.approxPolyDP(cnt, 0.02*cnt_len, True)
            
            if len(cnt) == 4 and cv.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)       

                    sumAngles = quad_sum(cnt)
                    if sumAngles != 360:
                        continue

                    x,y,w,h = cv.boundingRect(cnt)   

                    if x<0.2*squares[i][5].shape[0] or y<0.2*squares[i][5].shape[1]:
                        continue


                    draw = np.zeros((squares[i][5].shape[0], squares[i][5].shape[1], 3), dtype=np.uint8)
                    cv.rectangle(squares[i][5], (x,y), (x+w,y+h), (0,255,0),1)

                    patch = squares[i][5][x:x+w, y:y+h]
                    cv.imshow("path",patch)
                    cv.imshow("desenh", draw)
                    cv.imshow("waq", squares[i][5])
                    contoursT, hie = cv.findContours(patch, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
                    for cntT in contoursT:
                        cntT_len = cv.arcLength(cntT, True)
                        cntT = cv.approxPolyDP(cntT, 0.02*cntT_len, True)
                        if len(cntT) == 3:# and cv.countourArea(cnt) > 200:
                            markers.append(squares[i])

                    
        k = k+1
    return markers
def order_points(pts):
	# initialzie a list of coordinates that will be ordered
	# such that the first entry in the list is the top-left,
	# the second entry is the top-right, the third is the
	# bottom-right, and the fourth is the bottom-left
	rect = np.zeros((4, 2), dtype = "float32")
	# the top-left point will have the smallest sum, whereas
	# the bottom-right point will have the largest sum
	s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]
	# now, compute the difference between the points, the
	# top-right point will have the smallest difference,
	# whereas the bottom-left will have the largest difference
	diff = np.diff(pts, axis = 1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]
	# return the ordered coordinates
	return rect


def four_point_transform(image, pts):
	# obtain a consistent order of the points and unpack them
	# individually
	rect = order_points(pts)
	(tl, tr, br, bl) = rect
	# compute the width of the new image, which will be the
	# maximum distance between bottom-right and bottom-left
	# x-coordiates or the top-right and top-left x-coordinates
	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxWidth = max(int(widthA), int(widthB))
	# compute the height of the new image, which will be the
	# maximum distance between the top-right and bottom-right
	# y-coordinates or the top-left and bottom-left y-coordinates
	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	maxHeight = max(int(heightA), int(heightB))
	# now that we have the dimensions of the new image, construct
	# the set of destination points to obtain a "birds eye view",
	# (i.e. top-down view) of the image, again specifying points
	# in the top-left, top-right, bottom-right, and bottom-left
	# order
	dst = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype = "float32")
	# compute the perspective transform matrix and then apply it
	M = cv.getPerspectiveTransform(rect, dst)
	warped = cv.warpPerspective(image, M, (maxWidth, maxHeight))
	# return the warped image
	return warped

#####################################################################

#Começar a captura
cap = cv.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
cap.set(10, 100)

#parameters initialization
sucess, img = cap.read()
minPerimeterRate = 0.03
maxPerimeterRate = 4
minCornerDistanceRate = 0.05
minPerimeterPixels = minPerimeterRate * np.maximum(img.shape[0], img.shape[1])
maxPerimeterPixels = maxPerimeterRate * np.maximum(img.shape[0], img.shape[1])
parameters = aruco.DetectorParameters_create() ##S
minDistanceToBorder = parameters.minDistanceToBorder
minDistSq = np.maximum(img.shape[0], img.shape[1]) * np.maximum(img.shape[0], img.shape[1])


while True:
    success, img = cap.read()

    """
    #resize imagem
    scale_percent = 50 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)   
    img = cv.resize(img, dim)
    """

    #grayscale
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) 

    #canny
    canny = cv.Canny(gray, 255/3, 255)

    #dillation
    #kernel = np.ones((3,3),np.uint8)
    #canny = cv.dilate(canny,kernel,iterations = 1)

    
    #countours
    contours, hierarchy = cv.findContours(canny, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    
    # Draw contours
    drawing = np.zeros((canny.shape[0], canny.shape[1], 3), dtype=np.uint8)
    for i in range(len(contours)):
        color = (0, 255, 0)
        cv.drawContours(drawing, contours, i, color, 1, cv.LINE_8, hierarchy, 0)
    # Show in a window
    cv.imshow('Contours', drawing)

    
    
    squares = []
    triangles = []
    angle = 0
    for cnt in contours:
        cnt_len = cv.arcLength(cnt, True)
        cnt = cv.approxPolyDP(cnt, 0.02*cnt_len, True)
        if len(cnt) == 4  and cv.contourArea(cnt)>200 and cv.isContourConvex(cnt):
            cnt = cnt.reshape(-1, 2)          
            approxCurve = cnt
            sum_angles = quad_sum(cnt)
            minCornerDistancePixels = len(cnt) * minCornerDistanceRate
           
            for j in range(0,4):
                print(j, (j+1)%4)
                d = (approxCurve[j][0] - approxCurve[(j + 1)%4][0]) * (approxCurve[j][0] - approxCurve[(j + 1)%4][0]) + (approxCurve[j][1] - approxCurve[(j + 1)%4][1]) * (approxCurve[j][1] - approxCurve[(j + 1)%4][1])
                minDistSq = min(minDistSq, d)

            if sum_angles == 360 and minDistSq >= minCornerDistancePixels * minCornerDistancePixels:
                tooNearBorder = False
                for j in range(4):
                    if(approxCurve[j][0] < minDistanceToBorder or approxCurve[j][1] < minDistanceToBorder or approxCurve[j][0] > canny.shape[0] - 1 - minDistanceToBorder or approxCurve[j][1] > canny.shape[1] - 1 - minDistanceToBorder): 
                        tooNearBorder = True

                if(tooNearBorder): continue
                x,y,w,h = cv.boundingRect(cnt)
                area = cv.contourArea(cnt)
                

                candidate_corner = []
                warped =[]
                for j in range(4):
                    candidate_corner.append([approxCurve[j][0], approxCurve[j][1]])
                print("CANDIDATE CORN")
                
                candidate_corner = np.array(candidate_corner)
                candidate_corner = order_points(candidate_corner)
                warped = four_point_transform(gray, candidate_corner)
                _, warped = cv.threshold(warped, 125, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
                drawing3 = np.zeros((warped.shape[0], warped.shape[1], 3), dtype=np.uint8)
                contour_warped, _ = cv.findContours(warped, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)          

                a = (x,y,w,h, area, warped, contour_warped)
                squares.append(a)
                for k in range(len(contour_warped)):
                    #contour_len_warped = cv.arcLength(contour_warped[k], True)
                    #approx_Curve_warped = cv.approxPolyDP(contour_warped[k], (float)((contour_len_warped) * parameters.polygonalApproxAccuracyRate), True)
                    #if len(approx_Curve_warped) == 3 and cv.isContourConvex(approx_Curve_warped):
                    cv.drawContours(drawing3, contour_warped, k, color, 1, cv.LINE_8)

                cv.imshow("draw3", drawing3)

                #k = cv.waitKey(0)
                #cv.destroyWindow('draw3')
        """
        if len(cnt) == 3:# and cv.countourArea(cnt) > 200:
            xt,yt,wt,ht = cv.boundingRect(cnt)
            areat = cv.contourArea(cnt)
            b = (xt,yt,wt,ht, areat)
            triangles.append(b)
        """

    #sorts every square and triangle, from smaller to bigger
    squares = sorted(squares, key=itemgetter(4))
    #triangles = sorted(triangles, key=itemgetter(4))

    #performs non maximum supression
    squares = non_max_supression(squares, 0.5)
    #triangles = non_max_supression(triangles, 0.5)

    markers = match_warped(squares)

    """
    #join squares and triangles and orders them
    shapes = []
    shapes = squares #+ triangles
    shapes = sorted(shapes, key=itemgetter(4))

    
    #now, to find the marker (triangle inside square inside square)
    i = len(shapes)-1
    patch = []
    while(i >= 0):
        patch.append(img[(shapes[i][1]):(shapes[i][1]+shapes[i][3]), (shapes[i][0]):(shapes[i][0]+shapes[i][2])])
        i=i-1

    res, idx = match_templates(patch)

    if res == 1:#finds marker
        x1 = shapes[i][0]
        y1 = shapes[i][1]
        w = shapes[i][2]
        h = shapes[i][3]

        cv.rectangle(img, (x1,y1), (x1+w,y1+h), (0,255,0),10)
    """
    for i in range(len(markers)):
        x1 = markers[i][0]
        y1 = markers[i][1]
        w = markers[i][2]
        h = markers[i][3]
        cv.rectangle(img, (x1,y1), (x1+w,y1+h), (0,255,0),10)

    cv.imshow("window", img)

    


    #Quebrar se 'q' for premido
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

