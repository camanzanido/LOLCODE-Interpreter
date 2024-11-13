import re

def lexemes_matcher ():
    
    file = open("input.txt", "r")
    lines = file.readlines()

    token_dict = {}

    # Per line of the code
    for line in lines:

        line = line.strip()
        
        if (re.search("^HAI$", line) != None):
           token_dict["HAI"] = "Code Delimiter"
        
        elif (re.search("^KTHXBYE$", line) != None):
           token_dict["KTHXBYE"] = "Code Delimiter"
        
        elif (re.search("^PRODUKT OF$", line) != None):
           token_dict["PRODUKT OF"] = "Random String"

        elif (re.search("^QUOSHUNT OF$", line) != None):
            token_dict["QUOSHUNT OF"] = "Random String"
        
        elif (re.search("^MOD OF$", line) != None):
            token_dict["MOD OF"] = "Random String"

        elif (re.search("^BIGGR OF$", line) != None):
            token_dict["BIGGR OF"] = "Random String"
        
        elif (re.search("^SMALLR OF$", line) != None):
            token_dict["SMALLR OF"] = "Random String"
        
        elif (re.search("^BOTH OF$", line) != None):
            token_dict["BOTH OF"] = "Random String"

        elif (re.search("^EITHER OF$", line) != None):
            token_dict["EITHER OF"] = "Random String"

        elif (re.search("^WON OF$", line) != None):
            token_dict["WON OF"] = "Random String"

        elif (re.search("^NOT$", line) != None):
            token_dict["NOT"] = "Random String"

        elif (re.search("^ANY OF$", line) != None):
            token_dict["ANY OF"] = "Random String"

        elif (re.search("^ALL OF$", line) != None):
            token_dict["ALL OF"] = "Random String"
        
        elif (re.search("^BOTH SAEM$", line) != None):
            token_dict["BOTH SAEM"] = "Random String"

        elif (re.search("^DIFFRINT$", line) != None):
            token_dict["DIFFRINT"] = "Random String"

        elif (re.search("^SMOOSH$", line) != None):
            token_dict["SMOOSH"] = "Random String"

        elif (re.search("^MAEK$", line) != None):
            token_dict["MAEK"] = "Random String"

        elif (re.search("^A$", line) != None):
            token_dict["A"] = "Random String"

        elif (re.search("^IS NOW A$", line) != None):
            token_dict["IS NOW A"] = "Random String"

        elif (re.search("^VISIBLE$", line) != None):
            token_dict["VISIBLE"] = "Random String"

        elif (re.search("^GIMMEH$", line) != None):
            token_dict["GIMMEH"] = "Random String"

        elif (re.search("^O RLY\?$", line) != None):
            token_dict["O RLY?"] = "Random String"

        elif (re.search("^YA RLY$", line) != None):
            token_dict["YA RLY"] = "Random String"

        elif (re.search("^MEBBE$", line) != None):
            token_dict["MEBBE"] = "Random String"

        elif (re.search("^NO WAI$", line) != None):
            token_dict["NO WAI"] = "Random String"

        elif (re.search("^OIC$", line) != None):
            token_dict["OIC"] = "Random String"

        elif (re.search("^WTF\?$", line) != None):
            token_dict["WTF?"] = "Random String"

        elif (re.search("^OMG$", line) != None):
            token_dict["OMG"] = "Random String"

        elif (re.search("^OMGWTF$", line) != None):
            token_dict["OMGWTF"] = "Random String"

        elif (re.search("^IM IN YR$", line) != None):
            token_dict["IM IN YR"] = "Random String"

        elif (re.search("^UPPIN$", line) != None):
            token_dict["UPPIN"] = "Random String"

        elif (re.search("^NERFIN$", line) != None):
            token_dict["NERFIN"] = "Random String"

        elif (re.search("^YR$", line) != None):
            token_dict["YR"] = "Random String"

        elif (re.search("^TIL$", line) != None):
            token_dict["TIL"] = "Random String"

        elif (re.search("^WILE$", line) != None):
            token_dict["WILE"] = "Random String"
        
        elif (re.search("^IM OUTTA YR$", line) != None):
            token_dict["IM OUTTA YR"] = "Random String"

        elif (re.search("^HOW IZ I$", line) != None):
            token_dict["HOW IZ I"] = "Random String"

        elif (re.search("^IF U SAY SO$", line) != None):
            token_dict["IF U SAY SO"] = "Random String"

        elif (re.search("^GTFO$", line) != None):
            token_dict["GTFO"] = "Random String"

        elif (re.search("^FOUND YR$", line) != None):
            token_dict["FOUND YR"] = "Random String"

        elif (re.search("^I IZ$", line) != None):
            token_dict["I IZ"] = "Random String"

        elif (re.search("^MKAY$", line) != None):
            token_dict["MKAY"] = "Random String"

    print(token_dict)

lexemes_matcher()