# wtDxLite
Python program to pass DX cluster spots from DXLite to Win-Test

## Installation

### Windows

Install Python 3 [https://www.python.org/downloads/] (Important - when prompted, ensure you also install 'pip')
Install PyQT4:
* Download latest WHL file for your Python 3 version from http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4
* Install using `pip3 install [filename].whl` from the command line
Install PyZMQ:
* Install using `pip3 install zmq` from the command line

### Linux

Install Python 3 & PyQT4
* `apt-get install python3 python3-pip python3-pyqt4`
Install PyZMQ:
* `pip3 install zmq`

## Usage
Start wtDxLite.py from the command line or double-click. You will be prompted for the broadcast address for the network - this should match the setting in Win-Test (Options > Configure Interfaces). The port number is currently assumed to be 9871 - the Win-Test default.

### Why would you use it?
I created this 'Just Because I Could', however there are a couple of reasons I can think of in which it might be useful:
* You wish to run the cluster software on a non-logging and/or non-Windows PC
* You wish to use a cluster that does not support sending spots, to prevent accidental spotting

## Credits
Thanks are due to Michael G7VJR for the DXLite tool which this program uses. (http://dxlite.g7vjr.org/) 
More info on the Zero Message Queue: http://g7vjr.org/2013/09/dxlite-implemented-as-a-zero-message-queue-json/