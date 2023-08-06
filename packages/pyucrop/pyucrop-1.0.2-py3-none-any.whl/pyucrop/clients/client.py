import requests
from .exceptions import check_exceptions

class Client:
	def __init__(self, key):
		self.headers = {
			'x-api-key': key
		}

	def text_to_image(self, text, name_image):
		responce = requests.post('https://clipdrop-api.co/text-to-image/v1',
		  files = {
		      'prompt': (None, f'{text}', 'text/plain')
		  },
		  headers = self.headers
		)
		if responce.status_code == 200:
			try:
				with open(f"{name_image}", 'wb') as file:
					file.write(responce.content)
				return True
			except:
				return False
		else:
		 check_exceptions(code=responce.status_code)

	def remove_text(self, image, name_image):
		image_file_path = f'{image}'
		image_file = open(image_file_path, 'rb')

		responce = requests.post('https://clipdrop-api.co/remove-text/v1',
		  files = {
		    'image_file': (f'{image}', image_file, 'image/jpeg')
		    },
		  headers = self.headers
		)
		if responce.status_code == 200:
			try:
				with open(f"{name_image}", 'wb') as file:
					file.write(responce.content)
				return True
			except:
				return False
		else:
		  check_exceptions(code=responce.status_code)

	def upscale(self, image, name_image, scale: int = 2):
		image_file_path = f'{image}'
		image_file = open(image_file_path, 'rb')
		responce = requests.post('https://clipdrop-api.co/super-resolution/v1',
			files = {
				'image_file': (f'{image}', image_file, 'image/jpeg')
			},
				data = { 'upscale': int(scale) },
				headers = self.headers
			)
		if responce.status_code == 200:
			try:
				with open(f"{name_image}", 'wb') as file:
					file.write(responce.content)
				return True
			except:
				return False
		else:
			check_exceptions(code=responce.status_code)

	def remove_bg(self, image, name_image):
		image_file_path = f'{image}'
		image_file = open(image_file_path, 'rb')
		responce = requests.post('https://clipdrop-api.co/remove-background/v1',
		  files = {
		    'image_file': (f'{image}', image_file, 'image/jpeg'),
		    },
		  headers = self.headers
		)
		if responce.status_code == 200:
			try:
				with open(f"{name_image}", 'wb') as file:
					file.write(responce.content)
				return True
			except:
				return False
		else:
		  check_exceptions(code=responce.status_code)
