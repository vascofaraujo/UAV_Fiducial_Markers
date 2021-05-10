import os
import sys
import binascii
import struct


FIFO = 'myfifo'

if os.path.exists(FIFO): #Caso o named pipe já exista
	os.remove(FIFO)
os.mkfifo(FIFO)


while True:
    with open(FIFO) as fifo:
        for line in fifo:
        	print("---NEW LINE---")
        	#print(line)
        	siz =sys.getsizeof(line)
        	info = line.strip().strip('\x00')
        	str(info)
        	#print(info)
        	#print(type(info))

        	if not info:
        		print("Empty Line")
        		print("---END OF CYCLE---")
        		continue
        	num = float(info)
        	print("number read in Python: ")
        	print(num)
        	#print(type(num))
        	print("---END OF CYCLE---")
