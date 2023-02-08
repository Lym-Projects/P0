#import nltk




def syntax(lines: list) -> bool:
    flag = False
    return flag

def main():
    while True:
        filename = input("\nHi\nWhat's the file name you want to open?\n\n")
        try:
            file = open(filename, "r")
            print("\nFile opened successfully!\n")
            lines = file.readlines()
            if syntax(lines):
                print("\nSyntax is correct!\n")
            else:
                print("\nSyntax is incorrect!\n")
            file.close()
        except FileNotFoundError:
            print("\nFile not found!\n")


if "__Main__" == __name__:
    main()