import subprocess

proc = subprocess.Popen("./passCpp",
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE)

s1 = bytearray(10)   

s1[0] = 65 #A
s1[1] = 66 #B
s1[2] = 67 #C
s1[3] = 68 #D
s1[4] = 69 #E
s1[5] = 70 #F
s1[6] = 71 #G
s1[7] = 72 #H
s1[8] = 73 #I

t = memoryview(s1)       
print("1")
proc.stdin.write(t)
print("2")
message = proc.stdout.read(3)
print("return message ->" + message + " written by python \n" )
proc.stdin.write('q')
proc.wait()