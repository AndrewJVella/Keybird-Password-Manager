import random
import time
import traceback
#MENU
##The Main Menu, with a welcome message##
def menu():
	global VERSION
	clear()
	while (True):
		print("Thank you for using the Keybird Password Manager (Web Edition).\nVersion " +VERSION+ "\nCopyright 2022.\n\nThis is created by Andrew Vella.\nEmail:  andyjvella@gmail.com.\nGithub: @PixelatedStarfish\n\nPlease see the Disclaimer and License, before using this app.\nAlso please note that password masking is not available in this version of Keybird.")
		a = dinput("\nType a number and press enter (return) to select an option:\n0  Help\n1  One Key Mode\n2  Two Key Mode\n3  Username Generator\n4  Disclaimer and License\n> ")
		if (a == "-1"):
			test()
		if (a == "0"):
			print(docs())
		if (a == "1"):
			oneKey()
		if (a == "2"):
			twoKey()
		if (a == "3"):
			genUserName()				
		if (a == "4"):
			print(docs("legal"))
		input("Press Return (Enter) to return to the Main Menu.\n>")
		clear()


##This function runs the Two Key Mode## 
def twoKey():
	global KEY_LENGTH
	kOne = ""
	kTwo = ""

	clear()
	print("\nGive a Username Key. Be sure it is not easily guessed:\n")
	kOne = input(">  ")[0:KEY_LENGTH]

	kTwo = input("\nGive a Site Key, such as a website name:\n> ")[0:KEY_LENGTH]
	if (len(kOne) == 0 or len(kTwo) == 0):
		print("One of the keys is empty: no result.")
		return
	if (kOne[0] == '_' or kTwo[0] == '_'):
		print("Keys cannot begin with underscores: no result.")
		return
	r = (genResult(kOne, kTwo))
	print("\nResult:\n" + r + "\n")



##This function runs the One Key Mode## 
def oneKey():
	global KEY_LENGTH
	kOne = ""
	clear()
	print("\nGive a Key, such as a word you will remember. Be sure it is not easily guessed:\n")
	kOne = input(">  ")[0:KEY_LENGTH]
	kTwo = "Default_Key_2"
	if (len(kOne) == 0):
		print("Key is empty: no result.")
		return
	if (kOne[0] == '_'):
		print("Keys cannot begin with underscores: no result.")
		return
	r = (genResult(kOne, kTwo))
	print("\nResult:\n" + r + "\n")
	


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
-FIRST START UP-
To download from Github select the zip file "Keybird", click on it, then click "view raw" or the download button.

Keybird is stored inside the zip directory (or folder) "Keybird Inside". Open the zip, then open Keybrid and click
start.bat. A dialogue box should pop up, click "Extract all" and save it to the Desktop. You will not have to
extract it again. Open the Keybird directory again and click start. At this point, a blue box will appear that
reads "Windows Protected Your PC", this is a rightly paranoid security measure to protect you from malware.
I gave you my email and my source code (in src). You can decide what to do next.

If you still want to try Keybird. You should click the underlined text "More Info", and then click run. A window
will open and start running a shell. You may see some text for a short time as the app loads. Then you will see
the main menu.

You may need to install the Windows Linux Subsystem. A section on how to do that is included in this document.

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
-INSTALL WSL-
#if you require the windows linux subsystem to run nano (the text editor used by Keybird)
#run this command in Command Prompt by typing it in and pressing enter (return).

wsl --install

-GITHUB-
https://github.com/PixelatedStarfish/Keybird-Password-Manager

-WEB REPL-
tinyurl.com/KeybirdWeb

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

def clear():
	#cannot clear screen on trinket
	print("\n==========\n")	

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
	
def test():
	#a = [("fox", "content"), ("dog", "content"), ("Zap", "content"), ("zap", "content"), ("app", "content"), ("#$%^", "content"), ("app", "content"), ("pen", "content"), ("war", "content")]
	#message = getRandMessage()

	print("All tests are completed.")

#START HERE#
KEY_LENGTH = 16
PASSWORD_LENGTH = 16
VERSION = "2.4" #Keybasket 2.0

try:
	menu()
except Exception:
	traceback.print_exc()