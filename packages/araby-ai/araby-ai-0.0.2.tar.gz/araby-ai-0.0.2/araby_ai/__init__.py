from .writenow import *
import requests

class Client:
	def __init__(self, email, password):
		headers = {
			"authority": "v1.prd.socket.araby.ai",
			"accept": "application/json, text/plain, */*",
			"accept-language": "ar-AE,ar;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6",
			"content-type": "application/x-www-form-urlencoded;charset=UTF-8",
			"lang": "ar",
			"origin": "https://araby.ai",
			"referer": "https://araby.ai/",
			"sec-fetch-dest": "empty",
			"sec-fetch-mode": "cors",
			"sec-fetch-site": "same-site",
			"user-agent": "Mozilla/5.0 (Linux; Android 13; SM-A225F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36"}
		data = {"email": email, "password": password}
		response = requests.post("https://v1.prd.socket.araby.ai/login", headers=headers, data=data).json()
		self.client = response["token"]