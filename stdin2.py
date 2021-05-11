"""
import sys

print("hello")
line = input("hw")
print(f'Processing Message from sys.stdin *****{line}*****')
print("Done")
"""

import sys
import pickle
import fileinput

#for line in fileinput.input():
#    stdout = line
def read():



    stdout = sys.stdin.read()
        
    with open("filename", "a") as myfile:
        myfile.write(str(stdout))
        myfile.write("aaaaaaaaaa")

    #file2write.write(str(stdout))
    #file2write.write("hellout")
    return



read()


