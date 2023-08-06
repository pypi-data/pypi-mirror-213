import requests, random, re


class sign_up:
	def create_account():
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
		email = requests.post("https://api.internal.temp-mail.io/api/v3/email/new").json()["email"]
		rand = random.randrange(999)
		password = f"Mhmd@{rand}"
		data = {"email": email, "password": password}
		response = requests.post("https://v1.prd.socket.araby.ai/register", headers=headers, data=data)
		while True:
			check = requests.get(f"https://api.internal.temp-mail.io/api/v3/email/{email}/messages").json()
			if check:
				verify = re.findall(r'( (.*?) )', check[0]["body_text"])
				requests.get(verify[21][1])
				break
		return data