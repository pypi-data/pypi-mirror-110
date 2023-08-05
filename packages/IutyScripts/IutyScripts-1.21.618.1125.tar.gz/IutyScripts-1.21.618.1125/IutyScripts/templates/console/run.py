import sys,os


def getArgv():
    if len(sys.argv) == 0:
        return None
    return sys.argv.pop(0)

if __name__ == "__main__":
    getArgv()
    cmd = getArgv()
    if not cmd:
        print("no command recorgnised")
        input()
    
    
    pass