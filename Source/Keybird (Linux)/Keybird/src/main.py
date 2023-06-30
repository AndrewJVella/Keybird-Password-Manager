
#!/usr/bin/env python3
import random
import traceback
import os
import base64
import subprocess
import time
import pwinput

#2.4.2 has an installer!

##The Main Menu, with a welcome message##
def menu():
	global VERSION
	clear()
	while (True):
		print("Thank you for using the Keybird Password Manager (Linux Edition).\nVersion " +VERSION+ "\nCopyright 2022.\n\nThis is created by Andrew Vella.\nEmail:  andyjvella@gmail.com.\nGithub: @PixelatedStarfish\n\nPlease see the Disclaimer and License, before using this app.")
		a = dinput("\nType a number and press enter (return) to select an option:\n0  Help\n1  One Key Mode\n2  Two Key Mode\n3  Username Generator\n4  File Menu\n5  Settings Menu\n6  Disclaimer and License\n7  Erase Data\n8  Close\n> ")
		if (a == "-1"):
			test()
		if (a == "-2"):
			h = input("Generate sample files? You might lose data. (Type 'y' for yes.)\n")
			if (h[0].lower().lstrip() == 'y'):
				for i in range(10):
					randomSampleFile(randomKey())
		if (a == "0"):
			print(docs())
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
			clear()
			print(docs("legal"))
			
		if (a == "7"):
			clear()
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
					stressRelief()
				print("Done.")
				input("Press Return (Enter) to close.\n> ")
				exit()

				
		if (a == "8"):
			exit()
		input("Press Return (Enter) to return to the Main Menu.\n>")
		clear()


##This function runs the Two Key Mode## 
def twoKey():
	global KEY_LENGTH
	kOne = ""
	kTwo = ""

	clear()
	print("\nGive a Username Key. Be sure it is not easily guessed:\n")
	if (MASK):
		kOne = pwinput.pwinput(">>  ")[0:KEY_LENGTH]
	if (not MASK):
		kOne = input(">  ")[0:KEY_LENGTH]

	kTwo = input("\nGive a Site Key, such as a website name:\n> ")[0:KEY_LENGTH]
	if (len(kOne) == 0 or len(kTwo) == 0):
		print("One of the keys is empty: no result.")
		return
	if (kOne[0] == '_' or kTwo[0] == '_'):
		print("Keys cannot begin with underscores: no result.")
		return
	r = (genResult(kOne, kTwo))

	if (MASK):
		print("\nResult:\n" + ("*" * PASSWORD_LENGTH) + "\n")
	if (not MASK):
		print("\nResult:\n" + r + "\n")
	copyToclipMac(r)
	if (SAVE):
		saveTkToFile(kOne, kTwo, r)


##This function runs the One Key Mode## 
def oneKey():
	global MASK
	kOne = ""
	clear()
	print("\nGive a Key, such as a word you will remember. Be sure it is not easily guessed:\n")
	if (MASK):
		kOne = pwinput.pwinput(">>  ")[0:KEY_LENGTH]
	if (not MASK):
		kOne = input(">  ")[0:KEY_LENGTH]
	kTwo = "Default_Key_2"
	if (len(kOne) == 0):
		print("Key is empty: no result.")
		return
	if (kOne[0] == '_'):
		print("Keys cannot begin with underscores: no result.")
		return

	r = (genResult(kOne, kTwo))
	if (MASK):
		print("\nResult:\n" + ("*" * PASSWORD_LENGTH) + "\n")
	if (not MASK):
		print("\nResult:\n" + r + "\n")

	copyToclipMac(r)
	if (SAVE):
		saveOkToFile(kOne, r)


##This runs the hash function for One Key Mode and Two Key Mode. It maps passwords to keys.##
def genResult(key1, key2):
	global PASSWORD_LENGTH

	#set of all characters that can be in a password
	nums = list("1234567890")
	uppers = list("QWERTYUIOPASDFGHJKLZXCVBNM")
	lowers = list("qwertyuiopasdfghjklzxcvbnm")
	symbols = list("-_")
	
	#get new char sequence (result)
	s = ""
	while(len(s) < PASSWORD_LENGTH):
		s += key1[len(key1)//2:len(key1)] + key2[0:len(key2)//2] + key1[0:len(key1)//2] + key2[len(key2)//2:len(key2)] #weave keys together for increased variation
		while (len(s) < 64): #arbitrary buffer 
			s += s

	flipper = -1
	stuff = [nums, uppers, lowers, symbols]
	out = ""

	offsetKroll = 0  #as in Nick Kroll
	for c in s:
		flipper = flipper - (ord(c) % 3) #cycle through the four categories of characters
		flipper = flipper % 4
		out += stuff[flipper][(offsetKroll + ord(c)) % len(stuff[flipper])] #take letter from s, convert to number N, set N + O to itself mod list length, and get char N in list added to out, add N to O
		offsetKroll += ord(c)

	#offset is needed because the first three chars of a password are always identical if the same private key is used
	#So skip at least three characters ahead (and up to PASSWORD_LENGTH) according to the int value of the last char in the password	

	offsetMulaney = (ord(s[len(s) -1]) % PASSWORD_LENGTH) + 3 #as in John Mulaney; the first three chars are always the same, so the actual result is adjusted by an offset based on the least predictable letter (In file passwords... the first three characters are always the same). The offset lops off an (effectively) psuedo-random number of letters and gets the next 16 characters for a password. 


	#adjust to length
	return out[offsetMulaney:(PASSWORD_LENGTH + offsetMulaney)]

##Saves the data generated by Two Key Mode to an appropriate file.##
def saveTkToFile(kOne, kTwo, r):
	global MASK
	#this used to ask to save. Now it is a setting.
	h = 'y'
	if (h[0].lower().lstrip() == 'y'):
		content =  "\nSite Key:\t" + kTwo + "\nPassword:\t" + r + "\n"

		#make the file, if it exists, move on
		try:
			f = open("Files/" + kOne + ".txt", "x")
			if (not MASK):
				print("Created '" + kOne + ".txt'") 
			if (MASK):
				print("Created new file")
			f.close()
			encrypt_to_file("User key:\t" + "\n")
		except Exception:
			pass
		s = decrypt_file("Files/" + kOne + ".txt")
		s += content
		encrypt_to_file("Files/" + kOne + ".txt", s)

		if (not MASK):
			print("Added to '" + kOne + ".txt'")
		if (MASK):
			print("Added to file")
	

##Saves the data generated by One Key Mode to  "_oneKey.txt". ##
def saveOkToFile(kOne, r):
	
	h = 'y'
	if (h[0].lower().lstrip() == 'y'):
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
	

##The Username Genrator takes three phrases and splices three words together randomly.##
def genUserName():
	clear()
	print("Username Generator")
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

	#Display outlist and prompt for number to select.
	#If the selection is not in the list, run again, copy selection to clipboard and return

	i = 0 #again, a different i
	print("\nUsernames:")
	while (i < len(outList)):
		outList[i] = outList[i].replace("'", "")
		outList[i] = outList[i].replace('"', "")
		print(outList[i])
		i = i + 1
	print()
	

##For use in all yes or no questions##
def YesOrNo(s):
	a = str(input(s) + "")
	try:
		return a.lstrip().lower()[0] == "y"
	except Exception: #no input given means no
		return False
	
#SUBMENUS

##The Settings Menu. Toggle each setting on or off here.##
def SettingsMenu(a):
	while (not a == "4"):
		global SAVE
		global MASK
		if (a == "SettingsMenu"):
			clear()
			print("Settings Menu\n\n0  Help")
			print ("1  File Saving      (" + menuBooleanFormatter(SAVE) + ")")
			print ("2  Masking          (" + menuBooleanFormatter(MASK) + ")")
			print ("3  Retore Defaults\n4  Back to Main Menu\n5  Close")
			b = dinput("> ")
			if (not a == "4"):
				SettingsMenu(b)
			menu()

		if (a == "0"):
			print ("1  Toggle the option to save to a file.")
			print ("2  Toggle the option to mask passwords.")
			print ("3  Retore settings to default.\n4  Return to the Main Menu.\n5  End session.")

		if (a == "1"):
			SAVE = (not SAVE)
			print("Set to " + menuBooleanFormatter(SAVE))
		if (a == "2"):
			MASK = (not MASK)
			print("Set to " + menuBooleanFormatter(MASK))
		if (a == "1" or a == "2"):
			o = ""
			if (not SAVE and not MASK):
				o = "00"
			if (not SAVE and MASK):
				o = "01"
			if (SAVE and not MASK):
				o = "10"
			if (SAVE and MASK):
				o = "11"
		
			f = open("Files/__Settings.txt", "w") 
			f.write(o) 
			f.close()
			print("\nSaved.\n")

		if (a == "3"):
			SAVE = True
			MASK = True
			f = open("Files/__Settings.txt", "w") 
			f.write(defaultConstant())
			f.close()
			print("\nRestored.\n")
			
		if (a == "5"):
			exit()
	
		input("Press Return (Enter) to return to the Settings Menu.\n> ")
		a = "SettingsMenu"
	  

##The Files Menu. Read, edit, delete, and organize files.##
def FileMenu(a):
	while (not a == "7"):
		global SAVE
		global MASK
		if (a == "FileMenu"):
			clear()
			if (MASK):
				print ("\n*Please note that all text in this menu is not masked or hidden. All file content will be plainly visible.*")

			print("Files Menu\n\n0  Help\n1  List Files\n2  Read File\n3  Edit File\n4  Delete File\n5  Clean Files\n6  Use Notepad\n7  Back to Main Menu\n8  Close.")
			b = dinput("> ")
			if (not a == "7"):
				FileMenu(b)
			menu()
		if (a == "0"):
			print ("1  List all files by name.")
			print ("2  Read the contents of a file.")
			print ("3  Edit a file. For help, type '_help' at the prompt.")
			print ("4  Permenantly erase a file. (Be sure it is not in use.)")
			print ("5  Run the File Cleaner and organize keys.")
			print ("6  Open the notepad for use. The notepad is encrypted.")
			print ("7  Return to the Main Menu.")
			print ("8  End Session.")

		if (a == "1"):
			printFileList()
		if (a == "8"):
			exit()
		if (a == "2"):
			print(decrypt_file("Files/" +fileSelector()))
		if (a == "3"):
			openTextEditorMode("Files/" +fileSelector())
		if (a == "4"):
			os.remove("Files/" +fileSelector())
			print("Deleted.\n")
		if (a == "5"):
			fileCleaner()
			print("Done")
		if (a == "6"):
			print("Opening the notepad")
			openTextEditorMode("Files/__Notepad.txt")
		input("Press Return (Enter) to return to the Files Menu.\n> ")
		a = "FileMenu"
	 

##Open Edit Mode##
def openTextEditorMode(path):
	#if help is needed
	s = openNano(decrypt_file(path))
	if (not path == "Files/_help.txt"):
		encrypt_to_file(path, s)
		return
	encrypt_to_file(path, docs("nano")) #overwrite any edits to the nano help docs

##Ask the user for a file, and get it. If the file is not found, print the list of files.##
def fileSelector():
	#get input and check for a match in the Files dir, if no match is found, recur
	l = os.listdir("Files")

	#get input
	s = input("Please select a file by typing it's name. You do not need to include the extension.\nType nothing to return to the File Menu.\n>  ") + ".txt"
	s = s.replace(".txt.txt", ".txt")

	if (s == ".txt"): #no option given
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

##Generate and print a list of key files. Calls getFileList()##
def printFileList():
	l = getFileList()
	print("File List:")
	for i in l:
		print(i)
	

##Generates the list of key files.##
def getFileList():
	l = os.listdir("Files")
	#REMOVE HIDDEN FILES
	for i in l:
		if (i[0] == '_' and i[1] == '_'):
			l.remove(i)
	return l


#FILE CLEANER AND ORGANIZATION

##This cleans the files, sortng keys alphabetically and removing douplicated infomation.
#This is accomplished by creating (key, section) tuples, sorting the tuples by key, removing duplicates, and writing 
#each section to the file. This overwrites the previous version. FIles are decrypted at the start, and then encrypted.##
def fileCleaner():
	print("Running the File Cleaner")
	l = getFileList()

	for i in l:
		if (i[0] == "_"):
			l.remove(i)
	l.append("_oneKey.txt")
	
	for i in l:
		print("Cleaning " + i)
		stressRelief()
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
		encryptable = "" #file content before encrpytion as a string
		for i in range(0, len(tuples) - 1):
			encryptable += tuples[i][1] + "\n\n"
		encryptable += tuples[len(tuples) - 1][1]
		encryptable = encryptable.replace("\n\n\n", "\n\n") #triple newlines appear for some reason, have a bandaid!
		encrypt_to_file(path, encryptable)
		
	 
##extracts a key from a line of text that has a key in it.##
def extractKeyFromLine(s):
	if(len((s).split("\t")) < 2):
		return 
	return s.split("\t")[1]

##If you close the shell window while running nano, a .save file will be left over in src. This deletes them.##
def cleanNanoDroppings():
	l = os.listdir()
	for i in l:
		t = i.split(".") 
		if (t[len(t)-1] == "save"):
			os.remove(i)
	

##Function to do selection sort on tuples in an array, by element 0 of each tuple (yes, On^2)##
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

##Removes duplicate tuples in a sorted list##
def removeDuplicates(a):
	out = []
	temp = a[0][0]

	out.append(a[0])

	for i in a:
		if (not i[0] == temp):
			out.append(i)
			temp = i[0]
	return out

#FORMATTING
##This function is used by the settings menu to indicate that status of a setting##
def menuBooleanFormatter(b):
	if (b):
		return "ON"
	return "OFF"

##This constant stores default settings as bits (pedantically, characters) SAVE, DEBUG, MASK.##
def defaultConstant(): 
	return "11"

#ENCRYPTION AND DECRYPTION

##Encrypts a string to a reversed base64 string and wrties to a file. This is not secure from attacks, it prevents accidents.##
def encrypt_to_file(path, message):
	global ENCODING
	message = reverse(message)
	string_bytes = message.encode(ENCODING)
	base64_bytes = base64.b64encode(string_bytes)
	base64_string = base64_bytes.decode(ENCODING)

	f = open(path, "w")
	f.write(base64_string)
	f.close()
	
##Decrypts a file from a reversed base64 string. This returns a string.##
def decrypt_file(path):
	global ENCODING
	f = open(path, "r")
	base64_string = f.read()
	base64_bytes = base64_string.encode(ENCODING)
	string_bytes = base64.b64decode(base64_bytes)
	m = string_bytes.decode(ENCODING)
	return reverse(m)

##Function to reverse a string.##
def reverse(s):
	out = ""
	i = len(s)

	while (i > 0):
		i = i - 1
		out += s[i]
	return out

#DOCS
##Prints sections of the ducmentation where they are needed. Pass "legal" for the legal. Pass "nano" for nano 
#instructions. Pass nothing for the entire documentation.##
def docs(b = "all"):
	legal = '''
-LEGAL-
Disclaimer:
No information produced in whole or part by this app is guaranteed to be perfectly safe. Your files
can be read, modified, or deleted. The app source code can also be read, modified, or deleted, which would cause
unpredictable effects while running the app. Back up important things; store your passwords in a few safe places.
Keep untrustworthy people off your computer. Do not store your passwords publicly, or generate them with keys
that are easy to guess. Stay safe!

No birds were harmed in the making of Keybird, including the program, online material, documentation, and photography. 
Wild robins were photographed eating berries from a park tree.

License:
MIT License

Copyright (c) 2022 Andrew Vella

Permission is hereby granted, free of charge, to any person obtaining  a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
			''' 
	nano = '''
-EDIT MODE (HOW TO USE NANO)-
Nano is a text editor that runs on linux. It can also run on the Windows Linux Subsystem. Keybird uses nano to edit
the (unencrypted) contents of a file. The File Edit Mode opens the nano text editor after writing unencrypted file
contents to the file "_temp.txt". You can type "_help" into Edit Mode in the File Menu to load this section of the
documentation into nano. Edits to this document will not be saved, so you can experiment freely.

A short guide to shortcuts:
^G  means "press ctrl and G at the same time to use this shortcut" you can also press esc twice and then G
M-G means "press alt and G at the same time to use this shortcut"

Note that G can be substituted for any letter to get another shortcut. You should see a list of them at the bottom of
this window. ^X exits the nano editor and returns to Keybird. For more information use ^G.

Important Operations:
^G -- Help
^X -- Exit; go back to Keybird
Up and Down arrows -- Scroll
M-U -- Undo
M-E -- Redo

Upon finishing your edit and exiting, you will be asked if you want to save your edit. Type "yes" or "y" to save your
edit to the file you have selected. The file will be overwritten by the edit and encrypted. Type "no" or "n" to cancel
the edit. 
	'''
	s= '''
-INSTALL-
To download from Github select the zip file "Keybird", click on it, then click "view raw" or the download button.

This is the Linux Edition. If you would like to install Ubuntu, you can do so here:
https://ubuntu.com/tutorials/install-ubuntu-desktop#1-overview

(If you know more than I do and are rolling your eyes at these instructions, email me nicely about your way!)
If you click on this file, after extraction. It will create a Keybird directory, install pip and pwinput and
write the main source file in Keybird/src. You can stop there if that works for you.

For installation on a virtual environment, (ie Ubuntu) copy the content of the installation file, open Ubuntu
cd into the directory of your choice and do the following:
cat > install.sh
(Right click to paste)
control, shift, D (or command, shift, D) push all 3 keys at once.
bash ./install.sh

That's it. The ls command should show you a Keybird directory.

-WELCOME TO KEYBIRD-
The purpose of Keybird is to improve the accessibility of password managers without compromising security.
You need lots of passwords, but making them is tedious. Repeating passwords reduces their effectiveness. In-browser
managers are fine until they lock you out.

You may ask yourself:
"What was my password again?"
"Why does Safari fill in the wrong info?"
"Did I make this account on Google?"

Skip that nonsense, use Keybird.

Keybird is designed to generate and store passwords on your computer. While other managers integrate with your browser,
they are much better for accumulating passwords than actually managing them. At worst you can become dependant on a
specific browser to access your stuff. At best you might still use a small number of passwords you wrote yourself for
the important stuff, which puts the important stuff at risk.

My thinking is that 100 auto-generated passwords is bad, a small number of manually created passwords is worse, and
both of these together is what often happens. Instead of coming up with a few complicated passwords and using them
everywhere, depending on a browser extension, or (most likely) both. You can use Keybird to generate secure
passwords from simple keys, that are easy to create and remember.

-FEATURES-
Accessibility:
To prevent flashing lights, loading screens cannot update within the span of one third of a second.
Also updates to a process, such as modifying files, also cannot update within the span of one third of a second.
The a, s, d, f, g, h, j, k, and l keys map to 0 through 8. So you can use Keybird in the dark without issue.
(Note that an update is text printed to the screen.)

Keys:
This app uses keys to make passwords. The keys are easy to remember. The passwords are secure.
Keys are 16 characters max.
Passwords are 16 characters.

Two Key Mode:
Keybird has a Two Key Mode. One private key and many public keys. The public keys can be website names. You can have
many passwords and you only need to remember one key.

Username Generator:
The Username Generator helps you think of usernames. It asks you three questions, and generates names from your
answers.

Files:
Files store passwords and keys. They are encrypted to prevent accidents. Files are cleaned at start up. They are
alphabetized by key and duplicate info is deleted. Files can also be edited in the nano text editor.

Settings:
Toggle file saving
Toggle masking, which covers private stuff.
Toggle debug mode, which prints errors.

Notepad:
A notepad file is editable from the File Menu. Store usernames, passwords, and other things here and they will be
encrypted in the same manner as other files (protection from accidents, not attacks).

Web Repl:
Use the repl when you leave this app at home. If you need a password quickly, use your key. Nothing is saved on the
repl.\n'''+ nano +'''
-GITHUB-
https://github.com/PixelatedStarfish/Keybird-Password-Manager

-WEB REPL-
https://pixelatedstarfish.github.io/Keybird-Password-Manager/

-INDICATORS-
Note that a filename that begins with an underscore is reserved.
Two underscores means the file is hidden.
> Indicates input
>> Masked input

-TESTS-
Tests are written into the source.
At the main menu select the following:
-1 for general testing purposes
-2 to generate sample files

	''' + legal + '''
-SOURCES-
Clear Screen
https://www.csestack.org/clear-python-interpreter-console/
Copy to Clipboard
https://stackoverflow.com/questions/11063458/python-script-to-copy-text-to-clipboard
Documentation Conventions
https://peps.python.org/pep-0257/
Encryption
https://www.geeksforgeeks.org/encoding-and-decoding-base64-strings-in-python/
Flashing Lights Guidelines
https://www.accessguide.io/guide/flashing-lights
Get Current Working Directory
https://note.nkmk.me/en/python-os-getcwd-chdir/
License
https://choosealicense.com/
Nano
https://www.nano-editor.org/dist/latest/nano.html
Password Masking
https://stackoverflow.com/questions/9202224/getting-a-hidden-password-input

-ERRORS AND DEBUG-
Errors happen, and a well designed program can handle them fairly well There are two kinds of errors that Keybird is
designed to handle:

A Permission Error - these occur when Keybird attempts to modify a file that is open or in use.
A General Error    - these occur when Keybird functions incorrectly.

Errors are reported in Python3 as tracebacks through the call stack. The line number and function in source are shown
as well as the type of error that occurred. Sometimes errors occur while an error is being handled, in this case a
message will indicate as such, and more information will be printed.

In typical use the traceback will not be printed. You will be given a prompt that indicates an error has occurred and
you can close the app by pressing enter (return). Type "debug", "traceback", or "report" into the error prompt
to get the debug info. That said, I want to keep the error message as simple as I can, to prevent needless confusion. 
No one wants to see a wall of text when they are trying to understand what just happened! 

You are certainly welcome to reach out to me regarding an error in Keybird. I would appreciate your time.
You can reach out by email, Github, or Itch.

To email me, please use the subject line "Keybird Error Report" tell me about what happened and what you were
doing when the error occurred. You can include the traceback if you have one. I will try to reproduce the error
in a test and attempt to debug it. I will reply to you and update the Github and Itch pages. Programs and apps
need maintenance over time. Python, batch, and your operating system will be updated and changed over time.

Please be kind to me in your emails and other communications. I am a person, and I want to be treated like one.
I do not take responsibility for damages or inconveniences that result from the use of Keybird. That is what
the legal section is for, after all. I hope you find Keybird useful, simple, and enjoyable. Good luck!

-NOTES-
Keybird is written in Python3 and Batch for Windows.
Keybird is open source.\nVersion ''' + VERSION + '''
Developed by Andrew Vella
Copyright (c) 2022
@PixelatedStarfish on Github and Itch
andyjvella@gmail.com
Thank you for using Keybird!
	'''

	if (b == "all"):
		return s
	if(b == "legal"):
		return legal
	if(b == "nano"):
		return nano
	return None


#SHELL
##Copy string to clipboard so it can be pasted on Windows.##
def copyToclipX(txt):
	print("\nCopied to Clipboard.") #technically a lie but the message needs to print before the function ends.
	cmd='echo '+txt.strip()+'|clip'
	return subprocess.check_call(cmd, shell=True)

##Copy string to clipboard so it can be pasted on Mac.##
def copyToclipMac(txt):
	print("\nCopied to Clipboard.") #technically a lie but the message needs to print before the function ends.
	cmd='echo '+txt.strip()+'|pbcopy'
	return subprocess.check_call(cmd, shell=True)

##Open nano on Windows##
def openNanoPC(s):
	#I'm going to do my own saving prompt 
	f = open("_temp.txt", "w")
	f.write(s)
	f.close()
	clear()
	print("*Loading Nano*")
	print(docs("nano"))
	print("*Loading Nano*")
	stressRelief()
	subprocess.run(["wsl", "nano","_temp.txt", "-t"])
	f = open("_temp.txt", "r")
	n = f.read()
	f.close()
	os.remove("_temp.txt")
	stressRelief()
	clear()
	a = YesOrNo("Would you like to save your edit? (y/n)?\n>  ")
	if (a):
		s = n
		print("Saved.")
	if (not a):
		print("Your edit is cancelled.")

	return s

##Open nano on Mac##
def openNano(s):
	#I'm going to do my own saving prompt 
	f = open("_temp.txt", "w")
	f.write(s)
	f.close()
	clear()
	print("*Loading Nano*")
	print(docs("nano"))
	print("*Loading Nano*")
	stressRelief()
	subprocess.run(["nano","_temp.txt", "-t"])
	f = open("_temp.txt", "r")
	n = f.read()
	f.close()
	os.remove("_temp.txt")
	stressRelief()
	clear()
	a = YesOrNo("Would you like to save your edit? (y/n)?\n>  ")
	if (a):
		s = n
		print("Saved.")
	if (not a):
		print("Cancelled.")

	return s
##Clear shell on Windows##
def clearPC():
	os.system('cls')
	

##Clear shell on Mac##
def clear():
	os.system('clear')
	
#ACCESSIBILITY
def dinput(s):
	##In the dark, you can use the home row instead of groping for numbers and hitting function keys.##
	a = input(s)

	if (a.lower() == "a"):
		a = "0"
	if (a.lower() == "s"):
		a = "1"
	if (a.lower() == "d"):
		a = "2"
	if (a.lower() == "f"):
		a = "3"
	if (a.lower() == "g"):
		a = "4"
	if (a.lower() == "h"):
		a = "5"
	if (a.lower() == "j"):
		a = "6"
	if (a.lower() == "k"):
		a = "7"
	if (a.lower() == "l"):
		a = "8"
	return a

##Prevents flashing lights by ensures updates cannot ahppen within the span of a third of a second.##
def stressRelief():
	#extends process times by a random fraction of a second when used.
	#The purpose is to keep text from flashing and disappering quickly.
	
	#gap = random.randint(3, 4) for variation if needed
	
	time.sleep(.3 / 10) # gap / 10 (if needed for variation)
	


#TESTING
##These are all self explanatory.##
def test():
	#a = [("fox", "content"), ("dog", "content"), ("Zap", "content"), ("zap", "content"), ("app", "content"), ("#$%^", "content"), ("app", "content"), ("pen", "content"), ("war", "content")]
	#message = getRandMessage()

	print("All tests are completed.")

def maskedInputTest():
	d = pwinput.pwinput()
	print(d)

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
		i = i #pylint is not the best...
		stressRelief()
		if (random.randint(1, 3) == 2): 
			kTwo = randomKey() #for testing alphabetical sort and duplicate key deletion in the file cleaner
		r = (genResult(kOne, kTwo))
		saveTkToFile(kOne, kTwo, r)

def randomKey():
	SAMPLE_KEYS = '''
	Ray Charles Bille Holiday Evelyn Frank Apple Bananna Xavier Huzzah Test Java Mocha Cobra Pear
	Alto Soprano Tenor Tom Seven Robert Micheals Marty Dan Miller Beller Quote Cabbage Dessert Futon Big
	Pixelated Starfish Vella Cash Jones App Keybasket Key Lock Thread Race Condition Skidmore Echo Jolly
	Quarter Dime Dollar Euro Swan Lion Donkey Dank Dusk Dawn Sun Moon Phone Light Dark Kiss Touch Hug Pie
	Caress Shirt Pants Belt Socks Shoes Wolf Lana Del John Lennon Ampersand Third Amendment Linnel Pi Tau
	Flansy Question Mark Cola Simon Scallop Zap Pow Bang Woosh Brush Your Teeth Eat Food Live Laugh Tau En
	Love Ball Small Call Tall Tufted Titmouse Cardinal Chickadee Blue Jay Yellow Green Purple Tea For Sigma
	Two Three Art Tatum Channel Soda Milk Orange Juice Ice King Queen Duke Jack Rook Pawn Bishop Castle Oct
	Dec Non Hex Sep Bi Mono Queer Peace On Earth Mercy Xmas Angels Chickens Hello World Good Goodbye Bye Buy
	Gifts Dog Cat Mouse Mercury Venus Earth Mars Jupiter Saturn Uranus Neptune Pluto Asteroid Star Space Corn
	Supreme Deluxe Alpha Bravo Charlie Delta Epsilon Foxtrot Golf Hotel Indigo Juliet Kilo Lima Bean Passant
	Roof Tooth Hand Foot Mourning Dove Chick Raptor Claw Talon Qwerty Typewriter Type Writer Pan Pot Handle
	Brush Blush Breath Birth Ear Dear Clear Cheer Razor Candy Goth Morse Horse Bikes Likes Calmed Palmed Up
	'''.replace("\n", "").split(" ")

	return SAMPLE_KEYS[random.randint(0, len(SAMPLE_KEYS) -1 )].replace("\t", "")

#MAIN 
##This function loads settings the file "__Settings.txt" including file saving, debug mode, and password masking.##
def getSettings():
	global SAVE
	global MASK
	f = open("Files/__Settings.txt", "r")
	s = f.read()
	f.close()
	if (s[0] == "0"):
		SAVE = False
	if (s[0] == "1"):
		SAVE = True
	if (s[1] == "0"):
		MASK = False
	if (s[1] == "1"):
		MASK = True

##Configure and run the Keybird App and handle errors.##
def main():
	try: 
		print("Loading Working Directory.")
		#set cwd to source file
		os.chdir(os.path.dirname(os.path.abspath(__file__)))
		stressRelief()
		print("Loading Files.")

		#make Files dir if it does not exist
		try:
			os.mkdir("Files")
		except Exception:
			pass
		try:
			open("Files/_oneKey.txt", "x") 
		except Exception:
			pass
		try:
			open("Files/__Notepad.txt", "x") 
		except Exception:
			pass
		try:
			f = open("Files/__Settings.txt", "r") 
			f.close()
		except FileNotFoundError:
			f = open("Files/__Settings.txt", "x") 
			f.write(defaultConstant())
			
			f.close()
			pass
		try:
			global KEY_LENGTH
			global PASSWORD_LENGTH
			encrypt_to_file("Files/_help.txt", docs("nano")) #get the Nano section of the docs only
		except Exception:
			pass
		stressRelief()
		print("Loading Settings.")
		getSettings()
		stressRelief()
		fileCleaner() #File cleaner text printed in this function
		cleanNanoDroppings() #closing the app while nano is running leaves a .save file in src, this .save needs to be deleted
		stressRelief()
		print("Ready.\n----")
		stressRelief()
		#run the menu
		menu()
	except PermissionError:
		print("Access denied. Files may need to be closed in another application first.")
		input("Error; press Return (Enter) to close.\n> ")
	
	except Exception:
		d = input("Error; press Return (Enter) to close.\n> ")
		if (d.lower().lstrip() == "debug" or d.lower().lstrip() == "traceback" or d.lower().lstrip() == "report"):
			traceback.print_exc()
			input("Press Return (Enter) to close.\n> ")
	

##Program Starts Here## 
print("Initializing.") 

#globals
SAVE = True
MASK = True
KEY_LENGTH = 16
PASSWORD_LENGTH = 16
ENCODING = "utf_8" #for encryption
VERSION = "2.4.2" #Keybasket 2.0
main()



#!/usr/bin/env python3
import random
import traceback
import os
import base64
import subprocess
import time
import pwinput

#2.4.2 has an installer!

##The Main Menu, with a welcome message##
def menu():
	global VERSION
	clear()
	while (True):
		print("Thank you for using the Keybird Password Manager (Linux Edition).\nVersion " +VERSION+ "\nCopyright 2022.\n\nThis is created by Andrew Vella.\nEmail:  andyjvella@gmail.com.\nGithub: @PixelatedStarfish\n\nPlease see the Disclaimer and License, before using this app.")
		a = dinput("\nType a number and press enter (return) to select an option:\n0  Help\n1  One Key Mode\n2  Two Key Mode\n3  Username Generator\n4  File Menu\n5  Settings Menu\n6  Disclaimer and License\n7  Erase Data\n8  Close\n> ")
		if (a == "-1"):
			test()
		if (a == "-2"):
			h = input("Generate sample files? You might lose data. (Type 'y' for yes.)\n")
			if (h[0].lower().lstrip() == 'y'):
				for i in range(10):
					randomSampleFile(randomKey())
		if (a == "0"):
			print(docs())
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
			clear()
			print(docs("legal"))
			
		if (a == "7"):
			clear()
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
					stressRelief()
				print("Done.")
				input("Press Return (Enter) to close.\n> ")
				exit()

				
		if (a == "8"):
			exit()
		input("Press Return (Enter) to return to the Main Menu.\n>")
		clear()


##This function runs the Two Key Mode## 
def twoKey():
	global KEY_LENGTH
	kOne = ""
	kTwo = ""

	clear()
	print("\nGive a Username Key. Be sure it is not easily guessed:\n")
	if (MASK):
		kOne = pwinput.pwinput(">>  ")[0:KEY_LENGTH]
	if (not MASK):
		kOne = input(">  ")[0:KEY_LENGTH]

	kTwo = input("\nGive a Site Key, such as a website name:\n> ")[0:KEY_LENGTH]
	if (len(kOne) == 0 or len(kTwo) == 0):
		print("One of the keys is empty: no result.")
		return
	if (kOne[0] == '_' or kTwo[0] == '_'):
		print("Keys cannot begin with underscores: no result.")
		return
	r = (genResult(kOne, kTwo))

	if (MASK):
		print("\nResult:\n" + ("*" * PASSWORD_LENGTH) + "\n")
	if (not MASK):
		print("\nResult:\n" + r + "\n")
	copyToclipMac(r)
	if (SAVE):
		saveTkToFile(kOne, kTwo, r)


##This function runs the One Key Mode## 
def oneKey():
	global MASK
	kOne = ""
	clear()
	print("\nGive a Key, such as a word you will remember. Be sure it is not easily guessed:\n")
	if (MASK):
		kOne = pwinput.pwinput(">>  ")[0:KEY_LENGTH]
	if (not MASK):
		kOne = input(">  ")[0:KEY_LENGTH]
	kTwo = "Default_Key_2"
	if (len(kOne) == 0):
		print("Key is empty: no result.")
		return
	if (kOne[0] == '_'):
		print("Keys cannot begin with underscores: no result.")
		return

	r = (genResult(kOne, kTwo))
	if (MASK):
		print("\nResult:\n" + ("*" * PASSWORD_LENGTH) + "\n")
	if (not MASK):
		print("\nResult:\n" + r + "\n")

	copyToclipMac(r)
	if (SAVE):
		saveOkToFile(kOne, r)


##This runs the hash function for One Key Mode and Two Key Mode. It maps passwords to keys.##
def genResult(key1, key2):
	global PASSWORD_LENGTH

	#set of all characters that can be in a password
	nums = list("1234567890")
	uppers = list("QWERTYUIOPASDFGHJKLZXCVBNM")
	lowers = list("qwertyuiopasdfghjklzxcvbnm")
	symbols = list("-_")
	
	#get new char sequence (result)
	s = ""
	while(len(s) < PASSWORD_LENGTH):
		s += key1[len(key1)//2:len(key1)] + key2[0:len(key2)//2] + key1[0:len(key1)//2] + key2[len(key2)//2:len(key2)] #weave keys together for increased variation
		while (len(s) < 64): #arbitrary buffer 
			s += s

	flipper = -1
	stuff = [nums, uppers, lowers, symbols]
	out = ""

	offsetKroll = 0  #as in Nick Kroll
	for c in s:
		flipper = flipper - (ord(c) % 3) #cycle through the four categories of characters
		flipper = flipper % 4
		out += stuff[flipper][(offsetKroll + ord(c)) % len(stuff[flipper])] #take letter from s, convert to number N, set N + O to itself mod list length, and get char N in list added to out, add N to O
		offsetKroll += ord(c)

	#offset is needed because the first three chars of a password are always identical if the same private key is used
	#So skip at least three characters ahead (and up to PASSWORD_LENGTH) according to the int value of the last char in the password	

	offsetMulaney = (ord(s[len(s) -1]) % PASSWORD_LENGTH) + 3 #as in John Mulaney; the first three chars are always the same, so the actual result is adjusted by an offset based on the least predictable letter (In file passwords... the first three characters are always the same). The offset lops off an (effectively) psuedo-random number of letters and gets the next 16 characters for a password. 


	#adjust to length
	return out[offsetMulaney:(PASSWORD_LENGTH + offsetMulaney)]

##Saves the data generated by Two Key Mode to an appropriate file.##
def saveTkToFile(kOne, kTwo, r):
	global MASK
	#this used to ask to save. Now it is a setting.
	h = 'y'
	if (h[0].lower().lstrip() == 'y'):
		content =  "\nSite Key:\t" + kTwo + "\nPassword:\t" + r + "\n"

		#make the file, if it exists, move on
		try:
			f = open("Files/" + kOne + ".txt", "x")
			if (not MASK):
				print("Created '" + kOne + ".txt'") 
			if (MASK):
				print("Created new file")
			f.close()
			encrypt_to_file("User key:\t" + "\n")
		except Exception:
			pass
		s = decrypt_file("Files/" + kOne + ".txt")
		s += content
		encrypt_to_file("Files/" + kOne + ".txt", s)

		if (not MASK):
			print("Added to '" + kOne + ".txt'")
		if (MASK):
			print("Added to file")
	

##Saves the data generated by One Key Mode to  "_oneKey.txt". ##
def saveOkToFile(kOne, r):
	
	h = 'y'
	if (h[0].lower().lstrip() == 'y'):
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
	

##The Username Genrator takes three phrases and splices three words together randomly.##
def genUserName():
	clear()
	print("Username Generator")
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

	#Display outlist and prompt for number to select.
	#If the selection is not in the list, run again, copy selection to clipboard and return

	i = 0 #again, a different i
	print("\nUsernames:")
	while (i < len(outList)):
		outList[i] = outList[i].replace("'", "")
		outList[i] = outList[i].replace('"', "")
		print(outList[i])
		i = i + 1
	print()
	

##For use in all yes or no questions##
def YesOrNo(s):
	a = str(input(s) + "")
	try:
		return a.lstrip().lower()[0] == "y"
	except Exception: #no input given means no
		return False
	
#SUBMENUS

##The Settings Menu. Toggle each setting on or off here.##
def SettingsMenu(a):
	while (not a == "4"):
		global SAVE
		global MASK
		if (a == "SettingsMenu"):
			clear()
			print("Settings Menu\n\n0  Help")
			print ("1  File Saving      (" + menuBooleanFormatter(SAVE) + ")")
			print ("2  Masking          (" + menuBooleanFormatter(MASK) + ")")
			print ("3  Retore Defaults\n4  Back to Main Menu\n5  Close")
			b = dinput("> ")
			if (not a == "4"):
				SettingsMenu(b)
			menu()

		if (a == "0"):
			print ("1  Toggle the option to save to a file.")
			print ("2  Toggle the option to mask passwords.")
			print ("3  Retore settings to default.\n4  Return to the Main Menu.\n5  End session.")

		if (a == "1"):
			SAVE = (not SAVE)
			print("Set to " + menuBooleanFormatter(SAVE))
		if (a == "2"):
			MASK = (not MASK)
			print("Set to " + menuBooleanFormatter(MASK))
		if (a == "1" or a == "2"):
			o = ""
			if (not SAVE and not MASK):
				o = "00"
			if (not SAVE and MASK):
				o = "01"
			if (SAVE and not MASK):
				o = "10"
			if (SAVE and MASK):
				o = "11"
		
			f = open("Files/__Settings.txt", "w") 
			f.write(o) 
			f.close()
			print("\nSaved.\n")

		if (a == "3"):
			SAVE = True
			MASK = True
			f = open("Files/__Settings.txt", "w") 
			f.write(defaultConstant())
			f.close()
			print("\nRestored.\n")
			
		if (a == "5"):
			exit()
	
		input("Press Return (Enter) to return to the Settings Menu.\n> ")
		a = "SettingsMenu"
	  

##The Files Menu. Read, edit, delete, and organize files.##
def FileMenu(a):
	while (not a == "7"):
		global SAVE
		global MASK
		if (a == "FileMenu"):
			clear()
			if (MASK):
				print ("\n*Please note that all text in this menu is not masked or hidden. All file content will be plainly visible.*")

			print("Files Menu\n\n0  Help\n1  List Files\n2  Read File\n3  Edit File\n4  Delete File\n5  Clean Files\n6  Use Notepad\n7  Back to Main Menu\n8  Close.")
			b = dinput("> ")
			if (not a == "7"):
				FileMenu(b)
			menu()
		if (a == "0"):
			print ("1  List all files by name.")
			print ("2  Read the contents of a file.")
			print ("3  Edit a file. For help, type '_help' at the prompt.")
			print ("4  Permenantly erase a file. (Be sure it is not in use.)")
			print ("5  Run the File Cleaner and organize keys.")
			print ("6  Open the notepad for use. The notepad is encrypted.")
			print ("7  Return to the Main Menu.")
			print ("8  End Session.")

		if (a == "1"):
			printFileList()
		if (a == "8"):
			exit()
		if (a == "2"):
			print(decrypt_file("Files/" +fileSelector()))
		if (a == "3"):
			openTextEditorMode("Files/" +fileSelector())
		if (a == "4"):
			os.remove("Files/" +fileSelector())
			print("Deleted.\n")
		if (a == "5"):
			fileCleaner()
			print("Done")
		if (a == "6"):
			print("Opening the notepad")
			openTextEditorMode("Files/__Notepad.txt")
		input("Press Return (Enter) to return to the Files Menu.\n> ")
		a = "FileMenu"
	 

##Open Edit Mode##
def openTextEditorMode(path):
	#if help is needed
	s = openNano(decrypt_file(path))
	if (not path == "Files/_help.txt"):
		encrypt_to_file(path, s)
		return
	encrypt_to_file(path, docs("nano")) #overwrite any edits to the nano help docs

##Ask the user for a file, and get it. If the file is not found, print the list of files.##
def fileSelector():
	#get input and check for a match in the Files dir, if no match is found, recur
	l = os.listdir("Files")

	#get input
	s = input("Please select a file by typing it's name. You do not need to include the extension.\nType nothing to return to the File Menu.\n>  ") + ".txt"
	s = s.replace(".txt.txt", ".txt")

	if (s == ".txt"): #no option given
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

##Generate and print a list of key files. Calls getFileList()##
def printFileList():
	l = getFileList()
	print("File List:")
	for i in l:
		print(i)
	

##Generates the list of key files.##
def getFileList():
	l = os.listdir("Files")
	#REMOVE HIDDEN FILES
	for i in l:
		if (i[0] == '_' and i[1] == '_'):
			l.remove(i)
	return l


#FILE CLEANER AND ORGANIZATION

##This cleans the files, sortng keys alphabetically and removing douplicated infomation.
#This is accomplished by creating (key, section) tuples, sorting the tuples by key, removing duplicates, and writing 
#each section to the file. This overwrites the previous version. FIles are decrypted at the start, and then encrypted.##
def fileCleaner():
	print("Running the File Cleaner")
	l = getFileList()

	for i in l:
		if (i[0] == "_"):
			l.remove(i)
	l.append("_oneKey.txt")
	
	for i in l:
		print("Cleaning " + i)
		stressRelief()
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
		encryptable = "" #file content before encrpytion as a string
		for i in range(0, len(tuples) - 1):
			encryptable += tuples[i][1] + "\n\n"
		encryptable += tuples[len(tuples) - 1][1]
		encryptable = encryptable.replace("\n\n\n", "\n\n") #triple newlines appear for some reason, have a bandaid!
		encrypt_to_file(path, encryptable)
		
	 
##extracts a key from a line of text that has a key in it.##
def extractKeyFromLine(s):
	if(len((s).split("\t")) < 2):
		return 
	return s.split("\t")[1]

##If you close the shell window while running nano, a .save file will be left over in src. This deletes them.##
def cleanNanoDroppings():
	l = os.listdir()
	for i in l:
		t = i.split(".") 
		if (t[len(t)-1] == "save"):
			os.remove(i)
	

##Function to do selection sort on tuples in an array, by element 0 of each tuple (yes, On^2)##
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

##Removes duplicate tuples in a sorted list##
def removeDuplicates(a):
	out = []
	temp = a[0][0]

	out.append(a[0])

	for i in a:
		if (not i[0] == temp):
			out.append(i)
			temp = i[0]
	return out

#FORMATTING
##This function is used by the settings menu to indicate that status of a setting##
def menuBooleanFormatter(b):
	if (b):
		return "ON"
	return "OFF"

##This constant stores default settings as bits (pedantically, characters) SAVE, DEBUG, MASK.##
def defaultConstant(): 
	return "11"

#ENCRYPTION AND DECRYPTION

##Encrypts a string to a reversed base64 string and wrties to a file. This is not secure from attacks, it prevents accidents.##
def encrypt_to_file(path, message):
	global ENCODING
	message = reverse(message)
	string_bytes = message.encode(ENCODING)
	base64_bytes = base64.b64encode(string_bytes)
	base64_string = base64_bytes.decode(ENCODING)

	f = open(path, "w")
	f.write(base64_string)
	f.close()
	
##Decrypts a file from a reversed base64 string. This returns a string.##
def decrypt_file(path):
	global ENCODING
	f = open(path, "r")
	base64_string = f.read()
	base64_bytes = base64_string.encode(ENCODING)
	string_bytes = base64.b64decode(base64_bytes)
	m = string_bytes.decode(ENCODING)
	return reverse(m)

##Function to reverse a string.##
def reverse(s):
	out = ""
	i = len(s)

	while (i > 0):
		i = i - 1
		out += s[i]
	return out

#DOCS
##Prints sections of the ducmentation where they are needed. Pass "legal" for the legal. Pass "nano" for nano 
#instructions. Pass nothing for the entire documentation.##
def docs(b = "all"):
	legal = '''
-LEGAL-
Disclaimer:
No information produced in whole or part by this app is guaranteed to be perfectly safe. Your files
can be read, modified, or deleted. The app source code can also be read, modified, or deleted, which would cause
unpredictable effects while running the app. Back up important things; store your passwords in a few safe places.
Keep untrustworthy people off your computer. Do not store your passwords publicly, or generate them with keys
that are easy to guess. Stay safe!

No birds were harmed in the making of Keybird, including the program, online material, documentation, and photography. 
Wild robins were photographed eating berries from a park tree.

License:
MIT License

Copyright (c) 2022 Andrew Vella

Permission is hereby granted, free of charge, to any person obtaining  a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
			''' 
	nano = '''
-EDIT MODE (HOW TO USE NANO)-
Nano is a text editor that runs on linux. It can also run on the Windows Linux Subsystem. Keybird uses nano to edit
the (unencrypted) contents of a file. The File Edit Mode opens the nano text editor after writing unencrypted file
contents to the file "_temp.txt". You can type "_help" into Edit Mode in the File Menu to load this section of the
documentation into nano. Edits to this document will not be saved, so you can experiment freely.

A short guide to shortcuts:
^G  means "press ctrl and G at the same time to use this shortcut" you can also press esc twice and then G
M-G means "press alt and G at the same time to use this shortcut"

Note that G can be substituted for any letter to get another shortcut. You should see a list of them at the bottom of
this window. ^X exits the nano editor and returns to Keybird. For more information use ^G.

Important Operations:
^G -- Help
^X -- Exit; go back to Keybird
Up and Down arrows -- Scroll
M-U -- Undo
M-E -- Redo

Upon finishing your edit and exiting, you will be asked if you want to save your edit. Type "yes" or "y" to save your
edit to the file you have selected. The file will be overwritten by the edit and encrypted. Type "no" or "n" to cancel
the edit. 
	'''
	s= '''
-INSTALL-
To download from Github select the zip file "Keybird", click on it, then click "view raw" or the download button.

This is the Linux Edition. If you would like to install Ubuntu, you can do so here:
https://ubuntu.com/tutorials/install-ubuntu-desktop#1-overview

(If you know more than I do and are rolling your eyes at these instructions, email me nicely about your way!)
If you click on this file, after extraction. It will create a Keybird directory, install pip and pwinput and
write the main source file in Keybird/src. You can stop there if that works for you.

For installation on a virtual environment, (ie Ubuntu) copy the content of the installation file, open Ubuntu
cd into the directory of your choice and do the following:
cat > install.sh
(Right click to paste)
control, shift, D (or command, shift, D) push all 3 keys at once.
bash ./install.sh

That's it. The ls command should show you a Keybird directory.

-WELCOME TO KEYBIRD-
The purpose of Keybird is to improve the accessibility of password managers without compromising security.
You need lots of passwords, but making them is tedious. Repeating passwords reduces their effectiveness. In-browser
managers are fine until they lock you out.

You may ask yourself:
"What was my password again?"
"Why does Safari fill in the wrong info?"
"Did I make this account on Google?"

Skip that nonsense, use Keybird.

Keybird is designed to generate and store passwords on your computer. While other managers integrate with your browser,
they are much better for accumulating passwords than actually managing them. At worst you can become dependant on a
specific browser to access your stuff. At best you might still use a small number of passwords you wrote yourself for
the important stuff, which puts the important stuff at risk.

My thinking is that 100 auto-generated passwords is bad, a small number of manually created passwords is worse, and
both of these together is what often happens. Instead of coming up with a few complicated passwords and using them
everywhere, depending on a browser extension, or (most likely) both. You can use Keybird to generate secure
passwords from simple keys, that are easy to create and remember.

-FEATURES-
Accessibility:
To prevent flashing lights, loading screens cannot update within the span of one third of a second.
Also updates to a process, such as modifying files, also cannot update within the span of one third of a second.
The a, s, d, f, g, h, j, k, and l keys map to 0 through 8. So you can use Keybird in the dark without issue.
(Note that an update is text printed to the screen.)

Keys:
This app uses keys to make passwords. The keys are easy to remember. The passwords are secure.
Keys are 16 characters max.
Passwords are 16 characters.

Two Key Mode:
Keybird has a Two Key Mode. One private key and many public keys. The public keys can be website names. You can have
many passwords and you only need to remember one key.

Username Generator:
The Username Generator helps you think of usernames. It asks you three questions, and generates names from your
answers.

Files:
Files store passwords and keys. They are encrypted to prevent accidents. Files are cleaned at start up. They are
alphabetized by key and duplicate info is deleted. Files can also be edited in the nano text editor.

Settings:
Toggle file saving
Toggle masking, which covers private stuff.
Toggle debug mode, which prints errors.

Notepad:
A notepad file is editable from the File Menu. Store usernames, passwords, and other things here and they will be
encrypted in the same manner as other files (protection from accidents, not attacks).

Web Repl:
Use the repl when you leave this app at home. If you need a password quickly, use your key. Nothing is saved on the
repl.\n'''+ nano +'''
-GITHUB-
https://github.com/PixelatedStarfish/Keybird-Password-Manager

-WEB REPL-
https://pixelatedstarfish.github.io/Keybird-Password-Manager/

-INDICATORS-
Note that a filename that begins with an underscore is reserved.
Two underscores means the file is hidden.
> Indicates input
>> Masked input

-TESTS-
Tests are written into the source.
At the main menu select the following:
-1 for general testing purposes
-2 to generate sample files

	''' + legal + '''
-SOURCES-
Clear Screen
https://www.csestack.org/clear-python-interpreter-console/
Copy to Clipboard
https://stackoverflow.com/questions/11063458/python-script-to-copy-text-to-clipboard
Documentation Conventions
https://peps.python.org/pep-0257/
Encryption
https://www.geeksforgeeks.org/encoding-and-decoding-base64-strings-in-python/
Flashing Lights Guidelines
https://www.accessguide.io/guide/flashing-lights
Get Current Working Directory
https://note.nkmk.me/en/python-os-getcwd-chdir/
License
https://choosealicense.com/
Nano
https://www.nano-editor.org/dist/latest/nano.html
Password Masking
https://stackoverflow.com/questions/9202224/getting-a-hidden-password-input

-ERRORS AND DEBUG-
Errors happen, and a well designed program can handle them fairly well There are two kinds of errors that Keybird is
designed to handle:

A Permission Error - these occur when Keybird attempts to modify a file that is open or in use.
A General Error    - these occur when Keybird functions incorrectly.

Errors are reported in Python3 as tracebacks through the call stack. The line number and function in source are shown
as well as the type of error that occurred. Sometimes errors occur while an error is being handled, in this case a
message will indicate as such, and more information will be printed.

In typical use the traceback will not be printed. You will be given a prompt that indicates an error has occurred and
you can close the app by pressing enter (return). Type "debug", "traceback", or "report" into the error prompt
to get the debug info. That said, I want to keep the error message as simple as I can, to prevent needless confusion. 
No one wants to see a wall of text when they are trying to understand what just happened! 

You are certainly welcome to reach out to me regarding an error in Keybird. I would appreciate your time.
You can reach out by email, Github, or Itch.

To email me, please use the subject line "Keybird Error Report" tell me about what happened and what you were
doing when the error occurred. You can include the traceback if you have one. I will try to reproduce the error
in a test and attempt to debug it. I will reply to you and update the Github and Itch pages. Programs and apps
need maintenance over time. Python, batch, and your operating system will be updated and changed over time.

Please be kind to me in your emails and other communications. I am a person, and I want to be treated like one.
I do not take responsibility for damages or inconveniences that result from the use of Keybird. That is what
the legal section is for, after all. I hope you find Keybird useful, simple, and enjoyable. Good luck!

-NOTES-
Keybird is written in Python3 and Batch for Windows.
Keybird is open source.\nVersion ''' + VERSION + '''
Developed by Andrew Vella
Copyright (c) 2022
@PixelatedStarfish on Github and Itch
andyjvella@gmail.com
Thank you for using Keybird!
	'''

	if (b == "all"):
		return s
	if(b == "legal"):
		return legal
	if(b == "nano"):
		return nano
	return None


#SHELL
##Copy string to clipboard so it can be pasted on Windows.##
def copyToclipX(txt):
	print("\nCopied to Clipboard.") #technically a lie but the message needs to print before the function ends.
	cmd='echo '+txt.strip()+'|clip'
	return subprocess.check_call(cmd, shell=True)

##Copy string to clipboard so it can be pasted on Mac.##
def copyToclipMac(txt):
	print("\nCopied to Clipboard.") #technically a lie but the message needs to print before the function ends.
	cmd='echo '+txt.strip()+'|pbcopy'
	return subprocess.check_call(cmd, shell=True)

##Open nano on Windows##
def openNanoPC(s):
	#I'm going to do my own saving prompt 
	f = open("_temp.txt", "w")
	f.write(s)
	f.close()
	clear()
	print("*Loading Nano*")
	print(docs("nano"))
	print("*Loading Nano*")
	stressRelief()
	subprocess.run(["wsl", "nano","_temp.txt", "-t"])
	f = open("_temp.txt", "r")
	n = f.read()
	f.close()
	os.remove("_temp.txt")
	stressRelief()
	clear()
	a = YesOrNo("Would you like to save your edit? (y/n)?\n>  ")
	if (a):
		s = n
		print("Saved.")
	if (not a):
		print("Your edit is cancelled.")

	return s

##Open nano on Mac##
def openNano(s):
	#I'm going to do my own saving prompt 
	f = open("_temp.txt", "w")
	f.write(s)
	f.close()
	clear()
	print("*Loading Nano*")
	print(docs("nano"))
	print("*Loading Nano*")
	stressRelief()
	subprocess.run(["nano","_temp.txt", "-t"])
	f = open("_temp.txt", "r")
	n = f.read()
	f.close()
	os.remove("_temp.txt")
	stressRelief()
	clear()
	a = YesOrNo("Would you like to save your edit? (y/n)?\n>  ")
	if (a):
		s = n
		print("Saved.")
	if (not a):
		print("Cancelled.")

	return s
##Clear shell on Windows##
def clearPC():
	os.system('cls')
	

##Clear shell on Mac##
def clear():
	os.system('clear')
	
#ACCESSIBILITY
def dinput(s):
	##In the dark, you can use the home row instead of groping for numbers and hitting function keys.##
	a = input(s)

	if (a.lower() == "a"):
		a = "0"
	if (a.lower() == "s"):
		a = "1"
	if (a.lower() == "d"):
		a = "2"
	if (a.lower() == "f"):
		a = "3"
	if (a.lower() == "g"):
		a = "4"
	if (a.lower() == "h"):
		a = "5"
	if (a.lower() == "j"):
		a = "6"
	if (a.lower() == "k"):
		a = "7"
	if (a.lower() == "l"):
		a = "8"
	return a

##Prevents flashing lights by ensures updates cannot ahppen within the span of a third of a second.##
def stressRelief():
	#extends process times by a random fraction of a second when used.
	#The purpose is to keep text from flashing and disappering quickly.
	
	#gap = random.randint(3, 4) for variation if needed
	
	time.sleep(.3 / 10) # gap / 10 (if needed for variation)
	


#TESTING
##These are all self explanatory.##
def test():
	#a = [("fox", "content"), ("dog", "content"), ("Zap", "content"), ("zap", "content"), ("app", "content"), ("#$%^", "content"), ("app", "content"), ("pen", "content"), ("war", "content")]
	#message = getRandMessage()

	print("All tests are completed.")

def maskedInputTest():
	d = pwinput.pwinput()
	print(d)

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
		i = i #pylint is not the best...
		stressRelief()
		if (random.randint(1, 3) == 2): 
			kTwo = randomKey() #for testing alphabetical sort and duplicate key deletion in the file cleaner
		r = (genResult(kOne, kTwo))
		saveTkToFile(kOne, kTwo, r)

def randomKey():
	SAMPLE_KEYS = '''
	Ray Charles Bille Holiday Evelyn Frank Apple Bananna Xavier Huzzah Test Java Mocha Cobra Pear
	Alto Soprano Tenor Tom Seven Robert Micheals Marty Dan Miller Beller Quote Cabbage Dessert Futon Big
	Pixelated Starfish Vella Cash Jones App Keybasket Key Lock Thread Race Condition Skidmore Echo Jolly
	Quarter Dime Dollar Euro Swan Lion Donkey Dank Dusk Dawn Sun Moon Phone Light Dark Kiss Touch Hug Pie
	Caress Shirt Pants Belt Socks Shoes Wolf Lana Del John Lennon Ampersand Third Amendment Linnel Pi Tau
	Flansy Question Mark Cola Simon Scallop Zap Pow Bang Woosh Brush Your Teeth Eat Food Live Laugh Tau En
	Love Ball Small Call Tall Tufted Titmouse Cardinal Chickadee Blue Jay Yellow Green Purple Tea For Sigma
	Two Three Art Tatum Channel Soda Milk Orange Juice Ice King Queen Duke Jack Rook Pawn Bishop Castle Oct
	Dec Non Hex Sep Bi Mono Queer Peace On Earth Mercy Xmas Angels Chickens Hello World Good Goodbye Bye Buy
	Gifts Dog Cat Mouse Mercury Venus Earth Mars Jupiter Saturn Uranus Neptune Pluto Asteroid Star Space Corn
	Supreme Deluxe Alpha Bravo Charlie Delta Epsilon Foxtrot Golf Hotel Indigo Juliet Kilo Lima Bean Passant
	Roof Tooth Hand Foot Mourning Dove Chick Raptor Claw Talon Qwerty Typewriter Type Writer Pan Pot Handle
	Brush Blush Breath Birth Ear Dear Clear Cheer Razor Candy Goth Morse Horse Bikes Likes Calmed Palmed Up
	'''.replace("\n", "").split(" ")

	return SAMPLE_KEYS[random.randint(0, len(SAMPLE_KEYS) -1 )].replace("\t", "")

#MAIN 
##This function loads settings the file "__Settings.txt" including file saving, debug mode, and password masking.##
def getSettings():
	global SAVE
	global MASK
	f = open("Files/__Settings.txt", "r")
	s = f.read()
	f.close()
	if (s[0] == "0"):
		SAVE = False
	if (s[0] == "1"):
		SAVE = True
	if (s[1] == "0"):
		MASK = False
	if (s[1] == "1"):
		MASK = True

##Configure and run the Keybird App and handle errors.##
def main():
	try: 
		print("Loading Working Directory.")
		#set cwd to source file
		os.chdir(os.path.dirname(os.path.abspath(__file__)))
		stressRelief()
		print("Loading Files.")

		#make Files dir if it does not exist
		try:
			os.mkdir("Files")
		except Exception:
			pass
		try:
			open("Files/_oneKey.txt", "x") 
		except Exception:
			pass
		try:
			open("Files/__Notepad.txt", "x") 
		except Exception:
			pass
		try:
			f = open("Files/__Settings.txt", "r") 
			f.close()
		except FileNotFoundError:
			f = open("Files/__Settings.txt", "x") 
			f.write(defaultConstant())
			
			f.close()
			pass
		try:
			global KEY_LENGTH
			global PASSWORD_LENGTH
			encrypt_to_file("Files/_help.txt", docs("nano")) #get the Nano section of the docs only
		except Exception:
			pass
		stressRelief()
		print("Loading Settings.")
		getSettings()
		stressRelief()
		fileCleaner() #File cleaner text printed in this function
		cleanNanoDroppings() #closing the app while nano is running leaves a .save file in src, this .save needs to be deleted
		stressRelief()
		print("Ready.\n----")
		stressRelief()
		#run the menu
		menu()
	except PermissionError:
		print("Access denied. Files may need to be closed in another application first.")
		input("Error; press Return (Enter) to close.\n> ")
	
	except Exception:
		d = input("Error; press Return (Enter) to close.\n> ")
		if (d.lower().lstrip() == "debug" or d.lower().lstrip() == "traceback" or d.lower().lstrip() == "report"):
			traceback.print_exc()
			input("Press Return (Enter) to close.\n> ")
	

##Program Starts Here## 
print("Initializing.") 

#globals
SAVE = True
MASK = True
KEY_LENGTH = 16
PASSWORD_LENGTH = 16
ENCODING = "utf_8" #for encryption
VERSION = "2.4.2" #Keybasket 2.0
main()



#!/usr/bin/env python3
import random
import traceback
import os
import base64
import subprocess
import time
import pwinput

#2.4.2 has an installer!

##The Main Menu, with a welcome message##
def menu():
	global VERSION
	clear()
	while (True):
		print("Thank you for using the Keybird Password Manager (Linux Edition).\nVersion " +VERSION+ "\nCopyright 2022.\n\nThis is created by Andrew Vella.\nEmail:  andyjvella@gmail.com.\nGithub: @PixelatedStarfish\n\nPlease see the Disclaimer and License, before using this app.")
		a = dinput("\nType a number and press enter (return) to select an option:\n0  Help\n1  One Key Mode\n2  Two Key Mode\n3  Username Generator\n4  File Menu\n5  Settings Menu\n6  Disclaimer and License\n7  Erase Data\n8  Close\n> ")
		if (a == "-1"):
			test()
		if (a == "-2"):
			h = input("Generate sample files? You might lose data. (Type 'y' for yes.)\n")
			if (h[0].lower().lstrip() == 'y'):
				for i in range(10):
					randomSampleFile(randomKey())
		if (a == "0"):
			print(docs())
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
			clear()
			print(docs("legal"))
			
		if (a == "7"):
			clear()
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
					stressRelief()
				print("Done.")
				input("Press Return (Enter) to close.\n> ")
				exit()

				
		if (a == "8"):
			exit()
		input("Press Return (Enter) to return to the Main Menu.\n>")
		clear()


##This function runs the Two Key Mode## 
def twoKey():
	global KEY_LENGTH
	kOne = ""
	kTwo = ""

	clear()
	print("\nGive a Username Key. Be sure it is not easily guessed:\n")
	if (MASK):
		kOne = pwinput.pwinput(">>  ")[0:KEY_LENGTH]
	if (not MASK):
		kOne = input(">  ")[0:KEY_LENGTH]

	kTwo = input("\nGive a Site Key, such as a website name:\n> ")[0:KEY_LENGTH]
	if (len(kOne) == 0 or len(kTwo) == 0):
		print("One of the keys is empty: no result.")
		return
	if (kOne[0] == '_' or kTwo[0] == '_'):
		print("Keys cannot begin with underscores: no result.")
		return
	r = (genResult(kOne, kTwo))

	if (MASK):
		print("\nResult:\n" + ("*" * PASSWORD_LENGTH) + "\n")
	if (not MASK):
		print("\nResult:\n" + r + "\n")
	copyToclipMac(r)
	if (SAVE):
		saveTkToFile(kOne, kTwo, r)


##This function runs the One Key Mode## 
def oneKey():
	global MASK
	kOne = ""
	clear()
	print("\nGive a Key, such as a word you will remember. Be sure it is not easily guessed:\n")
	if (MASK):
		kOne = pwinput.pwinput(">>  ")[0:KEY_LENGTH]
	if (not MASK):
		kOne = input(">  ")[0:KEY_LENGTH]
	kTwo = "Default_Key_2"
	if (len(kOne) == 0):
		print("Key is empty: no result.")
		return
	if (kOne[0] == '_'):
		print("Keys cannot begin with underscores: no result.")
		return

	r = (genResult(kOne, kTwo))
	if (MASK):
		print("\nResult:\n" + ("*" * PASSWORD_LENGTH) + "\n")
	if (not MASK):
		print("\nResult:\n" + r + "\n")

	copyToclipMac(r)
	if (SAVE):
		saveOkToFile(kOne, r)


##This runs the hash function for One Key Mode and Two Key Mode. It maps passwords to keys.##
def genResult(key1, key2):
	global PASSWORD_LENGTH

	#set of all characters that can be in a password
	nums = list("1234567890")
	uppers = list("QWERTYUIOPASDFGHJKLZXCVBNM")
	lowers = list("qwertyuiopasdfghjklzxcvbnm")
	symbols = list("-_")
	
	#get new char sequence (result)
	s = ""
	while(len(s) < PASSWORD_LENGTH):
		s += key1[len(key1)//2:len(key1)] + key2[0:len(key2)//2] + key1[0:len(key1)//2] + key2[len(key2)//2:len(key2)] #weave keys together for increased variation
		while (len(s) < 64): #arbitrary buffer 
			s += s

	flipper = -1
	stuff = [nums, uppers, lowers, symbols]
	out = ""

	offsetKroll = 0  #as in Nick Kroll
	for c in s:
		flipper = flipper - (ord(c) % 3) #cycle through the four categories of characters
		flipper = flipper % 4
		out += stuff[flipper][(offsetKroll + ord(c)) % len(stuff[flipper])] #take letter from s, convert to number N, set N + O to itself mod list length, and get char N in list added to out, add N to O
		offsetKroll += ord(c)

	#offset is needed because the first three chars of a password are always identical if the same private key is used
	#So skip at least three characters ahead (and up to PASSWORD_LENGTH) according to the int value of the last char in the password	

	offsetMulaney = (ord(s[len(s) -1]) % PASSWORD_LENGTH) + 3 #as in John Mulaney; the first three chars are always the same, so the actual result is adjusted by an offset based on the least predictable letter (In file passwords... the first three characters are always the same). The offset lops off an (effectively) psuedo-random number of letters and gets the next 16 characters for a password. 


	#adjust to length
	return out[offsetMulaney:(PASSWORD_LENGTH + offsetMulaney)]

##Saves the data generated by Two Key Mode to an appropriate file.##
def saveTkToFile(kOne, kTwo, r):
	global MASK
	#this used to ask to save. Now it is a setting.
	h = 'y'
	if (h[0].lower().lstrip() == 'y'):
		content =  "\nSite Key:\t" + kTwo + "\nPassword:\t" + r + "\n"

		#make the file, if it exists, move on
		try:
			f = open("Files/" + kOne + ".txt", "x")
			if (not MASK):
				print("Created '" + kOne + ".txt'") 
			if (MASK):
				print("Created new file")
			f.close()
			encrypt_to_file("User key:\t" + "\n")
		except Exception:
			pass
		s = decrypt_file("Files/" + kOne + ".txt")
		s += content
		encrypt_to_file("Files/" + kOne + ".txt", s)

		if (not MASK):
			print("Added to '" + kOne + ".txt'")
		if (MASK):
			print("Added to file")
	

##Saves the data generated by One Key Mode to  "_oneKey.txt". ##
def saveOkToFile(kOne, r):
	
	h = 'y'
	if (h[0].lower().lstrip() == 'y'):
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
	

##The Username Genrator takes three phrases and splices three words together randomly.##
def genUserName():
	clear()
	print("Username Generator")
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

	#Display outlist and prompt for number to select.
	#If the selection is not in the list, run again, copy selection to clipboard and return

	i = 0 #again, a different i
	print("\nUsernames:")
	while (i < len(outList)):
		outList[i] = outList[i].replace("'", "")
		outList[i] = outList[i].replace('"', "")
		print(outList[i])
		i = i + 1
	print()
	

##For use in all yes or no questions##
def YesOrNo(s):
	a = str(input(s) + "")
	try:
		return a.lstrip().lower()[0] == "y"
	except Exception: #no input given means no
		return False
	
#SUBMENUS

##The Settings Menu. Toggle each setting on or off here.##
def SettingsMenu(a):
	while (not a == "4"):
		global SAVE
		global MASK
		if (a == "SettingsMenu"):
			clear()
			print("Settings Menu\n\n0  Help")
			print ("1  File Saving      (" + menuBooleanFormatter(SAVE) + ")")
			print ("2  Masking          (" + menuBooleanFormatter(MASK) + ")")
			print ("3  Retore Defaults\n4  Back to Main Menu\n5  Close")
			b = dinput("> ")
			if (not a == "4"):
				SettingsMenu(b)
			menu()

		if (a == "0"):
			print ("1  Toggle the option to save to a file.")
			print ("2  Toggle the option to mask passwords.")
			print ("3  Retore settings to default.\n4  Return to the Main Menu.\n5  End session.")

		if (a == "1"):
			SAVE = (not SAVE)
			print("Set to " + menuBooleanFormatter(SAVE))
		if (a == "2"):
			MASK = (not MASK)
			print("Set to " + menuBooleanFormatter(MASK))
		if (a == "1" or a == "2"):
			o = ""
			if (not SAVE and not MASK):
				o = "00"
			if (not SAVE and MASK):
				o = "01"
			if (SAVE and not MASK):
				o = "10"
			if (SAVE and MASK):
				o = "11"
		
			f = open("Files/__Settings.txt", "w") 
			f.write(o) 
			f.close()
			print("\nSaved.\n")

		if (a == "3"):
			SAVE = True
			MASK = True
			f = open("Files/__Settings.txt", "w") 
			f.write(defaultConstant())
			f.close()
			print("\nRestored.\n")
			
		if (a == "5"):
			exit()
	
		input("Press Return (Enter) to return to the Settings Menu.\n> ")
		a = "SettingsMenu"
	  

##The Files Menu. Read, edit, delete, and organize files.##
def FileMenu(a):
	while (not a == "7"):
		global SAVE
		global MASK
		if (a == "FileMenu"):
			clear()
			if (MASK):
				print ("\n*Please note that all text in this menu is not masked or hidden. All file content will be plainly visible.*")

			print("Files Menu\n\n0  Help\n1  List Files\n2  Read File\n3  Edit File\n4  Delete File\n5  Clean Files\n6  Use Notepad\n7  Back to Main Menu\n8  Close.")
			b = dinput("> ")
			if (not a == "7"):
				FileMenu(b)
			menu()
		if (a == "0"):
			print ("1  List all files by name.")
			print ("2  Read the contents of a file.")
			print ("3  Edit a file. For help, type '_help' at the prompt.")
			print ("4  Permenantly erase a file. (Be sure it is not in use.)")
			print ("5  Run the File Cleaner and organize keys.")
			print ("6  Open the notepad for use. The notepad is encrypted.")
			print ("7  Return to the Main Menu.")
			print ("8  End Session.")

		if (a == "1"):
			printFileList()
		if (a == "8"):
			exit()
		if (a == "2"):
			print(decrypt_file("Files/" +fileSelector()))
		if (a == "3"):
			openTextEditorMode("Files/" +fileSelector())
		if (a == "4"):
			os.remove("Files/" +fileSelector())
			print("Deleted.\n")
		if (a == "5"):
			fileCleaner()
			print("Done")
		if (a == "6"):
			print("Opening the notepad")
			openTextEditorMode("Files/__Notepad.txt")
		input("Press Return (Enter) to return to the Files Menu.\n> ")
		a = "FileMenu"
	 

##Open Edit Mode##
def openTextEditorMode(path):
	#if help is needed
	s = openNano(decrypt_file(path))
	if (not path == "Files/_help.txt"):
		encrypt_to_file(path, s)
		return
	encrypt_to_file(path, docs("nano")) #overwrite any edits to the nano help docs

##Ask the user for a file, and get it. If the file is not found, print the list of files.##
def fileSelector():
	#get input and check for a match in the Files dir, if no match is found, recur
	l = os.listdir("Files")

	#get input
	s = input("Please select a file by typing it's name. You do not need to include the extension.\nType nothing to return to the File Menu.\n>  ") + ".txt"
	s = s.replace(".txt.txt", ".txt")

	if (s == ".txt"): #no option given
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

##Generate and print a list of key files. Calls getFileList()##
def printFileList():
	l = getFileList()
	print("File List:")
	for i in l:
		print(i)
	

##Generates the list of key files.##
def getFileList():
	l = os.listdir("Files")
	#REMOVE HIDDEN FILES
	for i in l:
		if (i[0] == '_' and i[1] == '_'):
			l.remove(i)
	return l


#FILE CLEANER AND ORGANIZATION

##This cleans the files, sortng keys alphabetically and removing douplicated infomation.
#This is accomplished by creating (key, section) tuples, sorting the tuples by key, removing duplicates, and writing 
#each section to the file. This overwrites the previous version. FIles are decrypted at the start, and then encrypted.##
def fileCleaner():
	print("Running the File Cleaner")
	l = getFileList()

	for i in l:
		if (i[0] == "_"):
			l.remove(i)
	l.append("_oneKey.txt")
	
	for i in l:
		print("Cleaning " + i)
		stressRelief()
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
		encryptable = "" #file content before encrpytion as a string
		for i in range(0, len(tuples) - 1):
			encryptable += tuples[i][1] + "\n\n"
		encryptable += tuples[len(tuples) - 1][1]
		encryptable = encryptable.replace("\n\n\n", "\n\n") #triple newlines appear for some reason, have a bandaid!
		encrypt_to_file(path, encryptable)
		
	 
##extracts a key from a line of text that has a key in it.##
def extractKeyFromLine(s):
	if(len((s).split("\t")) < 2):
		return 
	return s.split("\t")[1]

##If you close the shell window while running nano, a .save file will be left over in src. This deletes them.##
def cleanNanoDroppings():
	l = os.listdir()
	for i in l:
		t = i.split(".") 
		if (t[len(t)-1] == "save"):
			os.remove(i)
	

##Function to do selection sort on tuples in an array, by element 0 of each tuple (yes, On^2)##
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

##Removes duplicate tuples in a sorted list##
def removeDuplicates(a):
	out = []
	temp = a[0][0]

	out.append(a[0])

	for i in a:
		if (not i[0] == temp):
			out.append(i)
			temp = i[0]
	return out

#FORMATTING
##This function is used by the settings menu to indicate that status of a setting##
def menuBooleanFormatter(b):
	if (b):
		return "ON"
	return "OFF"

##This constant stores default settings as bits (pedantically, characters) SAVE, DEBUG, MASK.##
def defaultConstant(): 
	return "11"

#ENCRYPTION AND DECRYPTION

##Encrypts a string to a reversed base64 string and wrties to a file. This is not secure from attacks, it prevents accidents.##
def encrypt_to_file(path, message):
	global ENCODING
	message = reverse(message)
	string_bytes = message.encode(ENCODING)
	base64_bytes = base64.b64encode(string_bytes)
	base64_string = base64_bytes.decode(ENCODING)

	f = open(path, "w")
	f.write(base64_string)
	f.close()
	
##Decrypts a file from a reversed base64 string. This returns a string.##
def decrypt_file(path):
	global ENCODING
	f = open(path, "r")
	base64_string = f.read()
	base64_bytes = base64_string.encode(ENCODING)
	string_bytes = base64.b64decode(base64_bytes)
	m = string_bytes.decode(ENCODING)
	return reverse(m)

##Function to reverse a string.##
def reverse(s):
	out = ""
	i = len(s)

	while (i > 0):
		i = i - 1
		out += s[i]
	return out

#DOCS
##Prints sections of the ducmentation where they are needed. Pass "legal" for the legal. Pass "nano" for nano 
#instructions. Pass nothing for the entire documentation.##
def docs(b = "all"):
	legal = '''
-LEGAL-
Disclaimer:
No information produced in whole or part by this app is guaranteed to be perfectly safe. Your files
can be read, modified, or deleted. The app source code can also be read, modified, or deleted, which would cause
unpredictable effects while running the app. Back up important things; store your passwords in a few safe places.
Keep untrustworthy people off your computer. Do not store your passwords publicly, or generate them with keys
that are easy to guess. Stay safe!

No birds were harmed in the making of Keybird, including the program, online material, documentation, and photography. 
Wild robins were photographed eating berries from a park tree.

License:
MIT License

Copyright (c) 2022 Andrew Vella

Permission is hereby granted, free of charge, to any person obtaining  a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
			''' 
	nano = '''
-EDIT MODE (HOW TO USE NANO)-
Nano is a text editor that runs on linux. It can also run on the Windows Linux Subsystem. Keybird uses nano to edit
the (unencrypted) contents of a file. The File Edit Mode opens the nano text editor after writing unencrypted file
contents to the file "_temp.txt". You can type "_help" into Edit Mode in the File Menu to load this section of the
documentation into nano. Edits to this document will not be saved, so you can experiment freely.

A short guide to shortcuts:
^G  means "press ctrl and G at the same time to use this shortcut" you can also press esc twice and then G
M-G means "press alt and G at the same time to use this shortcut"

Note that G can be substituted for any letter to get another shortcut. You should see a list of them at the bottom of
this window. ^X exits the nano editor and returns to Keybird. For more information use ^G.

Important Operations:
^G -- Help
^X -- Exit; go back to Keybird
Up and Down arrows -- Scroll
M-U -- Undo
M-E -- Redo

Upon finishing your edit and exiting, you will be asked if you want to save your edit. Type "yes" or "y" to save your
edit to the file you have selected. The file will be overwritten by the edit and encrypted. Type "no" or "n" to cancel
the edit. 
	'''
	s= '''
-INSTALL-
To download from Github select the zip file "Keybird", click on it, then click "view raw" or the download button.

This is the Linux Edition. If you would like to install Ubuntu, you can do so here:
https://ubuntu.com/tutorials/install-ubuntu-desktop#1-overview

(If you know more than I do and are rolling your eyes at these instructions, email me nicely about your way!)
If you click on this file, after extraction. It will create a Keybird directory, install pip and pwinput and
write the main source file in Keybird/src. You can stop there if that works for you.

For installation on a virtual environment, (ie Ubuntu) copy the content of the installation file, open Ubuntu
cd into the directory of your choice and do the following:
cat > install.sh
(Right click to paste)
control, shift, D (or command, shift, D) push all 3 keys at once.
bash ./install.sh

That's it. The ls command should show you a Keybird directory.

-WELCOME TO KEYBIRD-
The purpose of Keybird is to improve the accessibility of password managers without compromising security.
You need lots of passwords, but making them is tedious. Repeating passwords reduces their effectiveness. In-browser
managers are fine until they lock you out.

You may ask yourself:
"What was my password again?"
"Why does Safari fill in the wrong info?"
"Did I make this account on Google?"

Skip that nonsense, use Keybird.

Keybird is designed to generate and store passwords on your computer. While other managers integrate with your browser,
they are much better for accumulating passwords than actually managing them. At worst you can become dependant on a
specific browser to access your stuff. At best you might still use a small number of passwords you wrote yourself for
the important stuff, which puts the important stuff at risk.

My thinking is that 100 auto-generated passwords is bad, a small number of manually created passwords is worse, and
both of these together is what often happens. Instead of coming up with a few complicated passwords and using them
everywhere, depending on a browser extension, or (most likely) both. You can use Keybird to generate secure
passwords from simple keys, that are easy to create and remember.

-FEATURES-
Accessibility:
To prevent flashing lights, loading screens cannot update within the span of one third of a second.
Also updates to a process, such as modifying files, also cannot update within the span of one third of a second.
The a, s, d, f, g, h, j, k, and l keys map to 0 through 8. So you can use Keybird in the dark without issue.
(Note that an update is text printed to the screen.)

Keys:
This app uses keys to make passwords. The keys are easy to remember. The passwords are secure.
Keys are 16 characters max.
Passwords are 16 characters.

Two Key Mode:
Keybird has a Two Key Mode. One private key and many public keys. The public keys can be website names. You can have
many passwords and you only need to remember one key.

Username Generator:
The Username Generator helps you think of usernames. It asks you three questions, and generates names from your
answers.

Files:
Files store passwords and keys. They are encrypted to prevent accidents. Files are cleaned at start up. They are
alphabetized by key and duplicate info is deleted. Files can also be edited in the nano text editor.

Settings:
Toggle file saving
Toggle masking, which covers private stuff.
Toggle debug mode, which prints errors.

Notepad:
A notepad file is editable from the File Menu. Store usernames, passwords, and other things here and they will be
encrypted in the same manner as other files (protection from accidents, not attacks).

Web Repl:
Use the repl when you leave this app at home. If you need a password quickly, use your key. Nothing is saved on the
repl.\n'''+ nano +'''
-GITHUB-
https://github.com/PixelatedStarfish/Keybird-Password-Manager

-WEB REPL-
https://pixelatedstarfish.github.io/Keybird-Password-Manager/

-INDICATORS-
Note that a filename that begins with an underscore is reserved.
Two underscores means the file is hidden.
> Indicates input
>> Masked input

-TESTS-
Tests are written into the source.
At the main menu select the following:
-1 for general testing purposes
-2 to generate sample files

	''' + legal + '''
-SOURCES-
Clear Screen
https://www.csestack.org/clear-python-interpreter-console/
Copy to Clipboard
https://stackoverflow.com/questions/11063458/python-script-to-copy-text-to-clipboard
Documentation Conventions
https://peps.python.org/pep-0257/
Encryption
https://www.geeksforgeeks.org/encoding-and-decoding-base64-strings-in-python/
Flashing Lights Guidelines
https://www.accessguide.io/guide/flashing-lights
Get Current Working Directory
https://note.nkmk.me/en/python-os-getcwd-chdir/
License
https://choosealicense.com/
Nano
https://www.nano-editor.org/dist/latest/nano.html
Password Masking
https://stackoverflow.com/questions/9202224/getting-a-hidden-password-input

-ERRORS AND DEBUG-
Errors happen, and a well designed program can handle them fairly well There are two kinds of errors that Keybird is
designed to handle:

A Permission Error - these occur when Keybird attempts to modify a file that is open or in use.
A General Error    - these occur when Keybird functions incorrectly.

Errors are reported in Python3 as tracebacks through the call stack. The line number and function in source are shown
as well as the type of error that occurred. Sometimes errors occur while an error is being handled, in this case a
message will indicate as such, and more information will be printed.

In typical use the traceback will not be printed. You will be given a prompt that indicates an error has occurred and
you can close the app by pressing enter (return). Type "debug", "traceback", or "report" into the error prompt
to get the debug info. That said, I want to keep the error message as simple as I can, to prevent needless confusion. 
No one wants to see a wall of text when they are trying to understand what just happened! 

You are certainly welcome to reach out to me regarding an error in Keybird. I would appreciate your time.
You can reach out by email, Github, or Itch.

To email me, please use the subject line "Keybird Error Report" tell me about what happened and what you were
doing when the error occurred. You can include the traceback if you have one. I will try to reproduce the error
in a test and attempt to debug it. I will reply to you and update the Github and Itch pages. Programs and apps
need maintenance over time. Python, batch, and your operating system will be updated and changed over time.

Please be kind to me in your emails and other communications. I am a person, and I want to be treated like one.
I do not take responsibility for damages or inconveniences that result from the use of Keybird. That is what
the legal section is for, after all. I hope you find Keybird useful, simple, and enjoyable. Good luck!

-NOTES-
Keybird is written in Python3 and Batch for Windows.
Keybird is open source.\nVersion ''' + VERSION + '''
Developed by Andrew Vella
Copyright (c) 2022
@PixelatedStarfish on Github and Itch
andyjvella@gmail.com
Thank you for using Keybird!
	'''

	if (b == "all"):
		return s
	if(b == "legal"):
		return legal
	if(b == "nano"):
		return nano
	return None


#SHELL
##Copy string to clipboard so it can be pasted on Windows.##
def copyToclipX(txt):
	print("\nCopied to Clipboard.") #technically a lie but the message needs to print before the function ends.
	cmd='echo '+txt.strip()+'|clip'
	return subprocess.check_call(cmd, shell=True)

##Copy string to clipboard so it can be pasted on Mac.##
def copyToclipMac(txt):
	print("\nCopied to Clipboard.") #technically a lie but the message needs to print before the function ends.
	cmd='echo '+txt.strip()+'|pbcopy'
	return subprocess.check_call(cmd, shell=True)

##Open nano on Windows##
def openNanoPC(s):
	#I'm going to do my own saving prompt 
	f = open("_temp.txt", "w")
	f.write(s)
	f.close()
	clear()
	print("*Loading Nano*")
	print(docs("nano"))
	print("*Loading Nano*")
	stressRelief()
	subprocess.run(["wsl", "nano","_temp.txt", "-t"])
	f = open("_temp.txt", "r")
	n = f.read()
	f.close()
	os.remove("_temp.txt")
	stressRelief()
	clear()
	a = YesOrNo("Would you like to save your edit? (y/n)?\n>  ")
	if (a):
		s = n
		print("Saved.")
	if (not a):
		print("Your edit is cancelled.")

	return s

##Open nano on Mac##
def openNano(s):
	#I'm going to do my own saving prompt 
	f = open("_temp.txt", "w")
	f.write(s)
	f.close()
	clear()
	print("*Loading Nano*")
	print(docs("nano"))
	print("*Loading Nano*")
	stressRelief()
	subprocess.run(["nano","_temp.txt", "-t"])
	f = open("_temp.txt", "r")
	n = f.read()
	f.close()
	os.remove("_temp.txt")
	stressRelief()
	clear()
	a = YesOrNo("Would you like to save your edit? (y/n)?\n>  ")
	if (a):
		s = n
		print("Saved.")
	if (not a):
		print("Cancelled.")

	return s
##Clear shell on Windows##
def clearPC():
	os.system('cls')
	

##Clear shell on Mac##
def clear():
	os.system('clear')
	
#ACCESSIBILITY
def dinput(s):
	##In the dark, you can use the home row instead of groping for numbers and hitting function keys.##
	a = input(s)

	if (a.lower() == "a"):
		a = "0"
	if (a.lower() == "s"):
		a = "1"
	if (a.lower() == "d"):
		a = "2"
	if (a.lower() == "f"):
		a = "3"
	if (a.lower() == "g"):
		a = "4"
	if (a.lower() == "h"):
		a = "5"
	if (a.lower() == "j"):
		a = "6"
	if (a.lower() == "k"):
		a = "7"
	if (a.lower() == "l"):
		a = "8"
	return a

##Prevents flashing lights by ensures updates cannot ahppen within the span of a third of a second.##
def stressRelief():
	#extends process times by a random fraction of a second when used.
	#The purpose is to keep text from flashing and disappering quickly.
	
	#gap = random.randint(3, 4) for variation if needed
	
	time.sleep(.3 / 10) # gap / 10 (if needed for variation)
	


#TESTING
##These are all self explanatory.##
def test():
	#a = [("fox", "content"), ("dog", "content"), ("Zap", "content"), ("zap", "content"), ("app", "content"), ("#$%^", "content"), ("app", "content"), ("pen", "content"), ("war", "content")]
	#message = getRandMessage()

	print("All tests are completed.")

def maskedInputTest():
	d = pwinput.pwinput()
	print(d)

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
		i = i #pylint is not the best...
		stressRelief()
		if (random.randint(1, 3) == 2): 
			kTwo = randomKey() #for testing alphabetical sort and duplicate key deletion in the file cleaner
		r = (genResult(kOne, kTwo))
		saveTkToFile(kOne, kTwo, r)

def randomKey():
	SAMPLE_KEYS = '''
	Ray Charles Bille Holiday Evelyn Frank Apple Bananna Xavier Huzzah Test Java Mocha Cobra Pear
	Alto Soprano Tenor Tom Seven Robert Micheals Marty Dan Miller Beller Quote Cabbage Dessert Futon Big
	Pixelated Starfish Vella Cash Jones App Keybasket Key Lock Thread Race Condition Skidmore Echo Jolly
	Quarter Dime Dollar Euro Swan Lion Donkey Dank Dusk Dawn Sun Moon Phone Light Dark Kiss Touch Hug Pie
	Caress Shirt Pants Belt Socks Shoes Wolf Lana Del John Lennon Ampersand Third Amendment Linnel Pi Tau
	Flansy Question Mark Cola Simon Scallop Zap Pow Bang Woosh Brush Your Teeth Eat Food Live Laugh Tau En
	Love Ball Small Call Tall Tufted Titmouse Cardinal Chickadee Blue Jay Yellow Green Purple Tea For Sigma
	Two Three Art Tatum Channel Soda Milk Orange Juice Ice King Queen Duke Jack Rook Pawn Bishop Castle Oct
	Dec Non Hex Sep Bi Mono Queer Peace On Earth Mercy Xmas Angels Chickens Hello World Good Goodbye Bye Buy
	Gifts Dog Cat Mouse Mercury Venus Earth Mars Jupiter Saturn Uranus Neptune Pluto Asteroid Star Space Corn
	Supreme Deluxe Alpha Bravo Charlie Delta Epsilon Foxtrot Golf Hotel Indigo Juliet Kilo Lima Bean Passant
	Roof Tooth Hand Foot Mourning Dove Chick Raptor Claw Talon Qwerty Typewriter Type Writer Pan Pot Handle
	Brush Blush Breath Birth Ear Dear Clear Cheer Razor Candy Goth Morse Horse Bikes Likes Calmed Palmed Up
	'''.replace("\n", "").split(" ")

	return SAMPLE_KEYS[random.randint(0, len(SAMPLE_KEYS) -1 )].replace("\t", "")

#MAIN 
##This function loads settings the file "__Settings.txt" including file saving, debug mode, and password masking.##
def getSettings():
	global SAVE
	global MASK
	f = open("Files/__Settings.txt", "r")
	s = f.read()
	f.close()
	if (s[0] == "0"):
		SAVE = False
	if (s[0] == "1"):
		SAVE = True
	if (s[1] == "0"):
		MASK = False
	if (s[1] == "1"):
		MASK = True

##Configure and run the Keybird App and handle errors.##
def main():
	try: 
		print("Loading Working Directory.")
		#set cwd to source file
		os.chdir(os.path.dirname(os.path.abspath(__file__)))
		stressRelief()
		print("Loading Files.")

		#make Files dir if it does not exist
		try:
			os.mkdir("Files")
		except Exception:
			pass
		try:
			open("Files/_oneKey.txt", "x") 
		except Exception:
			pass
		try:
			open("Files/__Notepad.txt", "x") 
		except Exception:
			pass
		try:
			f = open("Files/__Settings.txt", "r") 
			f.close()
		except FileNotFoundError:
			f = open("Files/__Settings.txt", "x") 
			f.write(defaultConstant())
			
			f.close()
			pass
		try:
			global KEY_LENGTH
			global PASSWORD_LENGTH
			encrypt_to_file("Files/_help.txt", docs("nano")) #get the Nano section of the docs only
		except Exception:
			pass
		stressRelief()
		print("Loading Settings.")
		getSettings()
		stressRelief()
		fileCleaner() #File cleaner text printed in this function
		cleanNanoDroppings() #closing the app while nano is running leaves a .save file in src, this .save needs to be deleted
		stressRelief()
		print("Ready.\n----")
		stressRelief()
		#run the menu
		menu()
	except PermissionError:
		print("Access denied. Files may need to be closed in another application first.")
		input("Error; press Return (Enter) to close.\n> ")
	
	except Exception:
		d = input("Error; press Return (Enter) to close.\n> ")
		if (d.lower().lstrip() == "debug" or d.lower().lstrip() == "traceback" or d.lower().lstrip() == "report"):
			traceback.print_exc()
			input("Press Return (Enter) to close.\n> ")
	

##Program Starts Here## 
print("Initializing.") 

#globals
SAVE = True
MASK = True
KEY_LENGTH = 16
PASSWORD_LENGTH = 16
ENCODING = "utf_8" #for encryption
VERSION = "2.4.2" #Keybasket 2.0
main()


