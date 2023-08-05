INSTALL:

pip3 install python-shell

How to use:

Step 1:

First create a file containing python code(will be executed when given command is used).
The file does not have to have a .py extension.

To add arguments to your command, do it like this:

args = REPLACEME

for demonstration purposes i will use this simple code:


----------------------------------------------------------

args = REPLACEME

if(args[0] == "help"):
    print("This command prints whatever you want. Arguments: [text to print]")
else:
    for text in args:
        print(text + " ", end="")
    
----------------------------------------------------------

Step 2:

Create a new shell instance and add the command like this:

-----------------------------------------------------------

from python-shell import shell

cmdline = shell()
cmdline.add_command("echo", "/home/kiki/myfirstpythonscript/cmd/echo")

------------------------------------------------------------

Now, simply start the shell by adding this:

cmdline.start()
