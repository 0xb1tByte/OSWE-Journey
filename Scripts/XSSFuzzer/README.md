## Description :
a tiny XSS fuzzer (template script actually) that can read XSS payloads from txt file or XML file, and iterate through each payload and inject it into a POST parameter, or JSON parameter , no such magic here


## Dependencies 
```
requests
xml.etree.ElementTree     
termcolor 
json
```


## Notes: 
- Before running the code, there are a few lines in the code that require your modification (target url,headers, post/json params) , check the comments for that 
- The script **is still under development**, expect **errors, mistakes**, and **garbage codes** .. etc
- The script was developed for learning purposes 
