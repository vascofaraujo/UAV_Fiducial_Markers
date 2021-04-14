import os
  
  
# Path
path = "./mypipe"
  
# Mode of the FIFO (a named pipe)
# to be created
mode = 0o600
  
# Create a FIFO named path
# with the specified mode
# using os.mkfifo() method
os.mkfifo(path, mode)
    
print("FIFO named '% s' is created successfully." % path)
