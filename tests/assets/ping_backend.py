import time

import requests

while True:
    try:
        result = requests.get("http://0.0.0.0:3000")
        print(result)
        if result.status_code == 200:
            break
    except Exception as exc:
        print("Exception: ", exc)
    time.sleep(3)
