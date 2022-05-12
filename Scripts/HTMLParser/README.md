## Description :
The purpose of this script is to automate some tasks of source code review (particularly HTML & JS codes). The script can be used to test local codes files or remote codes (Fetching the code by initiating a request - reading URL). 

## Functionality 
 ### Local Test Case :
- 1 - Getting the list of all local html files recursively 
- 2 - Reading the content of each file 
- 3 - Passing the HTML content to Parser methods 

 ### Remote Test Case :
 - 1 - Parsing the URLs file and initiating the request to get the HTML
- 2 - Passing the HTML content to Parser methods 

 ### HTML Parser methods :
- 1 - Extract all links and check if the links are accessible as unauthenticated user 
- 2 - Extract all forms from the page ( GET & POST ) 
- 3 - Search for Reflected Input - potential Reflected XSS
- 4 - Search for Dangerous XSS functions 

## Dependencies 
```
requests 
os
BeautifulSoup
re
termcolor
```

## Usage 
```
PYTHONIOENCODING=utf-8 python3 myParser.py 
```
- ``PYTHONIOENCODING=utf-8`` : to set the encoding explicitly  


## Sample Output 
![alt text](https://github.com/0xb1tByte/OSWE-Journey/blob/main/Scripts/HTMLParser/1.jpg)
![alt text](https://github.com/0xb1tByte/OSWE-Journey/blob/main/Scripts/HTMLParser/2.jpg)
![alt text](https://github.com/0xb1tByte/OSWE-Journey/blob/main/Scripts/HTMLParser/3.jpg)


## Notes: 
- To run Remote test case, uncomment the ```221 & 222``` lines
- For Remote test case, you need to place ``urls.txt`` file in the same path with the script
- The script **is still under development**, expect **errors, mistakes**, and **garbage codes** .. etc
- The script was developed for learning purposes 
