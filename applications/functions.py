import os, uuid

def new_name_image(file):
	if hasattr(file, 'name'):
		ext = file.name.split(".")[-1]
		file.name = f"{uuid.uuid4()}.{ext}"
	else:
		ext = file.split(".")[-1]
		file = f"{uuid.uuid4()}.{ext}"
	return file

