import os
import re
import time
import json
import random
import requests
from fake_useragent import UserAgent
import random, string

class tempmail:
    def __init__(self):
        self.ses = requests.session()
        self.url = "https://api.mail.tm"
        self.password = "malboloro"
    
    def getRandomName(self):
        print("# Lynph, generating new email address !")
        name = "".join([random.choice(list("qwertyuiopasdfghjklzxcvbnm")) for _ in range(12)])
        return name

    def createEmail(self):
        front = self.getRandomName()
        vmail = front+"@midiharmonica.com"
        print("# new email address",vmail)
        data = {"address": vmail,"password": self.password}
        req = self.ses.post(self.url + "/accounts",json=data)
        if "This value is already used" in req.text:
            print("# email address already used !")
            print("- " * 25)
            self.createEmail()
        print("# success create email address !")
        return vmail

    def getToken(self,email):
        data = {"address":email,"password":self.password}
        req = self.ses.post(self.url + "/token",json=data)
        if "message" in req.text:
            print(f"# error : {req.json()['message']}")
            exit()
        return req.json()["token"]

    def getMessage(self,token):
        self.ses.headers.update({"Authorization":f"Bearer {token}"})
        while True:
            print("# waiting new email ..",flush=True,end='\r')
            req = self.ses.get(self.url + "/messages")
            if len(req.json()["hydra:member"]) != 0:
                print("# new email detected !")
                return req.json()["hydra:member"][0]["id"]

    def getDetailMessage(self,messageID):
        req = self.ses.get(self.url + "/messages/" + messageID).json()
        return req["text"]
        

class createAccount:
	def __init__(self):
		self.ses = requests.Session()
		self.url = "https://windscribe.com/signup"
		self.ua = UserAgent()

	def generate_username(self):
		req = requests.post(self.url,data={"generate_username":1}).json()
		return req['data']['username']
        
    

	def create(self,email):
		self.username = self.generate_username()
		self.headers = {"user-agent":self.ua.random}
		data = {
			"signup":"1",
			"username":self.username,
			"password": self.username,
			"password2": self.username,
			"email":email,
			"voucher_code":"",
			"captcha":"",
			"robert_status":"1",
			"unlimited_plan":"0"
			}
		req = requests.post(self.url,data=data,headers=self.headers).json()
		if 'session_auth_hash' in json.dumps(req):
			print("# register successfully !")
			open("account.txt","a+").write(f"Your Login: {imel} | Your Password: {self.username}\n")
			self.sesauth = req['data']['session_auth_hash']
			self.coco = {'ws_session_auth_hash':self.sesauth}
			exit() 
		elif "error" in json.dumps(req):
			print("# error ",req['errorMessage'])
			exit()
		else:
			print(req)

try:
	os.system("cls" if os.name == "nt" else "clear")
	print("~" * 50)
	print()
	print("# create windscribe account")
	print("# by : Lynph ")
	print()
	print("~" * 50)
	print()
	mail = tempmail()
	app = createAccount()
	imel = mail.createEmail()
	status = app.create(imel)
	token = mail.getToken(imel)
	mesg = mail.getMessage(token)
	resp = mail.getDetailMessage(mesg)
	cae = re.search('\[https://windscribe.com/signup/confirmemail/(.*?)\]',resp).group(1)
	rena = requests.get('https://windscribe.com/signup/confirmemail/' + cae,headers=app.headers,cookies=app.coco)
	if 'Email Confirmed' in rena.text:
	    print("# email has been confirmed")
	    req = requests.get('https://windscribe.com/myaccount?hello',headers=app.headers,cookies=app.coco)
	    toxen = re.search("csrf_token = '(.*?)';",req.text).group(1)
	    tine = re.search("csrf_time = (.*?);",req.text).group(1)
	    data = {
	    	"code":"PEACE",
			"ctoken":toxen,
			"ctime":tine
			}
	    req = requests.post('https://windscribe.com/myaccount/claimvoucher',data=data,cookies=app.coco).json()
	    if req['success'] == 1:
	        print("# submit code promo success !")
	        print(f"# account : {imel} ")
	        print("~" * 50)
except (KeyboardInterrupt,requests.exceptions.ConnectionError):
	exit()