import cv2 as cv
import sys

img = cv.imread("AR6.jpeg")

sys.stdout.buffer.write(img.tostring())