import cv2 as cv


img = cv.imread("C:/totalcmd/35mm/003/F1000001.JPG")

img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

th, img = cv.threshold(img, 128, 255, cv.THRESH_OTSU) 

th, img = cv.threshold(img,127,255,cv.THRESH_BINARY_INV)


cv.imshow("img", img)

cv.waitKey(0)

cv.imwrite('C:/totalcmd/IST/MESTRADO/Website/uploads/binarize.png',img)