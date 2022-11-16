from datetime import date
import random
import traceback
import os
import base64
import subprocess
# PRAGRAPH FORMAT INDICATORS
#^ is newline

#PASSWORDS ARE TOO LONG, SHORTEN TO 16 CHARS

#Note that a filename that begins with an unerscore is reserved. Two underscores means hidden.

#BASE MENU FUNCTIONS
def main(d):

	print("Loading Files.")
	#make Files dir if it does not exist
	try:
		os.mkdir("Files")
	except Exception:
		pass
	try:
		ff = open("Files/_oneKey.txt", "x") 
	except Exception:
		pass
	try:
		f = open("Files/__Settings.txt", "w") 
		f.write(defaultConstant())
	except Exception:
		pass
	print("Loading Settings.")
	getSettings()
	print("Ready.\n----")
	print("Thank you for using the Keybasket 2.0 Console Application Prototype.\nCopyright 2022.\n\nThis is created by Andrew Vella.\nEmail:  andyjvella@gmail.com.\nGithub: @PixelatedStarfish\n\nPlease see the Disclaimer, before using this app.") 
	try: 	
		if (d[0] == "d" or d[1] == "d"):
			global DEBUG
			DEBUG = True 
		if (d[0] == "s" or d[1] == "s"):
			global SAVE
			SAVE = True
	except IndexError:
		pass #no arg
	menu()
	return

def getSettings():
	global SAVE
	global DEBUG 
	try:
		
		f = open("Files/__Settings.txt", "r")
		s = f.read()
		f.close()
		if (s[0] == "0"):
			SAVE = False
		if (s[0] == "1"):
			SAVE = True
		if (s[1] == "0"):
			DEBUG = False
		if (s[1] == "1"):
			DEBUG = True
	except IndexError: #no settings
		
		f = open("Files/__Settings.txt", "w") 
		f.write(defaultConstant())
		f.close()
		getSettings()
	return

def menu():
	while (True):
		a = input("\nType a number to select an option:\n0  Help\n1  One Key Mode\n2  Two Key Mode\n3  Username Generator\n4  File Menu\n5  Settings Menu\n6  Disclaimer and License\n7  Erase Data\n8  Close\n> ")
		if (a == "-1"):
			test()
		if (a == "0"):
			print(paragraphAlign("^-Help-^^This application is designed to generate\nand store passwords on your computer.\nWhile other managers integrate with your browser,\nthey are much better for accumulating passwords\nthan actually managing them.\nAt worst you can become\ndependant on a specific browser to access your stuff.\nAt best you might still use\na small number of passwords\nyou wrote yourself for the important stuff,\nwhich puts the important stuff at risk.") + "\n\n" + paragraphAlign("My thinking is that 100 auto-generated passwords is bad,\na small number of manually created passwords is worse,\nand both of these together is what often happens.\nInstead of coming up with a few compilcated\npasswords and using them everywhere,\ndepending on a browser extension,\nor (most likely) both\nThis generates secure passwords from simple keys,\nthat are easy to create and remember.") + "\n\n" + paragraphAlign("Keys are " +str(KEY_LENGTH)+ " characters max.^Passwords are " + str(PASSWORD_LENGTH) +" characters."))
		if (a == "1"):
			oneKey()
		if (a == "2"):
			twoKey()
		if (a == "3"):
			genUserName()
		if (a == "4"):
			FileMenu("FileMenu")
		if (a == "5"): #val in parens right by each option
			SettingsMenu("SettingsMenu")
		if (a == "6"):
			print("-Disclaimer-\n")
			print(paragraphAlign("So, in plain terms, this app should be used with some care. It is about as secure as a basket of keys. If you keep it behind a locked door, your keys should stay put because only trusted people get anywhere near them. By analogy this app is the basket, and your computer is the door. You should be sure that your computer is secured and safe before using this app. No information produced in whole or part by this app is garenteed to be perfectly safe. Your files can be read, modified, or deleted. The app source code can also be read, modfied, or deleted, which would cause unpredictable effects while running the app. Back up important things; store your passwords in a few safe places. Keep untrustworthy people off your computer. Do not store your passwords publicly, or generate them with keys that are easy to guess. Stay safe!"))
			print("\n\n")
			print(paragraphAlign('MIT License^^Copyright (c) 2022 Andrew Vella^^Permission is hereby granted, free of charge, to any person obtaining a copy^of this software and associated documentation files (the "Software"), to deal^in the Software without restriction, including without limitation the rights^to use, copy, modify, merge, publish, distribute, sublicense, and/or sell^copies of the Software, and to permit persons to whom the Software is^furnished to do so, subject to the following conditions:^^The above copyright notice and this permission notice shall be included in all^copies or substantial portions of the Software.^^THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR^IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,^FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE^AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER^LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,^OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE^SOFTWARE.'))
		if (a == "7"):
			h = input("Erase all data and close? Type 'y' for yes.\n")
			if (h[0].lower().lstrip() == 'y'):
				l = os.listdir("Files")
				for i in l:
					os.remove("Files/" + i)
					print("Deleted '" + i + "'")
				print("Done.")
				input("Press Return (Enter) to close.\n> ")
				exit()
				return
				
		if (a == "8"):
			exit()
		input("Press Return (Enter) to return to the Main Menu.\n> ")
	return

def twoKey():
	
	#Password generator
	kOne = input("\nGive a Username Key. Be sure it is not easily guessed:\n> ")[0:12]
	kTwo = input("\nGive a Site Key, such as a website name:\n> ")[0:12]
	r = (genResult(kOne, kTwo))
	print("\nResult:\n" + r + "\n")
	copyToclipPC(r)
	if (SAVE):
		saveTkToFile(kOne, kTwo, r)

	return

def oneKey():
	
	#Password generator
	kOne = input("\nGive a Key, such as a word you will remember. Be sure it is not easily guessed:\n> ")[0:12]
	kTwo = "Default_Key_2"
	r = (genResult(kOne, kTwo))
	print("\nResult:\n" + r + "\n")
	copyToclipPC(r)
	if (SAVE):
		saveOkToFile(kOne, r)

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
	
def getTime():
	today = date.today()
	d4 = today.strftime("%b-%d-%Y")
	return d4

def saveTkToFile(kOne, kTwo, r):
	#this used to ask to save. Now it is a setting.
	h = 'y'
	if (h[0].lower().lstrip() == 'y'):
		t = getTime()
		content = "Key One:\t" + kOne + "\nKey Two:\t" + kTwo + "\nPassword:\t" + r + "\nDate:\t\t"  + t + "\n\n"

		#make the file, if it exists, move on
		try:
			f = open("Files/" + kOne + ".txt", "x")
			print("Created '" + kOne + ".txt'")
			f.close()
		except Exception as e:
			#print(e)
			pass
		s = decrypt_file("Files/" + kOne + ".txt")
		s += content
		encrypt_to_file("Files/" + kOne + ".txt", s)
		print("Added to '" + kOne + ".txt'\n")
	return

def saveOkToFile(kOne, r):
	
	#this used to ask to save. Now it is a setting.
	h = 'y'
	if (h[0].lower().lstrip() == 'y'):
		t = getTime()
		content = "Key:\t\t" + kOne + "\nPassword:\t" + r + "\nDate:\t\t"  + t + "\n\n"

		#make the file, if it exists, move on
		try:
			f = open("Files/_oneKey.txt", "x") 
			print("Created '" + "Files/_oneKey.txt'")
			f.close()
		except Exception:
			pass
		s = decrypt_file("Files/_oneKey.txt")
		s += content
		encrypt_to_file("Files/_oneKey.txt", s)
		
		print("Added to '_oneKey.txt'\n")
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
	
#SUBMENUS
def SettingsMenu(a):
	while (not a == "4"):
		global SAVE
		global DEBUG
		if (a == "SettingsMenu"):

			print("Settings Menu\n\n0  Help")
			print ("1  File Saving      (" + menuBooleanFormatter(SAVE) + ")")
			print ("2  Debug Mode       (" + menuBooleanFormatter(DEBUG) + ")")
			print ("3  Retore Defaults\n4  Back to Main Menu")
			b = input("> ")
			if (not a == "4"):
				SettingsMenu(b)
			menu()
		if (a == "0"):
			print ("1  Toggle the option to save to a file.")
			print ("2  Toggle the option to display errors.")
			print ("3  Retore settings to default.\n4  Return to the Main Menu.")

		if (a == "1"):
			SAVE = (not SAVE)
			print("Set to " + menuBooleanFormatter(SAVE))
		if (a == "2"):
			DEBUG = (not DEBUG)
			print("Set to " + menuBooleanFormatter(DEBUG))
		if (a == "1" or a == "2"):
			o = ""
			if (SAVE and DEBUG):
				o = "11"
			if (SAVE and not DEBUG):
				o = "10"
			if (not SAVE and DEBUG):
				o = "01"
			if (not SAVE and not DEBUG):
				o = "00"

			f = open("Files/__Settings.txt", "w") 
			f.write(o) 
			f.close()
			print("\nSaved.\n")

		if (a == "3"):
			SAVE = False
			DEBUG = False
			f = open("Files/__Settings.txt", "w") 
			f.write(defaultConstant())
			close()
			print("\nRestored.\n")
	
		input("Press Return (Enter) to return to the Settings Menu.\n> ")
		a = "SettingsMenu"
	return  

def FileMenu(a):
	while (not a == "4"):
		global SAVE
		global DEBUG
		if (a == "FileMenu"):

			print("Files Menu\n\n0  Help\n1  List Files\n2  Read File\n3  Delete File\n4  Back to Main Menu")
			b = input("> ")
			if (not a == "4"):
				FileMenu(b)
			menu()
		if (a == "0"):
			print ("1  List all files by name.")
			print ("2  Read the contents of a file.")
			print ("3  Permenantly erase a file. (Be sure it is not in use.)")
			print ("4  Return to the Main Menu.")

		if (a == "1"):
			printFileList()
		if (a == "2"):
			print(decrypt_file("Files/" +fileSelector()))
		if (a == "3"):
			os.remove("Files/" +fileSelector())
			print("Deleted.\n")
		input("Press Return (Enter) to return to the Files Menu.\n> ")
		a = "FileMenu"
	return 

def fileSelector():
	#get input and check for a match in the Files dir, if no match is found, recur
	l = os.listdir("Files")

	#get input
	s = input("Please select a file by typing it's name. You do not need to include the extension.\n>  ") + ".txt"
	s = s.replace(".txt.txt", ".txt")

	for i in l:
		if (s == i):
			return s
	print("\n'" + s + "' not found.")
	printFileList()
	return fileSelector()

def printFileList():
	l = os.listdir("Files")
	print("File List:")
	for i in l:
		if (not (i[0] == '_' and i[1] == '_')):
			print(i)
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

def menuBooleanFormatter(b):
	if (b):
		return "ON"
	return "OFF"

def defaultConstant(): #for settings; files on, debug off
	return "10"

#ENCRYPTION AND DECRYPTION

def encrypt_to_file(path, message):
	global ENCODING
	message = message.replace(" " * 8, chr(7))
	message = reverse(message)
	string_bytes = message.encode(ENCODING)
	base64_bytes = base64.b64encode(string_bytes)
	base64_string = base64_bytes.decode(ENCODING)

	f = open(path, "w")
	f.write(base64_string)
	f.close()
	return

def decrypt_file(path):
	global ENCODING
	f = open(path, "r")
	base64_string = f.read()
	base64_bytes = base64_string.encode(ENCODING)
	string_bytes = base64.b64decode(base64_bytes)
	m = string_bytes.decode(ENCODING)
	return reverse(m.replace(chr(7), " " * 8))

def reverse(s):
	out = ""
	i = len(s)

	while (i > 0):
		i = i - 1
		out += s[i]
	return out

#SYSTEM
def copyToclipPC(txt):
	print("\nCopied to Clipboard.") #technically a lie but the message needs to print before the function ends.
	cmd='echo '+txt.strip()+'|clip'
	return subprocess.check_call(cmd, shell=True)

def copyToclipMac(txt):
	print("\nCopied to Clipboard.") #technically a lie but the message needs to print before the function ends.
	cmd='echo '+txt.strip()+'|pbcopy'
	return subprocess.check_call(cmd, shell=True)

def test():
	print("No test.")
	return

#MAIN
print("Initializing.")

#globals
SAVE = False
DEBUG = False
LINE = 50
KEY_LENGTH = 16
PASSWORD_LENGTH = 16
ENCODING = "utf_8" 

print("Loading Working Directory.")
#set cwd to source file
os.chdir(os.path.dirname(os.path.abspath(__file__)))

try: 
	main(" ")
except PermissionError:
	print("Access denied. Files may need to be closed in another application first.")
	input("Error; press Return (Enter) to close.\n> ")

except Exception:
	#traceback.print_exc()
	if (DEBUG):
		traceback.print_exc()
	input("Error; press Return (Enter) to close.\n> ")

 #Sources:
 #Copy to Clipboard
  #https://stackoverflow.com/questions/11063458/python-script-to-copy-text-to-clipboard
 
 #Current Working Dir
  #https://note.nkmk.me/en/python-os-getcwd-chdir/

 #Encryption
  #https://www.geeksforgeeks.org/encoding-and-decoding-base64-strings-in-python/
 
 #License
  #https://choosealicense.com/
