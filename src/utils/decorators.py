def try_wrapper(err_msg: str = None):
	def try_deco(func):
		def wrapper(*args, **kwargs):
			try:
				return func(*args, **kwargs)
			except Exception as err:
				print(err_msg.format(*args, **kwargs, error_message=str(err)) if err_msg else err)
	
		return wrapper
	return try_deco