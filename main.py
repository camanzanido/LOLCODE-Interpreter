import re

def lexemes_matcher ():
    
    file = open("input.txt", "r")
    lines = file.readlines()

    token_dict = {}

    # Per line of the code
    for line in lines:
        
        if (re.search("^HAI$", line) != None):
           token_dict["HAI"] = "Code Delimiter"
        
        elif (re.search("^KTHXBYE$", line) != None):
           token_dict["KTHXBYE"] = "Code Delimiter"

    print(token_dict)

lexemes_matcher()