import requests

url = "https://www.fast2sms.com/dev/bulkV2"

payload = "sender_id=fast2sms&message=This is a test message&route=v3&numbers=8110949621"
headers = {
    'authorization': "7pkqtSf9ZduLM35A8oHEiNQwVblhJ4KX6PRngYacvW0FmGCByUXCMgnrGjESN7iQUewJ2VFA4tazlxqY",
    'Content-Type': "application/x-www-form-urlencoded",
    'Cache-Control': "no-cache",
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)