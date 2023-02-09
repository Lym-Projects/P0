import nltk
import sys
import os

def conditionCheck():
    pass

def varsCheck(lines: str) -> tuple:
    flag = True
    variables = {}
    # Check if str starts with VARS
    if not lines.startswith("VARS"):
        flag = False
    # Remove VARS from str
    lines = lines[4:]
    # Get variables names
        # Loop through the str to find the ";", make a copy of the str and cut it [:i] and do split(","), this list is the variables
    varstr = lines
    lastidx = 0
    for i in range(len(lines)):
        if lines[i] == ";":
            varstr = lines[:i].split(",")
            lastidx = i
            break
    # Add the variables to the dictionary, default value is "none"
    for var in varstr:
        variables[var] = "none"
    # Remove the variables from str
    lines = lines[lastidx+1:]
    return variables, lines, flag

def procsCheck(lines: str, variables: dict) -> tuple:
    flag = True
    methods = {}
    # Remove PROCS and the methods itself from str
    return methods, lines, flag

def syntax(lines: list) -> bool:
    flag = True
    # Convert lines to string to manage them easier
    lines = "".join(nltk.word_tokenize("\n".join(lines)))
    print(lines)
    # Check if str starts with ROBOT_R
    if not lines.startswith("ROBOT_R"):
        flag = False
    # Remove ROBOT_R from str
    lines = lines[7:]
    # Look for VARS or PROCS
    variables = {}
    methods = {}
    if lines.startswith("VARS") and flag:
        variables, lines, flag = varsCheck(lines)
    elif lines.startswith("PROCS") and flag:
        methods, lines, flag = procsCheck(lines, variables)
    return flag

def main():
    while True:
        os.system('cls')
        filename = input("¡Hi! What's the file name you want to open? ('stop' to finish)\n\n")
        if filename == "stop":
            os.system('cls')
            sys.exit()
        # Testing files are localed in data of this workspace
        filename = "data/" + filename
        try:
            file = open(filename, "r")
            print("\nFile opened successfully!\n")
            lines = file.readlines()
            if syntax(lines):
                print("\nSyntax is correct!\n")
            else:
                print("\nSyntax is incorrect!\n")
            file.close()
            end = input("Enter to continue or 'stop' to finish\n")
            if end == "stop":
                os.system('cls')
                sys.exit()            
        except FileNotFoundError:
            print("\nFile not found!\n")


if "__main__" == __name__:
    main()