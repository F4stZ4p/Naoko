from datetime import datetime

def log(object: str):
	return print(f'{datetime.utcnow()}: {object}')

def superlog(object: str, additional: str):
	return print(f'{datetime.utcnow()}: {object} ({additional})')