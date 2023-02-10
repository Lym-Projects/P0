import nltk
import sys
import os

def conditionCheck():
    pass

def varsCheck(lines: str) -> tuple:
    aplphabet = "abcdefghijklmnñopqrstuvwxyz"
    flag = True
    variables = {}
    # Check if str starts with VARS
    if not lines.startswith("vars"):
        flag = False
    # Remove VARS from str
    lines = lines[4:]
    # Get variables names
        # Loop through the str to find "procs", make a copy of the str and cut it [:i] and do split(","), this list is the variables
    varstr = lines
    lastidx = 0
    for i in range(len(lines)):
        if lines[i:i+5] == "procs":
            varstr = lines[:i].split(",")
            lastidx = i
            break
    # Check if variables are valid, only condition is that it must start with a letter
    for var in varstr:
        if var[0] not in aplphabet:
            flag = False
    # Add the variables to the dictionary, default value is "none"
    for var in varstr:
        variables[var] = "none"
    # Remove the variables from str
    lines = lines[lastidx+1:]
    return variables, lines, flag

def procsCheck(lines: str, variables: dict) -> tuple:
    flag = True
    methods = {}
    # Check existance of procs
    if not lines.startswith("procs"):
        flag = False
    # Remove procs from str
    lines = lines[4:]
    print(f"\n{lines}")
    # Make method object and try to separate every method (starts and ends with [] but be careful with nested [])
    method = {}
    i = 0
    count = 0
    while True:
        if lines[i] == "[":
            count += 1
            method["name"] = lines[:i]
            # Find the right closing bracket
            unclosedbrakets = 1
            for j in range(i+1, len(lines)):
                if lines[j] == "[":
                    unclosedbrakets += 1
                elif lines[j] == "]":
                    if unclosedbrakets == 1:
                        method["body"] = lines[i:j]
                        methods[method["name"]] = method
                        i = j+1
                        break
        
        i += 1
    # If there are no methods, flag is Fa
    return methods, lines, flag

def syntax(lines: list) -> bool:
    flag = True
    # Convert lines to string to manage them easier
    lines = "".join(nltk.word_tokenize("\n".join(lines))).lower()
    print(lines)
    # Check if str starts with ROBOT_R
    if not lines.startswith("robot_r"):
        flag = False
    # Remove ROBOT_R from str
    lines = lines[7:]
    # Look for VARS or PROCS
    variables = {}
    methods = {}
    if lines.startswith("vars") and flag:
        variables, lines, flag = varsCheck(lines)
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