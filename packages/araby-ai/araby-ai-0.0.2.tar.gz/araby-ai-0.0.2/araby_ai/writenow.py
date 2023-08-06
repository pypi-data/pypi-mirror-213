import requests

class long_documents:
	def __init__(self, client):
		self.client = client.client
	def AnalogyGenerator(self, language, text, number):
		headers = {
			"authority": "v1.prd.socket.araby.ai",
			"accept": "*/*",
			"accept-language": "ar-AE,ar;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6",
			"authorization": self.client,
			"content-type": "application/json",
			"origin": "https://dashboard.araby.ai",
			"sec-fetch-dest": "empty",
			"sec-fetch-mode": "cors",
			"sec-fetch-site": "same-site",
			"user-agent": "Mozilla/5.0 (Linux; Android 13; SM-A225F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36"}
		json_data = {
			"useCase": "AnalogyGenerator",
			"tone": "",
			"language": language,
			"inputs": [
						{
									"phrase": text,
						},
			],
			"number": int(number)}
		response = requests.post("https://v1.prd.socket.araby.ai/generate-text", headers=headers, json=json_data)
		return response.json()
	def Article(self, language, text, number):
		headers = {
			"authority": "v1.prd.socket.araby.ai",
			"accept": "*/*",
			"accept-language": "ar-AE,ar;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6",
			"authorization": self.client,
			"content-type": "application/json",
			"origin": "https://dashboard.araby.ai",
			"sec-fetch-dest": "empty",
			"sec-fetch-mode": "cors",
			"sec-fetch-site": "same-site",
			"user-agent": "Mozilla/5.0 (Linux; Android 13; SM-A225F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36"}
		json_data = {
			"useCase": "Article",
			"tone": "Casual",
			"language": language,
			"inputs": [
						{
									"topic": text,
						},
			],
			"number": int(number)}
		response = requests.post("https://v1.prd.socket.araby.ai/generate-text", headers=headers, json=json_data)
		return response.json()
	def BlogBody(self, language, text, number):
		headers = {
			"authority": "v1.prd.socket.araby.ai",
			"accept": "*/*",
			"accept-language": "ar-AE,ar;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6",
			"authorization": self.client,
			"content-type": "application/json",
			"origin": "https://dashboard.araby.ai",
			"sec-fetch-dest": "empty",
			"sec-fetch-mode": "cors",
			"sec-fetch-site": "same-site",
			"user-agent": "Mozilla/5.0 (Linux; Android 13; SM-A225F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36"}
		json_data = {
			"useCase": "BlogBody",
			"tone": "",
			"language": language,
			"inputs": [
						{
									"keywords": text,
						},
			],
			"number": int(number)}
		response = requests.post("https://v1.prd.socket.araby.ai/generate-text", headers=headers, json=json_data)
		return response.json()
		