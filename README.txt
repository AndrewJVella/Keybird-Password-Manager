-FIRST START UP-
To download from Github select the zip file "Keybird Inside", click on it, then click "view raw".

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

Important Operations:
^G Help
^X  Exit; go back to Keybird
up and down arrowsScroll
M-U:Undo
M-E:Redo

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
No information produced in whole or part by this app is guaranteed to be perfectly safe. Your files
can be read, modified, or deleted. The app source code can also be read, modified, or deleted, which would cause
unpredictable effects while running the app. Back up important things; store your passwords in a few safe places.
Keep untrustworthy people off your computer. Do not store your passwords publicly, or generate them with keys
that are easy to guess. Stay safe!

No birds were harmed in the making of Keybird, including the program, online material, documentation, and photography.
Wild robin were photographed eating berries from a park tree.

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

-ERRORS AND DEBUG MODE-
Errors happen, and a well designed program can handle them fairly well There are two kinds of errors that Keybird is
designed to handle:

A Permission Error - these occur when Keybird attempts to modify a file that is open or in use.
A General Error    - these occur when Keybird functions incorrectly.

Errors are reported in Python3 as tracebacks through the call stack. The line number and function in source are shown
as well as the type of of error that occurred. Sometimes errors occur while an error is being handled, in this case a
message will indicate as such, and more information will be printed.

In typical use the traceback will not be printed. You will be given a prompt that indicates an error has occurred and
you can close the app by pressing enter (return). If you would like to see debug information, run Keybird in
DEBUG mode, which can be toggled on and in the Settings menu. If DEBUG mode is off, you can still type "debug",
"traceback", or "report" to get the debug info. That said, I want to keep the error message as simple as I can, to
prevent needless confusion. No one wants to see a wall of text when they are trying to understand what just happened!

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
Keybird is open source.
Version 2.3.0
Developed by Andrew Vella
Copyright (c) 2022
@PixelatedStarfish on Github and Itch
andyjvella@gmail.com
Thank you for using Keybird!
