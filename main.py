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

        elif (re.search("^WAZZUP$", line) != None):
           token_dict["WAZZUP"] = "Code Delimiter"

        elif (re.search("^BUHBYE$", line) != None):
           token_dict["BUHBYE"] = "Code Delimiter"
        
        elif (re.search("^BTW$", line) != None):
           token_dict["BTW"] = "Code Delimiter"

        elif (re.search("^OBTW$", line) != None):
           token_dict["OBTW"] = "Code Delimiter"

        elif (re.search("^TLDR$", line) != None):
           token_dict["TLDR"] = "Code Delimiter"

        elif (re.search("^I HAS A$", line) != None):
           token_dict["I HAS A"] = "Code Delimiter"

        elif (re.search("^ITZ$", line) != None):
           token_dict["ITZ"] = "Code Delimiter"

        elif (re.search("^R$", line) != None):
           token_dict["R"] = "Code Delimiter"
        
        elif (re.search("^SUM OF$", line) != None):
           token_dict["SUM OF"] = "Code Delimiter"

        elif (re.search("^DIFF OF$", line) != None):
           token_dict["DIFF OF"] = "Code Delimiter"

      

    print(token_dict)

lexemes_matcher()