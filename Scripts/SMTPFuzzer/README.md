## Description :
This script can be used to automate the injection-based vulnerabilities (xss,sqli .. etc) against [SMTP headers](https://www.iana.org/assignments/message-headers/message-headers.xhtml)

## What smtpFuzzer.py Does? : 
- `Multiple Payloads into All Fields`: Injecting several payloads ( supplied to the script through a file ) into all SMTP headers (Sniper Approach - enumerates over each header, one at a time) 
- `Multiple Payloads into One Field`: Injecting several payloads into a specific SMTP header 
- `One Payload into All Fields`: Injecting a specific payload into all SMTP headers (Sniper Approach)
- `One Payload into One Field`: Injecting a specific payload into a specific SMTP header
- Printing payloads list 
- Converting a payload into a well-formed payload that escape bash special characters, then the well-formed payload can be supplied to the script argument directly 

## Help Page:
```
Options:
  -h, --help            show this help message and exit
  -f SENDER, --from=SENDER
                        From Email Address
  -t RECEIVER, --to=RECEIVER
                        Destination Email Address
  -s SMTPSERVER, --smtp=SMTPSERVER
                        SMTP Server
  -u USERNAME, --user=USERNAME
                        SMTP Username (optional)
  -p PASSWORD, --password=PASSWORD
                        SMTP Password (optional)
  -m PAYLOADMODE, --payloadMode=PAYLOADMODE
                        Available Payloads modes: onePayload,
                        localFilePayloads
  -l LOCALFILE, --localFile=LOCALFILE
                        Local Payloads file (file format: each payload in one
                        line). This option must be used together with -m to
                        specify the local file payloads
  -c CUSTOMPAYLOAD      Inject Custom Payload. This option must be used
                        together with -m to specify the custom payload, you
                        can use -e to create well-formed payload before pass
                        it to the script
  -i INJECTIONMODE, --injectionMode=INJECTIONMODE
                        Available Injection modes: oneField, allFields
  -F HEADERFIELD, --headerField=HEADERFIELD
                        Injection Field. This option must be used together
                        with -i to specify the field that will be injected
  -e PAYLOADFILE, --escapeBash=PAYLOADFILE
                        Use this option to escape any of the special shell
                        characters in your payload, you should save the
                        payload in a file, and pass the file name to the
                        script
  -P PAYLOADS, --printPayloads=PAYLOADS
                        Use this option to print the payloads within the
                        provided file, you should submit a file name where
                        your payloads are stored
                                                  
```

## Usage : 
1 - `Multiple Payloads into All Fields`: 
```bash
python3 smtpFuzzer.py -f attacker@local -t admin@local -s 192.168.129.106 -i allFields -m localFilePayloads -l payloadsFile.txt
```

2 - `Multiple Payloads into One Field` :
```bash
python3 smtpFuzzer.py -f attacker@local -t admin@olocal -s 192.168.129.106 -i oneField  -m localFilePayloads -l payloadsFile.txt -F Date
```

3 - `One Payload into All Fields` :
```bash
python3 smtpFuzzer.py -f attacker@local -t admin@local -s 192.168.129.106 -i allFields -m onePayload -c "payload"
```

4 - `One Payload into One Field` : 
```bash
python3 smtpFuzzer.py -f attacker@local -t admin@local -s 192.168.129.106 -i oneField -m onePayload -c "payload" -F Date
```

5 - Printing payloads list 
```bash
python3 smtpFuzzer.py -P payloadsFile.txt
```

6 - Crafting a well-formed payload :
```bash
python3 smtpFuzzer.py -e singlePayload.txt
```

## Sample Output :
1 - `Multiple Payloads into All Fields`: 
![alt text](https://github.com/0xb1tByte/OSWE-Journey/blob/main/Scripts/SMTPFuzzer/1.png)


2 - `Multiple Payloads into One Field` :
![alt text](https://github.com/0xb1tByte/OSWE-Journey/blob/main/Scripts/SMTPFuzzer/2.png)


3 - `One Payload into All Fields` :
![alt text](https://github.com/0xb1tByte/OSWE-Journey/blob/main/Scripts/SMTPFuzzer/3.png)


4 - `One Payload into One Field` : 
![alt text](https://github.com/0xb1tByte/OSWE-Journey/blob/main/Scripts/SMTPFuzzer/4.png)


5 - Printing payloads list 
![alt text](https://github.com/0xb1tByte/OSWE-Journey/blob/main/Scripts/SMTPFuzzer/5.png)


6 - Crafting a well-formed payload :
![alt text](https://github.com/0xb1tByte/OSWE-Journey/blob/main/Scripts/SMTPFuzzer/6.png)


