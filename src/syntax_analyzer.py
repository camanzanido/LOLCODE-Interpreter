from src.keyword_classifiers import *

def syntax_analyzer(lexemes):
    # lexemes = [('flag', 'Variable Identifier'), ('ITZ', 'Variable Declaration'), ('WIN', 'TROOF Literal'), ....]

    # Filtered lexemes
    array_lexemes = comments_remover(lexemes)
    symbol_table = []
    index = 0
    lexemes_length = len(array_lexemes)
    concat_string = ""

    # Consume function: Proceeds to the next token
    def consume(expected_token):
        nonlocal index
        if index < lexemes_length and array_lexemes[index][0] == expected_token:
            # Increment index/position: Next token
            index += 1
        else:
            raise SyntaxError(f"Expected '{expected_token}', but got '{array_lexemes[index][0]}'")
    
    # <program> ::= HAI <block> KTHXBYE
    def parse_program():
        nonlocal index
        lexeme = array_lexemes[index][0]
        if lexeme == "HAI":
            consume(lexeme)
            parse_block() 
            consume("KTHXBYE")
        else:
            raise SyntaxError(f"Expected 'HAI' at the start, but got '{lexeme}'")

    # <block> ::= <output> | <variable_declarations> | <input> | <variable_assignment>
    def parse_block():
        nonlocal index
        while index < lexemes_length:
            lexeme = array_lexemes[index][0]
            lexeme_type = array_lexemes[index][1]
            if lexeme == "VISIBLE":
                parse_output()
            elif lexeme == "WAZZUP":
                parse_variable_declarations()
            elif lexeme == "GIMMEH":
                parse_input()
            elif lexeme_type == ID_VAR:
                parse_assignment()
            else:
                break

    # <input> ::= GIMMEH <var_ident> 
    def parse_input():
        nonlocal index
        lexeme = array_lexemes[index][0]
        if lexeme == "GIMMEH":
            consume(lexeme)
            if index < lexemes_length and array_lexemes[index][1] == ID_VAR:
                consume(array_lexemes[index][0])
            else:
                print("Error: Hindi ko pa alam")

    # <output> ::= VISIBLE <expression>
    def parse_output():
        nonlocal index
        lexeme = array_lexemes[index][0]
        if lexeme == "VISIBLE":
            consume(lexeme)
            while index < lexemes_length:
                parse_expression()
                if index < lexemes_length and array_lexemes[index][0] == "AN":
                    consume("AN")
                else:
                    break
    
    # =========== EXPRESSIONS ============
    # <expression> ::= <arithmetic op> | <smoosh op> | var | literal
    def parse_expression():
        nonlocal index
        lexeme = array_lexemes[index][0]
        lexeme_type = array_lexemes[index][1]
        if lexeme_type in [LIT_YARN, LIT_NUMBR, LIT_NUMBAR, LIT_TROOF, ID_VAR]:
            consume(lexeme)
            if lexeme_type == LIT_NUMBAR:
                lexeme = float(lexeme)
            elif lexeme_type == LIT_NUMBR:
                lexeme = int(lexeme)
            return lexeme
        elif lexeme_type == KW_ARITHMETIC:
            value = parse_arithmethic_operations()
            return value
        elif lexeme_type == KW_CONCATENATE:
            parse_concatenation()
        else:
            print("Error: Hindi ko pa alam")

   # <arithmethic> ::= <operations> <literal|var_indent|arithmethic> AN <literal|var_indent|arithmethic>
    def parse_arithmethic_operations():
        nonlocal index
        lexeme = array_lexemes[index][0]
        lexeme_type = array_lexemes[index][1]

        if lexeme_type == KW_ARITHMETIC:
            operator = lexeme
            consume(lexeme)

            # Operand 1
            operand1 = operand()

            # AN
            if index < lexemes_length and array_lexemes[index][0] == "AN":
                consume("AN")
                # Operand 2
                operand2 = operand()

            # Evaluate 
            if operator == "SUM OF":
                return operand1 + operand2
            elif operator == "DIFF OF":
                return operand1 - operand2
            elif operator == "PRODUKT OF":
                return operand1 * operand2
            elif operator == "QUOSHUNT OF":
                return operand1 / operand2
            elif operator == "MOD OF":
                return operand1 % operand2
            elif operator == "BIGGR OF":
                return max(operand1, operand2)
            elif operator == "SMALLR OF":
                return min(operand1, operand2)
            else:
                print(f"Unknown arithmetic operation: {operator}")

    # <literal|var_indent|arithmethic>
    def operand():
        nonlocal index
        lexeme = array_lexemes[index][0]
        lexeme_type = array_lexemes[index][1]

        # Return the literal value or variable value
        if lexeme_type == ID_VAR:
            consume(lexeme)
            # Retrieve the variable's value from the symbol table
            value = get_variable_value(lexeme)
            return value

        elif lexeme_type == LIT_NUMBR:
            consume(lexeme)
            return int(lexeme)

        elif lexeme_type == LIT_NUMBAR:
            consume(lexeme)
            return float(lexeme)

        # Evaluate recursively
        elif lexeme_type == KW_ARITHMETIC:
            return parse_arithmethic_operations()

        else:
            print(f"Invalid operand type: {lexeme_type}")


    # <concatenate> ::= SMOOSH <expr> AN [<expr> | (<expr> AN)*]
    def parse_concatenation():
        nonlocal index
        lexeme = array_lexemes[index][0]
        lexeme_type = array_lexemes[index][1]
        # SMOOSH keyword
        if lexeme_type == KW_CONCATENATE:
            consume(lexeme)
            while index < lexemes_length:
                # expressions
                parse_expression()
                if index < lexemes_length and array_lexemes[index][0] == "AN":
                    consume("AN")
                else:
                    break
            # MKAY delimiter
            if index < lexemes_length and array_lexemes[index][1] == DELIM_EXPR_END:
                consume(array_lexemes[index][0])

    # <assignment> ::= var_indent R <typecasting> | var_ident R <expr>
    def parse_assignment():
        nonlocal index
        lexeme = array_lexemes[index][0]
        lexeme_type = array_lexemes[index][1]

        if lexeme_type == ID_VAR:
            # var_ident
            consume(lexeme)
            # R
            if index < lexemes_length and array_lexemes[index][1] == ASSIGNMENT_VAR:
                consume(array_lexemes[index][0])
                # Type casting
                if index < lexemes_length and array_lexemes[index][1] == KW_TYPECAST:
                    parse_type_casting()
                # Expression
                else:
                    parse_expression()
            # Type casting
            elif index < lexemes_length and array_lexemes[index][0] == "IS NOW A":
                parse_type_casting()
            else:
                print("Error: Hindi ko pa alam")


    def parse_type_casting():
        nonlocal index
        lexeme = array_lexemes[index][0]
        lexeme_type = array_lexemes[index][1]
        # <type_casting> ::= MAEK var_ident <literal> 
        if lexeme == "MAEK":
            consume(lexeme)
            if index < lexemes_length and array_lexemes[index][1] == ID_VAR:
                variable = array_lexemes[index][0]
                consume(variable)
                if index < lexemes_length and array_lexemes[index][0] in ["NUMBAR", "NUMBR", "YARN", "TROOF"]:
                    consume(array_lexemes[index][0])
         # <type_casting> ::= IS NOW A <literal> 
        elif lexeme == "IS NOW A":
            consume(lexeme)
            if index < lexemes_length and array_lexemes[index][1] == LIT:
                consume(array_lexemes[index][0])

    # <variable_declarations> ::= WAZZUP <variable_declaration> BUHBYE
    def parse_variable_declarations():
        nonlocal index
        lexeme = array_lexemes[index][0]
        if lexeme == "WAZZUP":
            consume(lexeme)
            # Variable declarations
            while index < lexemes_length and array_lexemes[index][0] == "I HAS A":
                parse_variable_declaration()
            # Delimter
            consume("BUHBYE")

    # <variable_declaration> ::= I HAS A varident | I HAS A varident ITZ <expr>
    def parse_variable_declaration():
        nonlocal index
        lexeme = array_lexemes[index][0]
        # I HAS A
        if lexeme == "I HAS A":
            consume(lexeme)
            # var_ident
            if index < lexemes_length and array_lexemes[index][1] == ID_VAR:
                variable = array_lexemes[index][0]
                consume(variable)
                # ITZ
                if index < lexemes_length and array_lexemes[index][0] == "ITZ":
                    consume("ITZ")
                    # expr
                    symbol_table.append([variable, parse_expression()])
                else:
                    symbol_table.append([variable, "NOOB"])
            else:
                print("Error: Hindi ko pa alam")

    # ------------------- HELPER FUNCTIONS -------------------
    def get_variable_value(var_name):
        for var, value in symbol_table:
            if var == var_name:
                return value
        print(f"Variable '{var_name}' not found")
    
    def existing_var(variable, new_value):
        for pair in symbol_table:
            if pair[0] == variable:
                pair[1] = new_value
                return True
        return False

    # Start parsing the program
    parse_program()
    print("Syntax analysis successful!")
    print("Symbol Table: ", symbol_table)

def comments_remover(array_lexemes):
    filtered_lexemes = []

    for tokens in array_lexemes:
        type_of_token = tokens[1]

        if type_of_token not in [KW_COMMENT_START, COMMENT, KW_COMMENT_DELIM]:
            # If the condition is met, add the item to the filtered_data list
            filtered_lexemes.append(tokens)

    # Return or print the filtered data list
    return filtered_lexemes
