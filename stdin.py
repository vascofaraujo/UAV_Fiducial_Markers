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
file2write=open("filename",'w')


#while(True):
stdout = sys.stdin.readlines()
      
file2write.write(str(stdout))

#stdout = sys.stdin.read()
#file2write.write(str(stdout))
#    stdout = ""


#stdout = sp.check_output("dir")

file2write.close()

