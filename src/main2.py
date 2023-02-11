import nltk
import sys
import os

global aplphabet
global alphanumeric
global possibleCommands
global possibleControlStructures
global possibleConditions

alphabet = "abcdefghijklmnñopqrstuvwxyz"
alphanumeric = alphabet + "0123456789"
possibleCommands = {
        "assingto":(("num"), ("var")),
        "goto": (("num","var"),("num","var")),
        "move": (("num"),("var")),
        "turn": (("dirT")),
        "face": (("ori")),
        "put":  (("num","var"),("obj")),
        "pick": (("num","var"),("obj")),
        "movetothe": (("num","var"),("dir")),
        "moveindir": (("num","var"),("ori")),
        "jumptothe": (("num","var"),("dir")),
        "jumpindir": (("num","var"),("ori")),
        "nop": ()
    }
possibleControlStructures = ("if", "while", "repeat")
# if: condition then: Block1 else: Block2
# while: condition do: Block
# repeat: n block
possibleConditions = {
    "facing": ["O"],
    "canput": ["n", "X"],
    "canpick": ["n", "X"],
    "canmoveindir": ["n", "D"],
    "canjumpindir": ["n", "D"],
    "canmovetothe": ["n", "O"],
    "canjumptothe": ["n", "O"],
    "not": ["cond"]
}

def conditionCheck(condition: str, variables: list, methods: dict) -> bool:
    # facing: O – where O is one of: north, south, east, or west
    # canPut: n , X – where X can be chips or balloons, and n is a number or a variable
    # canPick: n , X – where X can be chips or balloons, and n is a number or a variable
    # canMoveInDir: n , D – where D is one of: north, south, east, or west
    # canJumpInDir: n, D – where D is one of: north, south, east, or west
    # canMoveToThe: n ,O – where O is one of: front, right, left, or back
    # canJumpToThe: n, O – where O is one of: front, right, left, or back
    # not: cond – where cond is a condition
    flag = True
    # Check if the condition is valid
    if condition in possibleConditions:
        # Check if the condition has the correct number of arguments
        if len(possibleConditions[condition]) != len(condition.split(",")):
            return False
        # Check if the arguments are valid
        for i in range(len(possibleConditions[condition])):
            if possibleConditions[condition][i] == "O":
                # Check if the argument is a direction
                if condition.split(",")[i] not in ["north", "south", "east", "west"]:
                    return False
            elif possibleConditions[condition][i] == "n":
                # Check if the argument is a number or a variable
                if condition.split(",")[i] not in variables:
                    try:
                        int(condition.split(",")[i])
                    except ValueError:
                        return False
            elif possibleConditions[condition][i] == "X":
                # Check if the argument is an object
                if condition.split(",")[i] not in ["Chips", "Ballons"]:
                    return False
            elif possibleConditions[condition][i] == "D":
                # Check if the argument is a direction
                if condition.split(",")[i] not in ["north", "south", "east", "west"]:
                    return False
            elif possibleConditions[condition][i] == "cond":
                # Check if the argument is a condition
                if condition.split(",")[i] not in possibleConditions:
                    return False
    return flag

def blockCheck(instruction: str, variables: list, methods: dict) -> bool:
    # Loop to find the ":" and get the instruction name
    idx = 0
    for char in instruction:
        if char == ":":
            break
        idx += 1
    # Get the instruction name
    name = instruction[:idx]
    body = instruction[idx:]
    # Check for command
    if name in possibleCommands:
        # Get the arguments
        args = body.split(",")
        # Check if the number of arguments is correct
        if len(args) != len(possibleCommands[name]):
            return False
        # Check if the arguments are valid
        for i in range(len(args)):
            if possibleCommands[name][i] == "num":
                # Check if the argument is a number
                try:
                    int(args[i])
                except ValueError:
                    return False
            elif possibleCommands[name][i] == "var":
                # Check if the argument is a variable
                if args[i] not in variables:
                    return False
            elif possibleCommands[name][i] == "dirT":
                # Check if the argument is a direction
                if args[i] not in ["left", "right", "around"]:
                    return False
            elif possibleCommands[name][i] == "ori":
                # Check if the argument is an orientation
                if args[i] not in ["north", "south", "east", "west"]:
                    return False
            elif possibleCommands[name][i] == "obj":
                # Check if the argument is an object
                if args[i] not in ["Chips", "Ballons"]:
                    return False
            elif possibleCommands[name][i] == "dir":
                # Check if the argument is a direction
                if args[i] not in ["left", "right", "front", "back"]:
                    return False
    # Check for control structures
    elif name in possibleControlStructures:
        # Check if it's an if
        if name == "if":
            # Get the condition
            condition = body.split("then:")[0]
            # Check if the condition is valid
            if not conditionCheck(condition, variables, methods):
                return False
            # Get the blocks
            blocks = body.split("then:")[1].split("else:")
            # Check if the blocks are valid
            for block in blocks:
                # Check if the block is valid
                if not blockCheck(block, variables, methods):
                    return False
        # Check if it's a while
        elif name == "while":
            # Get the condition
            condition = body.split("do:")[0]
            # Check if the condition is valid
            if not conditionCheck(condition, variables, methods):
                return False
            # Get the block
            block = body.split("do:")[1]
            # Check if the block is valid
            if not blockCheck(block, variables, methods):
                return False
        # Check if it's a repeat
        elif name == "repeat":
            # Get the number of times to repeat
            times = body.split("block")[0]
            # Check if the number is valid
            try:
                int(times)
            except ValueError:
                return False
            # Get the block
            block = body.split("block")[1]
            # Check if the block is valid
            if not blockCheck(block, variables, methods):
                return False
    # Check if it's a method
    elif name in methods:
        # Get the arguments
        args = body.split(",")
        # Check if the number of arguments is correct
        if len(args) != len(methods[name]["args"]):
            return False
        # Check if the arguments are valid
        for i in range(len(args)):
            if methods[name]["args"][i] == "num":
                # Check if the argument is a number
                try:
                    int(args[i])
                except ValueError:
                    return False
            elif methods[name]["args"][i] == "var":
                # Check if the argument is a variable
                if args[i] not in variables:
                    return False
            elif methods[name]["args"][i] == "dirT":
                # Check if the argument is a direction
                if args[i] not in ["left", "right", "around"]:
                    return False
            elif methods[name]["args"][i] == "ori":
                # Check if the argument is an orientation
                if args[i] not in ["north", "south", "east", "west"]:
                    return False
            elif methods[name]["args"][i] == "obj":
                # Check if the argument is an object
                if args[i] not in ["Chips", "Ballons"]:
                    return False
            elif methods[name]["args"][i] == "dir":
                # Check if the argument is a direction
                if args[i] not in ["left", "right", "front", "back"]:
                    return False
    return True


def instructionsCheck(variables: dict, methods: dict) -> tuple:
    flag = True
    # Check every method body, ignore last one since it is instructions
    for method in methods.values()[:-1]:
        # Remove the "[" and "]" from the body at the start and end
        body = method["body"][1:-1]
        # Get their arguments, separated by "|" and "|" at the start of body, no arguments is "||", after them are the instructions
        if body.startswith("|"):
            body = body[1:]
        else:
            flag = False
        argstr = ""
        idx = 0
        for char in body:
            # These are the arguments, stop when the "|" is found
            if char == "|":
                break
            argstr += char
            idx += 1
        # Divide arguments by "," and check if they are valid if they start with a letter and are alphanumeric
        args = argstr.split(",")
        for arg in args:
            if arg[0] not in alphabet:
                flag = False
            for char in arg:
                if char not in alphanumeric:
                    flag = False
        # Store the arguments in the method
        method["args"] = args
        # Remove the arguments from the body
        body = body[idx+1:]
        # Get the instructions, they are separated by ";", do split and check each one
        instructionslst = body.split(";")
        # Subordinate the cheking of instruction blocks
        for instruction in instructionslst:
            flag = blockCheck(instruction, variables, methods)
    return methods, flag

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
    lines = lines[lastidx:]
    return variables, lines, flag

def procsCheck(lines: str, variables: dict) -> tuple:
    flag = True
    methods = {}
    # Check existance of procs
    if not lines.startswith("procs"):
        #print("false in #1")
        flag = False
    # Remove procs from str
    lines = lines[5:]
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
                method["name"] = "instructionsblock0"
            else:
                method["name"] = lines[:i]
            lines = lines[i:]
            i = 0
            #print("TEST: ", method["name"], lines)
            # Get the body of the method
            unclosed = 0
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
                    break
        i += 1
    # If there are no methods, flag is False
    if len(methods) == 0:
        #print("false in #2")
        flag = False
    # All methods must have name, except for the last one. They must also have body, if emtpy then flag is False
    for key in methods:
        if key == "" or key[0] not in alphabet:
            #print("false in #3")
            flag = False
        # key must start with a letter and have alfanumeric characters
        for char in key:
            if char not in alphanumeric:
                #print("false in #4")
                flag = False
        if methods[key].get("body") == None:
            #print("false in #5")
            flag = False
        elif methods[key]["body"] == "":
            #print("false in #6")
            flag = False
    # # Print for testing
    # print(f"\nMethods:")
    # for key in methods:
    #     print(f"\nkey = {key} : body = {methods[key]}")
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
    methods, flag = instructionsCheck(variables, methods)
    print(f"\nVariables: {variables}")
    #print(f"\nMethods: {methods}")
    for i in methods:
        print(f"\nKey: {i}")
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
            try:
                if syntax(lines):
                    print("\nSyntax is correct!\n")
                else:
                    print("\nSyntax is incorrect!\n")
            except Exception as e:
                print(f"\nSyntax is incorrect!\n")
            file.close()
            end = input("Enter to continue or 'stop' to finish\n")
            if end == "stop":
                os.system('cls')
                sys.exit()            
        except FileNotFoundError:
            print("\nFile not found!\n")


if "__main__" == __name__:
    main()