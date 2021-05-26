# ADis Chat System using pyro (python)

#### Tested on Windows 10, Python 3.9.5
> Required packages: `PyQt5` and `Pyro4`.

To run the App (GUI):
1. open a terminal and run:
```sh
python control.py
```
2. Start a nameserver.
3. Create as many clients as you want.


To run the App (Terminal/CMD):
1. open a terminal and run:
```sh
python -m Pyro4.naming
```
> **Note:** if you do not run the 1st step the connection will fail.
2. To instantiate a chat client open a new terminal and run: (can be run multiple times)
```sh
python client.py
```
