# Developed By : Alaa 

import requests 
import os
from bs4 import BeautifulSoup
import re
from termcolor import colored


"""
# To-Do : 
 # Local Test Case :
	1 - Getting the list of all local html files recursively =====================================> DONE 
	2 - Reading the content of each file =========================================================> DONE
	3 - Passing the HTML content to Parser methods ===============================================> DONE

 # Remote Test Case :
 	1 - Parsing the URLs file and initiating the request to get the HTML =========================> DONE
	2 - Passing the HTML content to Parser methods ===============================================> DONE

 # HTML Parser methods :
		1 - Extract all links and check if the links are accessible as unauthenticated user ======> DONE
		2 - Extract all forms from the page ( GET & POST ) =======================================> DONE
		3 - Search for Reflected Input - potential Reflected XSS =================================> DONE
		4 - Search for Dangerous XSS functions  ==================================================> DONE
"""


class MyParser:

	# ---------------------------------------------------------------------------------------- #
	def __init__(self):
		self.listFileName = "listOfFiles.txt"
		self.listOfAccessibleLinks = "listOfAccessibleLinks.txt"
		self.urlsFile = "urls.txt"
		self.host = "http://127.0.0.1/" 
		self.XSSFuncFilePath = "XSSFunc.txt"
	############################################################################################


	# --------------------------------------------------------------------------------------------------------------------------------------------- #
	# This function retrieves all the html/htm files in the current path, and writes the files names (with full path) to the listFileName.txt file  #
	# --------------------------------------------------------------------------------------------------------------------------------------------- #
	def findHTMLFiles(self):
		print(colored("[+] Trying to Find all html/htm files recursively","yellow"))
		command = os.popen("find . -iregex '.*\\.\\(htm\\|html\\)' -print  >" + self.listFileName)
	############################################################################################


	# ------------------------------------------------------------------------------------------- #
	# This function read each line of the listFileName.txt file and pass it to Parser functions   #
	# ------------------------------------------------------------------------------------------- #
	def parseLocalListFile (self):
		file = open(self.listFileName, 'r',encoding='utf-8')
		Lines = file.readlines()
		for line in Lines:
			print(colored(" [++] Parsing %s file" %(line.strip()),"blue"))
			self.parseHTMLFromFile(line.strip())
			# 4 - Dangerous XSS Sinks
			self.findDangFunc(line.strip())
	############################################################################################

			

	# ------------------------------------------------------------------------- #
	# This function parse the html from local file and call the parser methods  #
	# ------------------------------------------------------------------------- #
	def parseHTMLFromFile(self,fileName):
		contents = open(fileName,encoding='utf-8').read()
		soup = BeautifulSoup(contents, 'html.parser')
		# 1 - find all accessible links
		self.findAccessibleLinks(soup)
		forms = soup.find_all('form')
		# 2 - all GET & POST forms with their inputs
		self.getForms(forms)
		# 3 - Reflected Input - Potential Reflected XSS
		self.findReflectedInputs(forms) # Need To test this 
	############################################################################################


	# ------------------------------------------------------------------------------------------------- #
	# This function extracts all links and check if the links are accessible as unauthenticated user    #
	# ------------------------------------------------------------------------------------------------- #
	def findAccessibleLinks(self,soup):
		print("  [+++] Trying to find all accessible links (no auth)")
		# find all the anchor tags with "href" 
		for link in soup.find_all('a', attrs={'href': re.compile("(http|https)\:\/\/[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(\/\S*)?")}):
			# try to access the link as unauthenticated user 
			try:
				r = requests.get(link.get('href'))
			except requests.exceptions.ConnectionError:
				continue # continue if the page is not accessible 
			if (r.status_code == 200): # if the page accessible write the link to the file 
				with open('listOfAccessibleLinks.txt', 'a') as the_file:
					the_file.write( str(link.get('href')) + '\n')
				print(colored("Check the listOfAccessibleLinks.txt file!", "green"))

	############################################################################################



	# ---------------------------------------------------------------------------------------------------------- #
	# This function reads the contents of the urls.txt file, and pass each url to the parseHTMLFromURL function  #
	# ---------------------------------------------------------------------------------------------------------- #
	def parseURLFile (self):
		file = open(self.urlsFile, 'r',encoding='utf-8')
		Lines = file.readlines()
		for line in Lines:
			print(colored("[+] Parsing %s url" %(line.strip()),"blue"))
			self.parseHTMLFromURL(line.strip())
	############################################################################################



	# ------------------------------------------------------------------- #
	# This function parse the html from url  and call the parser methods  #
	# ------------------------------------------------------------------- #
	def parseHTMLFromURL (self,url):
		response = requests.get(url)
		html = response.text
		soup = BeautifulSoup(html, 'html.parser')
		# 1 - find all accessible links
		self.findAccessibleLinks(soup)
		forms = soup.find_all('form')
		# 2 - all GET & POST forms with their inputs
		self.getForms(forms)
		# 3 - Reflected Input - Potential Reflected XSS
		self.findReflectedInputs(forms)
		# 4 - Dangerous XSS Sinks
		with open('tempHTML.txt', 'a') as the_file:
							the_file.write(html)
		self.findDangFunc("tempHTML.txt") # Need to create temp local html file from the response 
	############################################################################################



	# ---------------------------------------------------------------------------------------- #
	# This function prints the GET & POST forms details 
	# ---------------------------------------------------------------------------------------- #
	def getForms(self,forms):
		print("  [+++] Extracting all forms from the page")
		for form in forms:
			method = form.attrs.get('method')
			if method == "post" or method == "get":
				print("================")
				print(colored("Action: %s" %(form.attrs.get('action')), "green"))
				print(colored("Method: %s" %(method), "green"))
				# get all form inputs
				inputs = []
				for inputTag in form.find_all("input"):
					# get type of input form control
					inputType = inputTag.attrs.get("type", "text")
					print(colored("Input Type: %s" %(inputType), "green"))
					# get name attribute
					inputName = inputTag.attrs.get("name")
					print(colored("Input Name: %s" %(inputName), "green"))
					# get the default value of that input tag
					inputValue =inputTag.attrs.get("value", "")
					print(colored("Input Value: %s" %(inputValue), "green"))
					print("--------------")
				print("\n")
	############################################################################################



	# ---------------------------------------------------------------------------------------- #
	# This function does the following : 
		# - parse the forms and extracts POST forms and its input
		# - send post request and injecting static sting "TestingReflectedString" in each parameter
		# - check if the string reflected in the html page 
	# ---------------------------------------------------------------------------------------- #
	def findReflectedInputs(self,forms):
		print("  [+++] Trying to find Reflected Inputs")
		for form in forms:
			method = form.attrs.get('method')
			action = form.attrs.get('action')
			testString = "TestingReflectedString"
			postBody = ""
			if method == "post": # if the form method is POST, then extract POST parameters from the form
				inputs = []
				for inputTag in form.find_all("input"):
					# get name attribute
					inputName = inputTag.attrs.get("name")
					postBody += str(inputName) + "=" + testString + "&"
				postBody = postBody[:-1] # remove last &
				# send the POST request
				url = self.host + str(action)  
				res = requests.post(url,postBody)
				if res.status_code == 200 : # parse the html only if we got 200 
					if testString in res.text: 
						print ("Potential Reflected XSS!!") 
						#print (res.text)
				postBody = "" # reset the variable for the next action
	############################################################################################


	# ---------------------------------------------------------------------------------------- #
	# This function tries to find XSS Sinks
	# ---------------------------------------------------------------------------------------- #
	def findDangFunc (self,htmlFilePath):
		print("  [+++] Trying to find Dangerous XSS Functions/Sinks")
		keys = open((self.XSSFuncFilePath), "r").readline()
		keys = keys.split(',')  # separates key strings
		with open(htmlFilePath,encoding='utf-8') as f:
		    for num,line in enumerate(f, 1):
		        for key in keys:
		            if key.strip() in line:
		            	print(colored("Function: " + key.strip(), "green"))
		            	print(colored("Whole line :" + line, "green"))
		            	print(colored("Line # %d: " %(num) , "green"))
		            	print("=========")
	############################################################################################


def main():
	parser = MyParser()
	print(colored("[i] Running the script for local test case","cyan"))
	parser.findHTMLFiles()
	parser.parseLocalListFile()

	#print(colored("[i] Running the script for remote test case","cyan"))
	#parser.parseURLFile()


if __name__ == '__main__':
    main()
