from src.keyword_classifiers import *

def syntax_analyzer(lexemes):
    # lexemes = [('flag', 'Variable Identifier'), ('ITZ', 'Variable Declaration'), ('WIN', 'TROOF Literal'), ....]

    # Filtered lexemes
    lexemes = comments_remover(lexemes)
    symbol_table = []
    index = 0

    # Consume function: Proceeds to the next token
    def consume(expected_token):
        nonlocal index
        if index < len(lexemes) and lexemes[index][0] == expected_token:
            # Increment index/position: Next token
            index += 1
        else:
            raise SyntaxError(f"Expected '{expected_token}', but got '{lexemes[index][0]}'")
    
    # <program> ::= HAI <block> KTHXBYE
    def parse_program():
        nonlocal index
        if lexemes[index][0] == "HAI":
            consume("HAI")
            parse_block() 
            consume("KTHXBYE")
        else:
            raise SyntaxError(f"Expected 'HAI' at the start, but got '{lexemes[index][0]}'")
    
    # <block> ::= <output> <variable_declarations> <input>
    def parse_block():
        nonlocal index
        while index < len(lexemes):
            if lexemes[index][0] == "VISIBLE":
                parse_output()
            elif lexemes[index][0] == "WAZZUP":
                parse_variable_declarations()
            elif lexemes[index][0] == "GIMMEH":
                parse_input()
            else:
                break

    # <output> ::= VISIBLE <literal> | VISIBLE <var_ident> | VISIBLE <arithmethic>
    def parse_output():
        nonlocal index
        if lexemes[index][0] == "VISIBLE":
            # Visible
            consume("VISIBLE")
            # Checks if the succeding code/type is valid
            if index < len(lexemes) and lexemes[index][1] in [LIT_YARN, LIT_NUMBR, LIT_NUMBAR, ID_VAR]:
                consume(lexemes[index][0]) 
            elif index < len(lexemes) and lexemes[index][1] == KW_ARITHMETIC:
                parse_arithmethic_operations()
            else:
                print("Error: Hindi ko pa alam")

    # <input> ::= GIMMEH <var_ident> 
    def parse_input():
        nonlocal index
        if lexemes[index][0] == "GIMMEH":
            # Visible
            consume("GIMMEH")
            # Checks if the succeding code/type is valid
            if index < len(lexemes) and lexemes[index][1] == ID_VAR:
                consume(lexemes[index][0]) 
            else:
                print("Error: Hindi ko pa alam")

    # <variable_declarations> ::= WAZZUP <variable_declaration> BUHBYE
    def parse_variable_declarations(): 
        nonlocal index
        if lexemes[index][0] == "WAZZUP":
            # WAZZUP 
            consume("WAZZUP")
            # Variable Declarations
            while index < len(lexemes) and lexemes[index][0] == "I HAS A":
                parse_variable_declaration()
            # BUHBYE (end)
            consume("BUHBYE")

    # <variable_declaration> ::= I HAS A varident | I HAS A varident ITZ <expr>
    def parse_variable_declaration():
        nonlocal index
        if lexemes[index][0] == "I HAS A":
            # I HAS A keyword
            consume("I HAS A")
            # Variable identifier
            if index < len(lexemes) and lexemes[index][1] == ID_VAR:
                # Saves the variable
                variable = lexemes[index][0]
                consume(lexemes[index][0]) 
                # Checks if initialized
                # ITZ
                if index < len(lexemes) and lexemes[index][0] == "ITZ":
                    consume(lexemes[index][0])
                    # Value (YARN|NUMBR|NUMBAR) 
                    if index < len(lexemes) and lexemes[index][1] in [LIT_YARN, LIT_NUMBR, LIT_NUMBAR, LIT_TROOF]:
                        value = lexemes[index][0]
                        # Conversion
                        if (lexemes[index][1] == LIT_NUMBAR):
                            value = float(value)
                        elif (lexemes[index][1] == LIT_NUMBR):
                            value = int (value)
                        # Append the variable and value to the symbol table
                        symbol_table.append([variable, value])
                        consume(lexemes[index][0]) 
                    # Expression
                    elif index < len(lexemes) and lexemes[index][1] == KW_ARITHMETIC:
                        parse_arithmethic_operations()
                else:
                    symbol_table.append([variable, "NOOB"])
            else:
                print("Error: Hindi ko pa alam")

    # <arithmethic> ::= <operations> <literal|var_indent|arithmethic> AN <literal|var_indent|arithmethic>
    def parse_arithmethic_operations():
        nonlocal index
        # <operations>
        if lexemes[index][1] == KW_ARITHMETIC:
            consume(lexemes[index][0])
            # Operand 1
            # <literal|var_indent>
            if index < len(lexemes) and (lexemes[index][1] in [ID_VAR, LIT_NUMBAR, LIT_NUMBR]):
                consume(lexemes[index][0])
            # <arithmetic>
            elif (index < len(lexemes) and lexemes[index][1] == KW_ARITHMETIC):
                parse_arithmethic_operations() 
            # AN (separator of the two operands)
            if index < len(lexemes) and lexemes[index][0] == "AN":
                # Operand 2
                consume(lexemes[index][0])
                # <literal|var_indent>
                if index < len(lexemes) and (lexemes[index][1] in [ID_VAR, LIT_NUMBAR, LIT_NUMBR]):
                    consume(lexemes[index][0])
                # <arithmetic>
                elif (index < len(lexemes) and lexemes[index][1] == KW_ARITHMETIC):
                    parse_arithmethic_operations()

    # Start parsing the program
    parse_program()
    print("Syntax analysis successful!")
    print("Symbol Table: ", symbol_table)

def comments_remover(lexemes):
    filtered_lexemes = []

    for tokens in lexemes:
        type_of_token = tokens[1]

        if type_of_token not in [KW_COMMENT_START, COMMENT, KW_COMMENT_DELIM]:
            # If the condition is met, add the item to the filtered_data list
            filtered_lexemes.append(tokens)

    # Return or print the filtered data list
    return filtered_lexemes
