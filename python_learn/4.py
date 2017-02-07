import functools
import os

def gwlog(func):
		def wrapper(*args, **kw):
				print('begin call')
				return func(*args, **kw),print('end call')
		return wrapper
		
@gwlog		
def gtest():
		print('call gtest it')		

gtest()

os.system("pause")