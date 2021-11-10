# By : Alaa (aka b1tByte) , github: 0xb1tByte
import smtplib
import optparse
import requests
import sys
import shlex


# To Do :
	# Main Tasks: 
		# 1 - Inject localFilePayloads into all fields ==> DONE
			# Usage : python3 smtpFuzzer.py -f attacker@offsec.local -t admin@offsec.local -s 192.168.129.106 -i allFields -m localFilePayloads -l payloadsFile.txt  
		
		# 2 - Inject onePayload into all fields =========> Done
			# Usage : python3 smtpFuzzer.py -f attacker@offsec.local -t admin@offsec.local -s 192.168.129.106 -i allFields -m onePayload -c "payload"  
		
		# 3 - Inject localFilePayloads into one field ===> Done
			# Usage : python3 smtpFuzzer.py -f attacker@offsec.local -t admin@offsec.local -s 192.168.129.106 -i oneField  -m localFilePayloads -l payloadsFile.txt -F Date  

		# 4 - Inject onePayload into one field ==========> Done
			# Usage : python3 smtpFuzzer.py -f attacker@offsec.local -t admin@offsec.local -s 192.168.129.106 -i oneField -m onePayload -c "payload" -F Date
	# Additional Tasks :
		# 1 - Printing payloads list within the file ====> Done
			# Usage : python3 smtpFuzzer.py -P payloadsFile.txt 

		# 2 - Converting a payload into a well-formed payload that escape bash special characters, then the well-formed payload can be suplied to the script directly 
			# Usage : python3 smtpFuzzer.py -e singlePayload.txt  

smtpHeaders = [
"Date",
"Subject",
"Body",
"Accept-Language",
"Alternate-Recipient",
"Autoforwarded",
"Autosubmitted",
"Bcc",
"Cc",
"Comments",
"Content-Identifier",
"Content-Return",
"Conversion",
"Conversion-With-Loss",
"DL-Expansion-History",
"Deferred-Delivery",
"Delivery-Date",
"Discarded-X400-IPMS-Extensions",
"Discarded-X400-MTS-Extensions",
"Disclose-Recipients",
"Disposition-Notification-Options",
"Disposition-Notification-To",
"Encoding",
"Encrypted",
"Expires",
"Expiry-Date",
"Generate-Delivery-Report",
"Importance",
"In-Reply-To",
"Incomplete-Copy",
"Keywords",
"Language",
"Latest-Delivery-Time",
"List-Archive",
"List-Help",
"List-ID",
"List-Owner",
"List-Post",
"List-Subscribe",
"List-Unsubscribe",
"Message-Context",
"Message-ID",
"Message-Type",
"Obsoletes",
"Original-Encoded-Information-Types",
"Original-Message-ID",
"Originator-Return-Address",
"PICS-Label",
"Prevent-NonDelivery-Report",
"Priority",
"Received",
"References",
"Reply-By",
"Reply-To",
"Resent-Bcc",
"Resent-Cc",
"Resent-Date",
"Resent-From",
"Resent-Message-ID",
"Resent-Reply-To",
"Resent-Sender",
"Resent-To",
"Return-Path",
"Sender",
"Sensitivity",
"Supersedes",
"X400-Content-Identifier",
"X400-Content-Return",
"X400-Content-Type",
"X400-MTS-Identifier",
"X400-Originator",
"X400-Received",
"X400-Recipients",
"X400-Trace"]



def sendEmail(sender,receiver,message,smtpServer):
	try:
		smtpObj = smtplib.SMTP(smtpServer)
		smtpObj.sendmail(sender, receiver, message)         
		print ("[++] Successfully sent email")
	except SMTPException:
		print ("[!] Error: unable to send email")


def allFieldsAttack(payloadMode,payload,sender,receiver,smtpServer):
	msg  = ''
	body = ''
	if payloadMode == "localFilePayloads":
		# loop over each header
		for header in smtpHeaders:
			counter = 0
			with open(payload) as file:
				# loop over each Payload in the file
				for line in file:
					msg += (header + ":" + str(line.rstrip())) + "\n"
					body = "injected Payload [%d] : %s into Header: %s" % (counter, line.rstrip(),header) + "\n"
					print("[+] injected Payload [%d]: %s into Header: %s" % (counter, line.rstrip(),header))
					msg += body
					sendEmail(sender,receiver,msg,smtpServer)
					msg = '' # re-set message for next payload 
					body = ''# re-set body for next payload 
					counter += 1
	elif payloadMode == "onePayload":
		# loop over each header
		for header in smtpHeaders:
			msg += (header + ":" + str(payload)) + "\n"
			body = "injected Payload : %s into Header: %s" % (payload,header) + "\n"
			print("[+] injected Payload : %s into Header: %s" % (payload,header))
			msg += body
			sendEmail(sender,receiver,msg,smtpServer)
			msg = '' # re-set message for next header field
			body = ''# re-set body for next header field


def oneFieldAttack(payloadMode,payload,sender,receiver,smtpServer,fieldName):
	msg  = ''
	body = ''
	if payloadMode == "localFilePayloads":
		with open(payload) as file:
			counter = 0
			for line in file:
				msg += (fieldName + ":" + str(line.rstrip())) + "\n"
				body = "injected Payload [%d]: %s into Header: %s" % (counter,line.rstrip(),fieldName) + "\n"
				print("[+] injected Payload [%d]: %s into Header: %s" % (counter,line.rstrip(),fieldName))
				msg += body
				sendEmail(sender,receiver,msg,smtpServer)
				msg = '' # re-set message for next payload 
				body = ''# re-set body for next payload 
				counter += 1 # increament payload counter 
	elif payloadMode == "onePayload":
		msg += (fieldName + ":" + str(payload)) + "\n"
		body = "injected Payload : %s into Header: %s" % (payload,fieldName) + "\n"
		print("[+] injected Payload : %s into Header: %s" % (payload,fieldName))
		msg += body
		sendEmail(sender,receiver,msg,smtpServer)


def printPayloads (file):
	counter = 0
	with open(file) as file:
		for line in file:
			print("Payload %d : %s" %(counter ,line.rstrip()))
			counter  += 1


def escapeBashCharacters (payloadFile):
	with open(payloadFile) as payload:
			for line in payload:
				s = line.rstrip()
				print("[+] Your well-formed payload is:")
				print(shlex.quote(s))


def main():
	 # setting the script options
	 usage = "%prog -f sender -t receiver -s smtpServer:port [options]"
	 parser = optparse.OptionParser(usage=usage)
	 parser.add_option("-f", "--from", type="string", action="store", dest="sender", help="From Email Address")
	 parser.add_option("-t", "--to", type="string", action="store", dest="receiver",  help="Destination Email Address")
	 parser.add_option("-s", "--smtp", type="string", action="store", dest="smtpServer",help="SMTP Server")
	 parser.add_option("-u", "--user", type="string", action="store", dest="username", help="SMTP Username (optional)")
	 parser.add_option("-p", "--password", type="string",action="store", dest="password", help="SMTP Password (optional)")
	 parser.add_option("-m", "--payloadMode", type="choice", choices=["onePayload", "localFilePayloads"], action="store", dest="payloadMode",help="Available Payloads modes:\n" + "onePayload, localFilePayloads \n")
	 parser.add_option("-l", "--localFile", type="string", action="store", dest="localFile", help="Local Payloads file (file format: each payload in one line). This option must be used together with -m to specify the local file payloads")
	 parser.add_option("-c", action="store", dest="custompayload", help="Inject Custom Payload. This option must be used together with -m to specify the custom payload, you can use -e to create well-formed payload before pass it to the script")
	 parser.add_option("-i", "--injectionMode", type="choice", choices=["oneField", "allFields"], action="store", dest="injectionMode", help="Available Injection modes:\n" + "oneField, allFields \n")
	 parser.add_option("-F", "--headerField", type="string", action="store", dest="headerField", help="Injection Field. This option must be used together with -i to specify the field that will be injected")
	 parser.add_option("-e", "--escapeBash", type="string",  action="store", dest="payloadFile", help="Use this option to escape any of the special shell characters in your payload, you should save the payload in a file, and pass the file name to the script")
	 parser.add_option("-P", "--printPayloads", type="string", action="store", dest="payloads", help="Use this option to print the payloads within the provided file, you should submit a file name where your payloads are stored")

	 # getting user's options
	 (options, args) = parser.parse_args()
	 sender = options.sender
	 receiver = options.receiver
	 smtpServer = options.smtpServer
	 username = options.username
	 password = options.password
	 custompayload = options.custompayload 
	 payloadMode = options.payloadMode 
	 injectionMode = options.injectionMode
	 headerField = options.headerField
	 payloadsFile = options.localFile
	 escape = options.payloadFile
	 payloads = options.payloads

	 # checking the supplied options 
	 if escape:
	 	escapeBashCharacters(escape)
	 elif payloads:
	 	printPayloads(payloads)
	 elif not (receiver and sender and smtpServer and injectionMode and payloadMode):
	 	parser.print_help()
	 	sys.exit()
	 if payloadMode == "onePayload":
	 	if injectionMode == "allFields":
	 		allFieldsAttack(payloadMode,custompayload,sender,receiver,smtpServer) # Task #2 - onePayload into all fields
	 	elif injectionMode == "oneField":
	 		oneFieldAttack(payloadMode,custompayload,sender,receiver,smtpServer,headerField) # Task #4 - onePayload into one field
	 elif payloadMode == "localFilePayloads":
	 	if injectionMode == "allFields":
	 		allFieldsAttack(payloadMode,payloadsFile,sender,receiver,smtpServer) # Task #1 - localFilePayloads into all fields
	 	elif injectionMode == "oneField":
	 		oneFieldAttack(payloadMode,payloadsFile,sender,receiver,smtpServer,headerField) # Task #3 localFilePayloads into one field
	 

if __name__ == '__main__':
    main()

