import base64
import re
from Crypto.Cipher import AES
from Crypto.Hash import MD5


# this is the python of the script "cracking-a-mobile-app-pin.java" of this repository 


enc="G38zckAufW4B9A6sywz28kzgW8CCx1UWugLUTjKlo/kwV1CVesmr0tPX/JZOW0aik0TlkrcAIZZ/G0BigUtmeg=="
key0="PD09PSBQM250M3N0M3JMNGIgPT09Pg=="

uuid=re.compile('.*-.*-.*-.*-')

key1 = base64.b64decode(key0).decode("utf-8") 
abyte= base64.b64decode(enc)
iv   = abyte[0:16]
data = abyte[16:]


for x in range(0,9999):
	pin="%04d" % x
	h=MD5.new()
	h.update(key1.encode())
	h.update(pin.encode())
	key= h.digest()[0:16]
	try:
		cipher = AES.new(key, AES.MODE_CBC, iv)
		clear = cipher.decrypt(data)
		if uuid.match(str(clear)):
			print(clear)
	except Exception as err:
		pass 
