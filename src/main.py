import nltk
import sys
import os

global aplphabet
global alphanumeric

alphabet = "abcdefghijklmnñopqrstuvwxyz"
alphanumeric = alphabet + "0123456789"

def conditionCheck():
    pass

def varsCheck(lines: str) -> tuple:
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
            # If there's an "" var, then flag false
            for var in varstr:
                if var == "":
                    flag = False
            lastidx = i
            break
    # Check if variables are valid, only condition is that it must start with a letter
    for var in varstr:
        if var[0] not in alphabet:
            flag = False
        for char in var:
            if char not in alphanumeric:
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
    # Make method object and try to separate every method (starts and ends with [] but be careful with nested [])
    i = 0
    while True:
        #print(f"{lines[i:]}")
        method = {}
        if i >= len(lines):
            break
        # Get the name of the method
        if lines[i] == "[":
            # After it finds the candidate to instructions block (last one) then we will use red flag if there's even another method
            if lines[:i] == "]":
                method["name"] = "instructions block"
            else:
                method["name"] = lines[:i]
            lines = lines[i:]
            i = 0
            #print("TEST: ", method["name"], lines)
            # Get the body of the method
            unclosed = 0
            print(lines[i])
            for j in range(i, len(lines)):
                if lines[j] == "]":
                    unclosed -= 1
                elif lines[j] == "[":
                    unclosed += 1
                if unclosed == 0:
                    method["body"] = lines[i:j+1]
                    # Add method to methods dictionary
                    methods[method["name"]] = method
                    if j+1 < len(lines):
                        if lines[j+1] == "[":
                            lines = lines[j:]
                        else:
                            lines = lines[j+1:]
                    else:
                        lines = lines[j+1:]
                    i = 0
                    print(f"\nTest: {method['name']} = {method['body']}")
                    break
            if "body" not in method:
                flag = False
        i += 1
    # If there are no methods, flag is False
    if len(methods) == 0:
        flag = False
    # All methods must have name, except for the last one. They must also have body, if emtpy then flag is False
    for key in methods:
        if key == "" or key[0] not in alphabet:
            flag = False
        # key must start with a letter and have alfanumeric characters
        for char in key:
            if char not in alphanumeric:
                flag = False
        if methods[key]["body"] == "":
            flag = False
    # Print for testing
    for key in methods:
        #print(f"\nName: {methods[key]['name']}\nBody: {methods[key]['body']}")
        pass

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