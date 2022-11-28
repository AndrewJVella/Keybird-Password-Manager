import random
import traceback
import os
import base64
import subprocess
import sys

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
	try:
		global KEY_LENGTH
		global PASSWORD_LENGTH
		encrypt_to_file("Files/_help.txt", paragraphAlign("^-Help-^^This application is designed to generate\nand store passwords on your computer.\nWhile other managers integrate with your browser,\nthey are much better for accumulating passwords\nthan actually managing them.\nAt worst you can become\ndependant on a specific browser to access your stuff.\nAt best you might still use\na small number of passwords\nyou wrote yourself for the important stuff,\nwhich puts the important stuff at risk.") + "\n\n" + paragraphAlign("My thinking is that 100 auto-generated passwords is bad,\na small number of manually created passwords is worse,\nand both of these together is what often happens.\nInstead of coming up with a few compilcated\npasswords and using them everywhere,\ndepending on a browser extension,\nor (most likely) both\nThis generates secure passwords from simple keys,\nthat are easy to create and remember.") + "\n\n" + paragraphAlign("Keys are " +str(KEY_LENGTH)+ " characters max.^Passwords are " + str(PASSWORD_LENGTH) +" characters."))
	except Exception:
		pass
	print("Loading Settings.")
	getSettings()
	fileCleaner()
	print("Ready.\n----")
	print("Thank you for using the Keybird Password Manager Prototype.\nCopyright 2022.\n\nThis is created by Andrew Vella.\nEmail:  andyjvella@gmail.com.\nGithub: @PixelatedStarfish\n\nPlease see the Disclaimer and License, before using this app.\n\nKnown Issues:\nThis app is currently vunerable to over-the-shoulder attacks.\nSomeone looking over your shoulder can see what you are typing and note your information. Please use this app in privacy.") 
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
		a = input("\nType a number and press enter (return) to select an option:\n0  Help\n1  One Key Mode\n2  Two Key Mode\n3  Username Generator\n4  File Menu\n5  Settings Menu\n6  Disclaimer and License\n7  Erase Data\n8  Close\n> ")
		if (a == "-1"):
			test()
		if (a == "-2"):
			fileCleaner()
		if (a == "-3"):
			h = input("Generate sample files? You might lose data. (Type 'y' for yes.)\n")
			if (h[0].lower().lstrip() == 'y'):
				for i in range(10):
					randomSampleFile(randomKey())
		if (a == "0"):
			print(decrypt_file("Files/_help.txt"))
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
			h = YesOrNo("Erase all data and close? (y/n). This will end thr current session.\n")
			if (h):
				l = os.listdir("Files")
				l.remove("__Settings.txt")
				f = open("Files/__Settings.txt", "w") 
				f.write(defaultConstant())
				f.close()
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

	return None

def saveTkToFile(kOne, kTwo, r):
	#this used to ask to save. Now it is a setting.
	h = 'y'
	if (h[0].lower().lstrip() == 'y'):
		t = getTime()
		content =  "\nSite Key:\t" + kTwo + "\nPassword:\t" + r + "\n"

		#make the file, if it exists, move on
		try:
			f = open("Files/" + kOne + ".txt", "x")
			print("Created '" + kOne + ".txt'") 
			f.close()
			encrypt_to_file("User key:\t" + "\n")
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
		content = "Key:\t\t" + kOne + "\nPassword:\t" + r + "\n"

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
			print ("3  Retore Defaults\n4  Back to Main Menu\n5  Close")
			b = input("> ")
			if (not a == "4"):
				SettingsMenu(b)
			menu()
		if (a == "0"):
			print ("1  Toggle the option to save to a file.")
			print ("2  Toggle the option to display errors.")
			print ("3  Retore settings to default.\n4  Return to the Main Menu.\n5  End session.")

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
		if (a == "5"):
			exit()
	
		input("Press Return (Enter) to return to the Settings Menu.\n> ")
		a = "SettingsMenu"
	return  

def FileMenu(a):
	while (not a == "5"):
		global SAVE
		global DEBUG
		if (a == "FileMenu"):

			print("Files Menu\n\n0  Help\n1  List Files\n2  Read File\n3  Edit File\n4  Delete File\n5  Back to Main Menu\n6  Close.")
			b = input("> ")
			if (not a == "5"):
				FileMenu(b)
			menu()
		if (a == "0"):
			print ("1  List all files by name.")
			print ("2  Read the contents of a file.")
			print ("3  Edit a file. For help, type '_help' at the prompt.")
			print ("4  Permenantly erase a file. (Be sure it is not in use.)")
			print ("5  Return to the Main Menu.")
			print ("6  End Session.")

		if (a == "1"):
			printFileList()
		if (a == "6"):
			exit()
		if (a == "2"):
			print(decrypt_file("Files/" +fileSelector()))
		if (a == "3"):
			openTextEditorMode("Files/" +fileSelector())
		if (a == "4"):
			os.remove("Files/" +fileSelector())
			print("Deleted.\n")
		input("Press Return (Enter) to return to the Files Menu.\n> ")
		a = "FileMenu"
	return 

def fileSelector():
	#get input and check for a match in the Files dir, if no match is found, recur
	l = os.listdir("Files")

	#get input
	s = input("Please select a file by typing it's name. You do not need to include the extension.\nType nothing to return to the File Menu.\n>  ") + ".txt"
	s = s.replace(".txt.txt", ".txt")

	if (s == ""): #no option given
		FileMenu("FileMenu")

	#edge case for edit mode
	if (s == "_help" or s == "_help.txt"):
		return s

	for i in l:
		if (s == i):
			return s
	print("\n'" + s + "' not found.")
	printFileList()
	return fileSelector()

def getFileList():
	l = os.listdir("Files")
	#REMOVE HIDDEN FILES
	for i in l:
		if (i[0] == '_' and i[1] == '_'):
			l.remove(i)
	return l

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
	return reverse(m)

def reverse(s):
	out = ""
	i = len(s)

	while (i > 0):
		i = i - 1
		out += s[i]
	return out

#ORG

def fileCleaner():
	print("Running the File Cleaner")
	l = getFileList()

	for i in l:
		if (i[0] == "_"):
			l.remove(i)
	l.append("_oneKey.txt")
	
	for i in l:
		path = "Files/" + i
		s = decrypt_file(path)
		Parts = s.split("\n\n") 


		if (len(Parts) < 2):
			return #the file has one key or less, no cleaning needed. 

		#convert file into (key, section) tuples, with a tuple for each key
		Tuples = []

		for i in Parts:
			t = (extractKeyFromLine(i.split("\n")[0]), i)
			if (not t[0] == None): #there should not be any "nones"
				Tuples.append(t)

		tuples = removeDuplicates(selectionSort(Tuples)) #do the cleaning 

		#convert tuples into file content
		encryptable = ""
		for i in range(0, len(tuples) - 1):
			encryptable += tuples[i][1] + "\n\n"
		encryptable += tuples[len(tuples) - 1][1]
		encrypt_to_file(path, encryptable)
	return 

def extractKeyFromLine(s):
	if(len((s).split("\t")) < 2):
		return
	return s.split("\t")[1]


# Function to do selection sort on tuples in an array, by element 0 of each tuple (yes, On^2)
def selectionSort(a):
	r = 0 #this will incremnt to last element, at which point the array is sorted
	while (r < len(a)):
		for i in range(0, r):
			if (a[r][0] < a[i][0]):
				#swap
				temp = a[r]
				a[r] = a[i]
				a[i] = temp
		r = r + 1
	return a 

def removeDuplicates(a):
	out = []
	temp = a[0][0]

	out.append(a[0])

	for i in a:
		if (not i[0] == temp):
			out.append(i)
			temp = i[0]
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

def openTextEditorMode(path):
	#if help is needed
	if (path == "_help"):
		f = open("Files/__helpEdit.txt", "w")
		encrypt_to_file("Files/__helpEdit.txt", "-EDIT MODE HELP-\n\nYou can edit a file in nano. Select the file by typing its name into the prompt. The file will be decrypted and written to \"_temp.txt\" for editing. When you are done editing, you will be prompted to save your edit. If you type no, your file will be unchanged. If you type yes, your file will be overwritten with the edit and encrypted. You can edit this file as much as you like. Try things out! Your edit will not be saved to this file.\n\nHOW TO USE NANO SHORTCUTS:\n\n ^G indicates that the control key and the g key can be pressed to use the shortcut. (You can also push esc twice and then push G) ^ means 'Control and...'\nM- means 'alt and...' Push alt and a key at the  same time to use those.\n\nUse ^G for more help, and ^X to exit and return to the File Menu.")
		path = "Files/__helpEdit.txt"
	s = openNano(decrypt_file(path))
	encrypt_to_file(path, s)
	return


def openNano(s):
	#I'm going to do my own saving prompt 
	f = open("_temp.txt", "w")
	f.write(s)
	f.close()
	print("Loading Text Editor (Nano).")
	subprocess.run(["wsl", "nano","_temp.txt", "-t"])
	f = open("_temp.txt", "r")
	n = f.read()
	f.close()
	os.remove("_temp.txt")
	a = YesOrNo("Would you like to save your edit? (y/n)?\n>  ")
	if (a):
		s = n
		print("Saved.")
	if (a):
		print("Cancelled.")

	return s

def openNanoMac(s):
	#I'm going to do my own saving prompt 
	f = open("_temp.txt", "w")
	f.write(s)
	f.close()
	print("Loading Text Editor (Nano).")
	subprocess.run(["nano","_temp.txt", "-t"])
	f = open("_temp.txt", "r")
	n = f.read()
	f.close()
	os.remove("_temp.txt")
	a = YesOrNo("Would you like to save your edit, yes or no (y/n)?\n>  ")
	if (a):
		s = n
		print("Saved.")
	if (not a):
		print("Cancelled.")

	return s

def YesOrNo(s):
	a = str(input(s) + "")
	try:
		return a.lstrip().lower()[0] == "y"
	except TypeError: #no input given means no
		return False

#TESTING
def test():
	a = [("fox", "content"), ("dog", "content"), ("Zap", "content"), ("zap", "content"), ("app", "content"), ("#$%^", "content"), ("app", "content"), ("pen", "content"), ("war", "content")]
	message = getRandMessage()

	#tupleSortNoDupsTest(a)
	#encrpytAndDecryptTest(message)
	#openTextEditorTest()
	#textColorTest()

	print("All tests are completed.")
	return

def getRandMessage():
	M = ["We're on some kind of mission. We have an obligation. We have to wear toupees!", " You was doing PIPI in your pampers when i was beating players much more stronger then you! ... And \"w\"esley \"s\"o is nobody for me, just a player who are crying every single time when loosing, ( remember what you say about Firouzja ) !!!", "ThE QuIck BrOwN fOx JuMpEd OvEr ThE LaZy DoG", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", "Namespaces are one honking great idea -- let's do more of those!"]
	return M[random.randint(0, len(M) - 1)]

def tupleSortNoDupsTest(a):
	print("---\nTUPLE SORT NO DUPS TEST:\n---")
	print(a)
	print("")
	print(removeDuplicates(selectionSort(a)))

def tupleSortTest(a):
	print("---\nTUPLE SORT TEST:\n---")
	print(a)
	print("")
	print(selectionSort(a))

def openTextEditorTest():
	f = open("_temp.txt", "w")
	f.write("LOVE THE CHICKENS")
	f.close()
	subprocess.run(["wsl", "nano","_temp.txt"])
	f = open("_temp.txt", "r")
	print(f.read())
	f.close()

	os.remove("_temp.txt")

	return

def encrpytAndDecryptTest(message):
	print("---\nENCRYPT AND DECRYPT TEST:\n---")
	message = getRandMessage()
	print("Message: " + message)
	encrypt_to_file("__testing.txt", message)
	f = open("__testing.txt", "r")
	print("\nEncrypted: " + f.read())
	print("\nDecrypted: " + decrypt_file("__testing.txt"))
	f.close()
	os.remove("__testing.txt")


def randomSampleFile(kOne):
	#this function is for testing the file cleaner
	kTwo = randomKey()
	for i in range (0, 20):
		if (random.randint(1, 3) == 2): 
			kTwo = randomKey() #for testing alphabetical sort and duplicate key deletion in the file cleaner
		r = (genResult(kOne, kTwo))
		saveTkToFile(kOne, kTwo, r)
def randomKey():
	SAMPLE_KEYS = '''
	Ray Charles Bille Holiday Evelyn Frank Apple Bananna Xavier Huzzah Test Java Mocha Cobra Pear
	Alto Soprano Tenor Tom Seven Robert Micheals Marty Dan Miller Beller Quote Cabbage Dessert Futon
	Pixelated Starfish Vella Cash Jones App Keybasket Key Lock Thread Race Condition Skidmore Echo 
	Quarter Dime Dollar Euro Swan Lion Donkey Dank Dusk Dawn Sun Moon Phone Light Dark Kiss Touch Hug
	Caress Shirt Pants Belt Socks Shoes Wolf Lana Del John Lennon Ampersand Third Amendment Linnel Pi
	Flansy Question Mark Cola Simon Scallop Zap Pow Bang Woosh Brush Your Teeth Eat Food Live Laugh Tau En
	Love Ball Small Call Tall Tufted Titmouse Cardinal Chickadee Blue Jay Yellow Green Purple Tea For Sigma
	Two Three Art Tatum Channel Soda Milk Orange Juice Ice King Queen Duke Jack Rook Pawn Bishop Castle Oct
	Dec Non Hex Sep Bi Mono Queer Peace On Earth Mercy Xmas Angels Chickens Hello World Good Goodbye Bye Buy
	Gifts Dog Cat Mouse Mercury Venus Earth Mars Jupiter Saturn Uranus Neptune Pluto Asteroid Star Space Corn
	Supreme Deluxe Alpha Bravo Charlie Delta Epsilon Foxtrot Golf Hotel Indigo Juliet Kilo Lima Bean Passant
	'''.replace("\n", "").split(" ")

	return SAMPLE_KEYS[random.randint(0, len(SAMPLE_KEYS) -1 )].replace("\t", "")

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
	traceback.print_exc() #comment this line out for stable versions
	if (DEBUG):
		traceback.print_exc()
	input("Error; press Return (Enter) to close.\n> ")

'''
KNOWN ISSUES
	Right now this is vunerable to over the shoulder attacks. Need some way to obfuscate text, by manipulating colors or something else.
	Powershell can handle colors, but it requires specific security clearances to use. Batch cannot handle colors

SPECIAL KEYS
	Note that a filename that begins with an underscore is reserved. Two underscores means hidden.
	^ is newline
	Edit mode now runs in nano, copy content to _temp and open it in nano. wsl is used to run nano in batch.

SOURCES
	Copy to Clipboard
	https://stackoverflow.com/questions/11063458/python-script-to-copy-text-to-clipboard
	
	Encryption
	https://www.geeksforgeeks.org/encoding-and-decoding-base64-strings-in-python/

	Get Current Working Dir
	https://note.nkmk.me/en/python-os-getcwd-chdir/
 	
 	License
 	https://choosealicense.com/
	
	Nano
	https://www.nano-editor.org/dist/latest/nano.html
	
	Text Color 
	https://www.geeksforgeeks.org/print-colors-python-terminal/
'''
