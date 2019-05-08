To install packages in requirement.txt file you will need Python, version 3.x will be okay.

Before you can install Pip on your server, you’ll need to confirm that Python is installed.

# Check for Python
The simplest way to test for a Python installation on your Windows server is to open a command prompt (click on the Windows icon and type cmd, then click on the command prompt icon). Once a command prompt window opens, type python and press Enter. If Python is installed correctly, you should see output similar to what is shown below:

Python 3.7.0 (v3.7.0:1bf9cc5093, Jun 27 2018, 04:59:51) [MSC v.1914 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.

If you receive a message like:

Python is not recognized as an internal or external command, operable program or batch file.
Python is either not installed or the system variable path hasn’t been set. 
You’ll need to either launch Python from the folder in which it is installed or adjust your 
system variables to allow Python to be launched from any location. 

# Installing Pip
Once you’ve confirmed that Python is correctly installed, you can proceed with installing Pip.

Download get-pip.py to a folder on your computer.
Open a command prompt and navigate to the folder containing get-pip.py.
Run the following command:
python get-pip.py
Pip is now installed!
You can verify that Pip was installed correctly by opening a command prompt and entering the following command:

pip -V

You should see output similar to the following:

pip 18.0 from c:\users\administrator\appdata\local\programs\python\python37\lib\site-packages\pip 
(python 3.7)

Now that Pip is installed and configured, you can begin using it to manage your Python packages. 
For a brief overview of the available commands and syntax for Pip, 
open a command prompt and enter:

pip help

# Install Requirements with pip

use the python commnad:
pip install -r /path/to/requirements.txt

To install all requirements for the project.

Admin username: The password

Thank You.