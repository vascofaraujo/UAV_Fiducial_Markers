import cppyy


cppyy.include('zlib.h')
cppyy.load_library('libz')
cppyy.gbl.zlibVersion()

print("hello")