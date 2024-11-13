import re

def lexemes_matcher (line):
    token_list = []

    # If the line contains 'BTW' followed by any text, exit early
    if re.search("^BTW .*$", line) != None:
        return token_list

    # Handle the case where 'BTW' is in the line
    if 'BTW' in line:
        line = line.split('BTW')[0].strip()

    if re.search("^HAI$", line) != None:
        token_list.append("HAI")
        token_list.append("Code Delimiter")
        
    elif re.search("^KTHXBYE$", line) != None:
        token_list.append("KTHXBYE")
        token_list.append("Code Delimiter")

    elif re.search("^WAZZUP$", line) != None:
        token_list.append("WAZZUP")
        token_list.append("Code Delimiter")

    elif re.search("^BUHBYE$", line) != None:
        token_list.append("BUHBYE")
        token_list.append("Code Delimiter")
        
    elif re.search("^BTW$", line) != None:
        token_list.append("BTW")
        token_list.append("Code Delimiter")

    elif re.search("^OBTW$", line) != None:
        token_list.append("OBTW")
        token_list.append("Code Delimiter")

    elif re.search("^VISIBLE$", line) != None:
        token_list.append("VISIBLE")
        token_list.append("Code Delimiter")

    elif re.search("^TLDR$", line) != None:
        token_list.append("TLDR")
        token_list.append("Code Delimiter")

    elif re.search("^I HAS A ", line) != None:
        token_list.append("I HAS A")
        token_list.append("Code Delimiter")

    elif re.search("^ITZ$", line) != None:
        token_list.append("ITZ")
        token_list.append("Code Delimiter")

    elif re.search("^R$", line) != None:
        token_list.append("R")
        token_list.append("Code Delimiter")
        
    elif re.search("^SUM OF $", line) != None:
        token_list.append("SUM OF")
        token_list.append("Code Delimiter")
        
    elif re.search("^DIFF OF $", line) != None:
        token_list.append("DIFF OF")
        token_list.append("Code Delimiter")
        
    elif re.search("^[a-zA-Z][a-zA-Z0-9_]* ", line) != None:
        variable = re.search("[a-zA-Z][a-zA-Z0-9_]* ", line).group()
        token_list.append(variable)
        token_list.append("Variable Identifier")
    return token_list


def lexemes_init():
  
    file = open("input.txt", "r")
    lines = file.readlines()

    token_dict = {}

    # Per line of the code
    for line in lines:
        
        line = line.strip()
        while line != "":
            token = lexemes_matcher(line)
            if token != []:
                token_dict[token[0]] = token[1]
                line = line.replace(token[0], "").strip()
            else:
                break
    
    for key, value in token_dict.items():
        print(f"{key}: {value}")


lexemes_init()

