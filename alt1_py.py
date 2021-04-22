import os
import cv2 as cv
import numpy as np
import sys


if __name__ == "__main__":

    IPC_FIFO_NAME = "pipe1"

    fifo = os.open(IPC_FIFO_NAME, os.O_WRONLY)
    print("Hello from Python\n")
    try:
        img = cv.imread("AR6.jpeg")
        cv.imshow("Janela Python", img)
        
        os.write(fifo, bytes(str(img), 'utf8'))
        cv.waitKey(0)
        #if cv.waitKey(1) & 0xFF == ord('q'):
            #break


    except KeyboardInterrupt:
        print("\nGoodbye!")
    finally:
        os.close(fifo)
        print("Bye from Python\n")
        print("Exiting...\n")
