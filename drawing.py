import cv2 as cv



img = cv.imread("img_expo.JPG")
scale_percent = 30 # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)   
img = cv.resize(img, dim)


res = res = cv.xphoto.oilPainting(img, 7, 1)


cv.imshow("hane", res)

while True:
    if cv.waitKey(1) & 0xFF == ord('q'):
        cv.destroyAllWindows()
        break