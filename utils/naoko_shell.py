from os import popen

def shell(content):
	return popen(content).read()