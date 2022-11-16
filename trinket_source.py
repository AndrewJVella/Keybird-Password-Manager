#on trinket here: https://trinket.io/features/python3
from datetime import date
import random
import traceback
import os
import base64
import subprocess
# PRAGRAPH FORMAT INDICATORS
#^ is newline

#Note that a filename that begins with an unerscore is reserved. Two underscores means hidden.

#BASE MENU FUNCTIONS
def main(d):

	print("Ready.\n----")
	print("Thank you for using the Keybasket 2.0 Web Application Repl.\nCopyright 2022.\n\nThis is created by Andrew Vella.\nEmail:  andyjvella@gmail.com.\nGithub: @PixelatedStarfish\n\nPlease see the Disclaimer and License before using this app.") 
	menu()
	return


def menu():
	global KEY_LENGTH
	global PASSWORD_LENGTH
	while (True):
		a = input("\nType a number to select an option:\n0  Help\n1  One Key Mode\n2  Two Key Mode\n3  Username Generator\n4  See Disclaimer and License\n> ")
		if (a == "0"):
			print(paragraphAlign("^-Help-^^This application is designed to generate\nand store passwords on your computer.\nWhile other managers integrate with your browser,\nthey are much better for accumulating passwords\nthan actually managing them.\nAt worst you can become\ndependant on a specific browser to access your stuff.\nAt best you might still use\na small number of passwords\nyou wrote yourself for the important stuff,\nwhich puts the important stuff at risk.") + "\n\n" + paragraphAlign("My thinking is that 100 auto-generated passwords is bad,\na small number of manually created passwords is worse,\nand both of these together is what often happens.\nInstead of coming up with a few compilcated\npasswords and using them everywhere,\ndepending on a browser extension,\nor (most likely) both\nThis generates secure passwords from simple keys,\nthat are easy to create and remember.") + "\n\n" + paragraphAlign("Keys are "+ str(KEY_LENGTH) +" characters max.^Passwords are " + str(PASSWORD_LENGTH) + " characters."))
		if (a == "1"):
			oneKey()
		if (a == "2"):
			twoKey()
		if (a == "3"):
			genUserName()
		if (a == "4"):
			print("-Disclaimer-\n")
			print(paragraphAlign("So, in plain terms, this app should be used with some care. It is about as secure as a basket of keys. If you keep it behind a locked door, your keys should stay put because only trusted people get anywhere near them. By analogy this app is the basket, and your computer is the door. You should be sure that your computer is secured and safe before using this app. No information produced in whole or part by this app is garenteed to be perfectly safe. Your files can be read, modified, or deleted. The app source code can also be read, modfied, or deleted, which would cause unpredictable effects while running the app. Back up important things; store your passwords in a few safe places. Keep untrustworthy people off your computer. Do not store your passwords publicly, or generate them with keys that are easy to guess. Stay safe!"))
			print("\n\n")
			print(paragraphAlign('-MIT License-^^Copyright (c) 2022 Andrew Vella^^Permission is hereby granted, free of charge, to any person obtaining a copy^of this software and associated documentation files (the "Software"), to deal^in the Software without restriction, including without limitation the rights^to use, copy, modify, merge, publish, distribute, sublicense, and/or sell^copies of the Software, and to permit persons to whom the Software is^furnished to do so, subject to the following conditions:^^The above copyright notice and this permission notice shall be included in all^copies or substantial portions of the Software.^^THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR^IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,^FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE^AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER^LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,^OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE^SOFTWARE.'))
		input("Press Return (Enter) to return to the Main Menu.\n> ")
	return

def twoKey():
	
	#Password generator
	kOne = input("\nGive a Username Key. Be sure it is not easily guessed:\n> ")[0:12]
	kTwo = input("\nGive a Site Key, such as a website name:\n> ")[0:12]
	r = (genResult(kOne, kTwo))
	print("\nResult:\n" + r + "\n")
	#copyToclipPC(r)

	return

def oneKey():
	
	#Password generator
	kOne = input("\nGive a Key, such as a word you will remember. Be sure it is not easily guessed:\n> ")[0:12]
	kTwo = "Default_Key_2"
	r = (genResult(kOne, kTwo))
	print("\nResult:\n" + r + "\n")
	#copyToclipPC(r)


	return

def genResult(key1, key2):
	global PASSWORD_LENGTH

	if (len(key1) == 0 or len(key2) == 0):
		print("\nError: Empty key.\n")
		return ""
	if (key1[0] == "_"):
		print("\nError: User Keys cannot start with underscores. '_' (Such names are reserved.)\n")
		return ""

	nums = list("1234567890")
	uppers = list("QWERTYUIOPASDFGHJKLZXCVBNM")
	lowers = list("qwertyuiopasdfghjklzxcvbnm")
	symbols = list("-_")
	
	#get new char sequence (result)
	s = ""
	while(len(s) < PASSWORD_LENGTH):
		s += key1[len(key1)//2:len(key1)] + key2[0:len(key2)//2] + key1[0:len(key1)//2] + key2[len(key2)//2:len(key2)] #weave keys together for increased variation

	flipper = -1
	stuff = [nums, uppers, lowers, symbols]
	out = ""

	offset = 0
	for c in s:
		flipper = flipper - (ord(c) % 3) #cycle through the four categories of characters
		flipper = flipper % 4
		out += stuff[flipper][(offset + ord(c)) % len(stuff[flipper])] #take letter from s, convert to number N, set N + O to itself mod list length, and get char N in list added to out, add N to O
		offset += ord(c)

	#adjust to length

	return out[0:PASSWORD_LENGTH]

	return

#takes three phrases and splices three words together randomly...
def genUserName():

	p1 = input("\nGive a name you like:\n> ")
	p2 = input("\nGive a hobby:\n> ")
	p3 = input("\nGive a memorable reference:\n> ")
	
	cat1 = (p1).split(" ")
	cat2 = (p2).split(" ")
	cat3 = (p3).split(" ")

	#generate all possbile usernames (to ensure variation in possible names)
	nameList = [] 

	for i in cat1:
		for j in cat2:
			for k in cat3:
				nameList.append(i + "-" + j + "-" + k)
				nameList.append(i + "-" + k + "-" + j)
				nameList.append(k + "-" + j + "-" + i)
				nameList.append(k + "-" + i + "-" + j)
				nameList.append(j + "-" + k + "-" + i)
				nameList.append(j + "-" + i + "-" + k)

	i = 5 #different i, number of names listed, 5 max
	#randomly choose listed names
	outList =[] 
	while (i > 0):
	 	r = random.randint(0, len(nameList) -1)
	 	outList.append(nameList[r])
	 	nameList.remove(nameList[r])
	 	i = i - 1

	#display outlist and prompt for number to select, if the selection is not in the list, run again, copy selection to clipboard and return

	i = 0 #again, a different i
	print("\nUsernames:")
	while (i < len(outList)):
		outList[i] = outList[i].replace("'", "")
		outList[i] = outList[i].replace('"', "")
		print(outList[i])
		i = i + 1
	print()
	return
	

###FORMATTING THAT ACTUALLY COOPERATES###
def paragraphAlign(s): #for large strings
	s = s.replace("\n", " ")
	i = 0
	j = 0
	S = list(s)
	while (i < len(s)):
		if (j > LINE and s[i] == " "):
			S[i] = "\n" 
			j = 0
		i = i + 1
		j = j + 1
		
	out = ""
	i = 0
	while (i < len(S)):
		out += S[i]
		i = i + 1
	out = out.replace("^", "\n")
	return out


print("Initializing.")

#globals
LINE = 50
KEY_LENGTH = 16
PASSWORD_LENGTH = 16
ENCODING = "utf_8" 

print("Loading Working Directory.")
#set cwd to source file
os.chdir(os.path.dirname(os.path.abspath(__file__)))

try: 
	main(" ")

except Exception:
	traceback.print_exc()
	input("Error; press Return (Enter) to close.\n> ")

 #Sources:
 #Copy to Clipboard
  #https://stackoverflow.com/questions/11063458/python-script-to-copy-text-to-clipboard
 
 #Current Working Dir
  #https://note.nkmk.me/en/python-os-getcwd-chdir/

 #Encryption
  #https://www.geeksforgeeks.org/encoding-and-decoding-base64-strings-in-python/

  #Enbed via Trinket

  # <iframe src="https://trinket.io/embed/python3/258ed5f022?outputOnly=true&runOption=run&start=result" width="100%" height="356" frameborder="0" marginwidth="0" marginheight="0" allowfullscreen></iframe>
