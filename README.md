# ChessGame
This chess engen created to win StockFish11, it is based on deep learning with a new model.

Requirements:
- python 3.7.6 or >
- pygame module
- 12 Gb ram memory or > # if you want to train the model


1/ Setting up python:

Ubuntu 20.04 and other versions of Debian Linux ship with Python 3 pre-installed. To make sure that our versions are up-to-date, 
let’s update and upgrade the system with the apt command to work with Ubuntu’s Advanced Packaging Tool:

$ sudo apt update
$ sudo apt -y upgrade

The -y flag will confirm that we are agreeing for all items to be installed, but depending on your version of Linux, you may need to confirm additional prompts as your system updates and upgrades.

Once the process is complete, we can check the version of Python 3 that is installed in the system by typing: 

$ python3 -V

You’ll receive output in the terminal window that will let you know the version number. While this number may vary, the output will be similar to this:

Output
Python 3.8.2

To manage software packages for Python, let’s install pip, a tool that will install and manage programming packages we may want to use in our development projects. You can learn more about modules or packages that you can install with pip by reading “How To Import Modules in Python 3.”

$ sudo apt install -y python3-pip

Python packages can be installed by typing:

$ pip3 install package_name

Here, package_name can refer to any Python package or library, such as Django for web development or NumPy for scientific computing. So if you would like to install NumPy, you can do so with the command pip3 install numpy.

There are a few more packages and development tools to install to ensure that we have a robust setup for our programming environment:

$ sudo apt install -y build-essential libssl-dev libffi-dev python3-dev
