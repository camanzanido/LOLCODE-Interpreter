import re
from src import keyword_classifiers

def lexemes_matcher (line):
    token_list = []

    if re.search("^BTW .*$", line) != None:
        return token_list

    if 'BTW' in line:
        line = line.split('BTW')[0].strip()

    # Code Delimiters
    if re.search("^HAI$", line) != None:
        token_list.append("HAI")
        token_list.append(keyword_classifiers.DELIM_CODE)
        
    elif re.search("^KTHXBYE$", line) != None:
        token_list.append("KTHXBYE")
        token_list.append(keyword_classifiers.DELIM_CODE)

    # Variables
    elif re.search("^WAZZUP$", line) != None:
        token_list.append("WAZZUP")
        token_list.append(keyword_classifiers.DELIM_DECLARATION)

    elif re.search("^BUHBYE$", line) != None:
        token_list.append("BUHBYE")
        token_list.append(keyword_classifiers.DELIM_DECLARATION)
        
    elif re.search("^I HAS A( )?", line) != None:
        token_list.append("I HAS A")
        token_list.append(keyword_classifiers.DECLARATION_VAR)

    elif re.search("^ITZ( )?", line) != None:
        token_list.append("ITZ")
        token_list.append(keyword_classifiers.DECLARATION_VAR)

    # Comments
    elif re.search("^BTW$", line) != None:
        token_list.append("BTW")
        token_list.append(keyword_classifiers.KW_COMMENT)

    elif re.search("^OBTW$", line) != None:
        token_list.append("OBTW")
        token_list.append(keyword_classifiers.KW_COMMENT)

    # Input/Output
    elif re.search("^GIMMEH( )?", line) != None:
        token_list.append("GIMMEH")
        token_list.append(keyword_classifiers.KW_INPUT)

    elif re.search("^VISIBLE( )?", line) != None:
        token_list.append("VISIBLE")
        token_list.append(keyword_classifiers.KW_OUTPUT)

    elif re.search("^TLDR$", line) != None:
        token_list.append("TLDR")
        token_list.append(keyword_classifiers.KW_COMMENT)

    # Assignment
    elif re.search("^R( )?", line) != None:
        token_list.append("R")
        token_list.append(keyword_classifiers.ASSIGNMENT_VAR)

    # Arithmetic
    elif re.search("^SUM OF( )?", line) != None:
        token_list.append("SUM OF")
        token_list.append(keyword_classifiers.KW_ARITHMETIC)
        
    elif re.search("^DIFF OF( )?", line) != None:
        token_list.append("DIFF OF")
        token_list.append(keyword_classifiers.KW_ARITHMETIC)

    elif re.search("^PRODUKT OF( )?", line) != None:
        token_list.append("PRODUKT OF")
        token_list.append(keyword_classifiers.KW_ARITHMETIC)
    
    elif re.search("^QUOSHUNT OF( )?", line) != None:
        token_list.append("QUOSHUNT OF")
        token_list.append(keyword_classifiers.KW_ARITHMETIC)
    
    elif re.search("^MOD OF( )?", line) != None:
        token_list.append("MOD OF")
        token_list.append(keyword_classifiers.KW_ARITHMETIC)
    
    elif re.search("^BIGGR OF( )?", line) != None:
        token_list.append("BIGGR OF")
        token_list.append(keyword_classifiers.KW_ARITHMETIC)
    
    elif re.search("^SMALLR OF( )?", line) != None:
        token_list.append("SMALLR OF")
        token_list.append(keyword_classifiers.KW_ARITHMETIC)
    
    # Boolean
    elif re.search("^BOTH OF( )?", line) != None:
        token_list.append("BOTH OF")
        token_list.append(keyword_classifiers.KW_BOOLEAN)

    elif re.search("^EITHER OF( )?", line) != None:
        token_list.append("EITHER OF")
        token_list.append(keyword_classifiers.KW_BOOLEAN)

    elif re.search("^WON OF( )?", line) != None:
        token_list.append("WON OF")
        token_list.append(keyword_classifiers.KW_BOOLEAN)

    elif re.search("^NOT( )?", line) != None:
        token_list.append("NOT")
        token_list.append(keyword_classifiers.KW_BOOLEAN)

    elif re.search("^ANY OF( )?", line) != None:
        token_list.append("ANY OF")
        token_list.append(keyword_classifiers.KW_BOOLEAN)

    elif re.search("^ALL OF( )?", line) != None:
        token_list.append("ALL OF")
        token_list.append(keyword_classifiers.KW_BOOLEAN)
    
    # Comparison
    elif re.search("^BOTH SAEM( )?", line) != None:
        token_list.append("BOTH SAEM")
        token_list.append(keyword_classifiers.KW_COMPARISON)

    elif re.search("^DIFFRINT( )?", line) != None:
        token_list.append("DIFFRINT")
        token_list.append(keyword_classifiers.KW_COMPARISON)

    # Concatenation
    elif re.search("^SMOOSH( )?", line) != None:
        token_list.append("SMOOSH")
        token_list.append(keyword_classifiers.KW_CONCATENATE)

    # Typecasting
    elif re.search("^MAEK( )?", line) != None:
        token_list.append("MAEK")
        token_list.append(keyword_classifiers.KW_TYPECAST)

    elif re.search("^IS NOW A( )?", line) != None:
        token_list.append("IS NOW A")
        token_list.append(keyword_classifiers.KW_TYPECAST)

    # Separator
    elif re.search("^A( )?", line) != None:
        token_list.append("A")
        token_list.append(keyword_classifiers.KW_SEPARATOR)

    elif re.search("^AN( )?", line) != None:
        token_list.append("AN")
        token_list.append(keyword_classifiers.KW_SEPARATOR)

    # If-Then 
    elif re.search(r"^O RLY\?( )?", line) != None:
        token_list.append("O RLY?")
        token_list.append(keyword_classifiers.KW_CONDITION)

    elif re.search("^YA RLY( )?", line) != None:
        token_list.append("YA RLY")
        token_list.append(keyword_classifiers.KW_CONDITION)

    elif re.search("^MEBBE( )?", line) != None:
        token_list.append("MEBBE")
        token_list.append(keyword_classifiers.KW_CONDITION)

    elif re.search("^NO WAI( )?", line) != None:
        token_list.append("NO WAI")
        token_list.append(keyword_classifiers.KW_CONDITION )

    elif re.search("^OIC( )?", line) != None:
        token_list.append("OIC")
        token_list.append(keyword_classifiers.DELIM_CONDITION )

    # Switch-Case
    elif re.search(r"^WTF\?( )?", line) != None:
        token_list.append("WTF?")
        token_list.append(keyword_classifiers.KW_CONDITION )

    elif re.search("^OMG( )?", line) != None:
        token_list.append("OMG")
        token_list.append(keyword_classifiers.KW_CONDITION )

    elif re.search("^OMGWTF( )?", line) != None:
        token_list.append("OMGWTF")
        token_list.append(keyword_classifiers.KW_CONDITION )

    # Loop
    elif re.search("^IM IN YR( )?", line) != None:
        token_list.append("IM IN YR")
        token_list.append(keyword_classifiers.KW_LOOP)

    elif re.search("^UPPIN( )?", line) != None:
        token_list.append("UPPIN")
        token_list.append(keyword_classifiers.KW_LOOP)

    elif re.search("^NERFIN( )?", line) != None:
        token_list.append("NERFIN")
        token_list.append(keyword_classifiers.KW_LOOP)

    elif re.search("^YR( )?", line) != None:
        token_list.append("YR")
        token_list.append(keyword_classifiers.KW_LOOP)

    elif re.search("^TIL( )?", line) != None:
        token_list.append("TIL")
        token_list.append(keyword_classifiers.ID_LOOP)

    elif re.search("^WILE( )?", line) != None:
        token_list.append("WILE")
        token_list.append(keyword_classifiers.ID_LOOP)
    
    elif re.search("^IM OUTTA YR( )?", line) != None:
        token_list.append("IM OUTTA YR")
        token_list.append(keyword_classifiers.KW_LOOP)

    # Function
    elif re.search("^HOW IZ I( )?", line) != None:
        token_list.append("HOW IZ I")
        token_list.append(keyword_classifiers.ID_FUNC)

    elif re.search("^IF U SAY SO( )?", line) != None:
        token_list.append("IF U SAY SO")
        token_list.append(keyword_classifiers.KW_FUNCTION )

    # Return
    elif re.search("^GTFO( )?", line) != None:
        token_list.append("GTFO")
        token_list.append(keyword_classifiers.DELIM_CONDITION)

    elif re.search("^FOUND YR( )?", line) != None:
        token_list.append("FOUND YR")
        token_list.append(keyword_classifiers.DELIM_CONDITION )

    # Calling
    elif re.search("^I IZ( )?", line) != None:
        token_list.append("I IZ")
        token_list.append(keyword_classifiers.KW_FUNCTION )

    elif re.search("^MKAY( )?", line) != None:
        token_list.append("MKAY")
        token_list.append(keyword_classifiers.DELIM_EXPR_END)

    # Data Type
    elif re.search(r"^(-)?[0-9]+( )?", line) != None:
        numbr = re.search(r"^(-)?[0-9]+( )?", line).group()
        token_list.append(numbr)
        token_list.append(keyword_classifiers.LIT_NUMBR)
    
    elif re.search(r"^(-)?[0-9]+\.[0-9]+( )?", line) != None:
        numbar = re.search(r"^(-)?[0-9]+\.[0-9]+( )?", line).group()
        token_list.append(numbar)
        token_list.append(keyword_classifiers.LIT_NUMBAR)

    elif re.search(r'^"([^":]|:\)|:>|:o|:"|::)*"( )?', line) != None:
        yarn = re.search(r'^"([^":]|:\)|:>|:o|:"|::)*"( )?', line).group()
        token_list.append(yarn)
        token_list.append(keyword_classifiers.LIT_YARN )
    
    elif re.search("^(WIN|FAIL)( )?", line) != None:
        troof = re.search("[a-zA-Z][a-zA-Z0-9_]*( )?", line).group()
        token_list.append(troof)
        token_list.append(keyword_classifiers.LIT_TROOF)
    
    elif re.search("^(NOOB|NUMBR|NUMBAR|YARN|TROOF)( )?", line) != None:
        type = re.search("[a-zA-Z][a-zA-Z0-9_]*( )?", line).group()
        token_list.append(type)
        token_list.append(keyword_classifiers.LIT)

    elif re.search("^[a-zA-Z][a-zA-Z0-9_]*( )?", line) != None:
        variable = re.search("[a-zA-Z][a-zA-Z0-9_]*( )?", line).group()
        token_list.append(variable)
        token_list.append(keyword_classifiers.ID_VAR)
    
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
                token_dict[token[0].strip()] = token[1].strip()
                line = line.replace(token[0], "").strip()
              
            else:
                break
    
    for key, value in token_dict.items():
        print(f"{key} \t\t {value}")


lexemes_init()
