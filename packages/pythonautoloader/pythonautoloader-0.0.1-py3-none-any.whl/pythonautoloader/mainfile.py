# imports
import os
import json
import csv
import time

# vars
maindir = (os.path.dirname(os.path.realpath(__file__)))


class mainclass():

    # main functions
    def main():
        script = "def main(): \n     print('hello world!') \nmain()"
        f = open("main.py", "a+")
        f.truncate(0)
        f.write(script)
        f.close()
        time.sleep(2)
        exec(open(maindir + '\main.py').read())

    # run function main
    main()
