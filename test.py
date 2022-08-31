

import requests
r = requests.get("https://sun9-1.userapi.com/c9591/u00001/136592355/z_a8fd75ba.jpg")
with open('1.jpg', 'wb') as f:
    f.write(r.content)