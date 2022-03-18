import requests

def send_complex_message():
    return requests.post(
        "https://api.mailgun.net/v3/sandbox21350be7856646358b7c51226953c2d7.mailgun.org/messages",
        auth=("api", "4493bee0acba36a334957edf6d204f17-c3d1d1eb-71ae2c6d"),
        
        data={"from": "User <mailgun@sandbox21350be7856646358b7c51226953c2d7.mailgun.org>",
              "to": ["yournews@sandbox21350be7856646358b7c51226953c2d7.mailgun.org"],
              "subject": "Your news letter",
              "text": "Testing some Mailgun awesomness!",
              "html": "<html><body><h1>Hi</h1></body></html>"})

def send_simple_message():
	return requests.post(
		"https://api.mailgun.net/v3/sandbox21350be7856646358b7c51226953c2d7.mailgun.org/messages",
		auth=("api", "4493bee0acba36a334957edf6d204f17-c3d1d1eb-71ae2c6d"),
		data={"from": "Excited User <mailgun@sandbox21350be7856646358b7c51226953c2d7.mailgun.org>",
			"to": ["shanki4games@gmail.com"],
			"subject": "Hello",
			"text": "Testing some Mailgun awesomness!"})
send_complex_message()
#send_simple_message()
print(send_complex_message())
#print(send_simple_message())