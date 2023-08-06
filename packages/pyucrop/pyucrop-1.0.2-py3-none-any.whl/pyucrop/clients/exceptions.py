class Bad_Request(Exception):
	def __init__(self, *args):
		if args:
			self.message = args[0]
		else:
			self.message = None

	def __str__(self):
		return '<Code 400> Request is malformed or incomplete, non exhaustive causes can be:\n- Missing image_file in request\n- Input image format is not valid\n- Image resolution is too big'

class Unauthorized(Exception):
	def __init__(self, *args):
		if args:
			self.message = args[0]
		else:
			self.message = None

	def __str__(self):
		return '<Code 401> Missing api key.'

class Payment_Required(Exception):
	def __init__(self, *args):
		if args:
			self.message = args[0]
		else:
			self.message = None

	def __str__(self):
		return '<Code 402> Your account has no remaining credits, you can buy more in your account page.'

class Forbidden(Exception):
	def __init__(self, *args):
		if args:
			self.message = args[0]
		else:
			self.message = None

	def __str__(self):
		return '<Code 403> Invalid or revocated api key.'

class Not_Acceptable(Exception):
	def __init__(self, *args):
		if args:
			self.message = args[0]
		else:
			self.message = None

	def __str__(self):
		return '<Code 406> Accept header not acceptable.'

class TooManyRequests(Exception):
	def __init__(self, *args):
		if args:
			self.message = args[0]
		else:
			self.message = None

	def __str__(self):
		return '<Code 429> Too many requests, blocked by the rate limiter.'

class InternalServerError(Exception):
	def __init__(self, *args):
		if args:
			self.message = args[0]
		else:
			self.message = None

	def __str__(self):
		return '<Code 500> This may be a bug on our side.'

class UnprocessableEntity(Exception):
	def __init__(self, *args):
		if args:
			self.message = args[0]
		else:
			self.message = None

	def __str__(self):
		return '<Code 422> the content of the request does not comply with the application rules.'

def check_exceptions(code=0):
	code = int(code)
	if code == 400:
		raise Bad_Request()
	if code == 401:
		raise Unauthorized()
	if code == 402:
		raise Payment_Required()
	if code == 403:
		raise Forbidden()
	if code == 406:
		raise Not_Acceptable()
	if code == 429:
		raise TooManyRequests()
	if code == 500:
		raise InternalServerError()
	if code == 422:
		raise UnprocessableEntity()