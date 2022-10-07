from Ui import Terminal, GUI
from sys import argv

def usage():   
    print(f"""
Usage: {argv[0]} [g | t]
g : play with the GUI
t : play with the Terminal""")
    quit()

if __name__ == "__main__":
    if len(argv) != 2:
        usage()
    if argv[1] == 'g':
        ui = GUI()
        ui.run()
        pass
    elif argv[1] == 't':
        ui = Terminal()
        ui.run()
    else:
        usage()

