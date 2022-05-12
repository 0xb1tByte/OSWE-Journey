import requests
import xml.etree.ElementTree as ET    
from termcolor import colored
import json

headers = {'Accept': '*/*' , 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36','Content-Type': 'application/x-www-form-urlencoded'} # update the headers values as required
url = "" # update the url 


print(colored("[+] Injecting XSS Payloads","cyan"))
########################################################
# the below code is an example of reading the XSS payloads from .txt file, and iterating through each payload and inject it into a POST Parameter 
########################################################
print(colored("[++] Reading the payloads from txt file","yellow"))
file1 = open('xssPayload.txt', 'r')
Lines = file1.readlines() 
count = 0
# Strips the newline character
for line in Lines:
    count += 1
    #print("Line{}: {}".format(count, line.strip()))
    xssPayload = line.strip()
    print(colored("payload : %s" %(line.strip()), "yellow"))
    body = "injectableParam1=test payload "+str(count)+"&injectableParam2="+str(xssPayload) # update the body params 
    res = requests.post(url, body, headers=headers)
    print(colored("The status code : %s" %(str(res.status_code)),"yellow"))
    #print(res.text)


########################################################
# the below code is an example of reading the XSS payloads from XML file, and iterating through each payload and inject it into a JSON Parameter 
########################################################
print(colored("[++] Reading the payloads from XML file","yellow"))    
doc1 = ET.parse("xssAttacks.xml")
root = doc1.getroot()
counter = 1
for element in root.findall("attack"):
    code = element.find("code").text
    name = element.find("name").text
    #print("name: " + name)
    #print("code: " + code)
    xssPayload = code
    print(colored("payload : %s" %(code), "yellow"))
    jsonParam = {"injectableJSONParam2":str(xssPayload)} # update JSON Param
    res = requests.post(url, json=jsonParam, headers=headers)
    print(colored("The status code : %s" %(str(res.status_code)),"yellow"))
    #print("line :" + str(counter))
    print()
    counter += 1
    #print(code)



