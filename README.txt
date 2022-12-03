-WELCOME TO KEYBIRD-
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
both of these together is what often happens. Instead of coming up with a few compilcated passwords and using them
everywhere, depending on a browser extension, or (most likely) both. You can use Keybird to generate secure
passwords from simple keys, that are easy to create and remember.

-FEATURES-
Keys:
This app uses keys to make passwords. The keys are easy to remeber. The passwords are secure.
Keys are 16 characters max.
Passwords are 16 characters.

Two Key Mode:
Keybird has a Two Key Mode. One private key and many public keys. The public keys can be website names. You can have
many passwords and you only need to remeber one key.

Username Generator:
The Username Generator helps you think of usernames. It asks you three questions, and generates names from your
answers.

Files:
Files store passwords and keys. They are encrypted to prevent accidents. Files are cleaned at start up. They are
alphabatized by key and duplicate info is deleted. Files can also be edited in the nano text editor.

Settings:
Toggle file saving
Toggle masking, which covers private stuff.
Toggle debug mode, which prints errors.

Web Repl:
Use the repl when you leave this app at home. If you need a password quickly, use your key. Nothing is saved on the
repl.


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

Upon finishing your edit and exiting, you will be asked if you want to save your edit. Type "yes" or "y" to save your
edit to the file you have selected. The file will be overwritten by the edit and encrypted. Type "no" or "n" to cancel
the edit.


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
-2 to run the file cleaner
-3 to generate sample files

-LEGAL-
Disclaimer:
So, in plain terms, this app should be used with some care. It is about as secure as a basket of keys. If you keep it
behind a locked door, your keys should stay put because only trusted people get anywhere near them. By analogy this
app is the basket, and your computer is the door. You should be sure that your computer is secured and safe before
using this app. No information produced in whole or part by this app is garenteed to be perfectly safe. Your files
can be read, modified, or deleted. The app source code can also be read, modfied, or deleted, which would cause
unpredictable effects while running the app. Back up important things; store your passwords in a few safe places.
Keep untrustworthy people off your computer. Do not store your passwords publicly, or generate them with keys
that are easy to guess. Stay safe!

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

-SOURCES-
Clear Screen
https://www.csestack.org/clear-python-interpreter-console/
Copy to Clipboard
https://stackoverflow.com/questions/11063458/python-script-to-copy-text-to-clipboard
Encryption
https://www.geeksforgeeks.org/encoding-and-decoding-base64-strings-in-python/
Get Current Working Directory
https://note.nkmk.me/en/python-os-getcwd-chdir/
License
https://choosealicense.com/
Nano
https://www.nano-editor.org/dist/latest/nano.html
Password Masking
https://stackoverflow.com/questions/9202224/getting-a-hidden-password-input

-NOTES-
Keybrid is written in Python3 and Batch for Windows.
Keybird is open source.
Developed by Andrew Vella
Copyright (c) 2022
@PixelatedStarfish on Github and Itch
andyjvella@gmail.com
Thank you for using Keybird!
