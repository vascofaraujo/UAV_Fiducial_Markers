import os
import cv2

fifo_name = 'fifo'

def main():
    data = cv2.imread('AR6.jpeg').tobytes()    
    try:
        os.mkfifo(fifo_name)
    except FileExistsError:
        pass
    with open(fifo_name, 'wb') as f:
        print(data)
        f.write('{}\n'.format(len(data)).encode())
        f.write(data)
    
    print("Final")

if __name__ == '__main__':
    main()