from src.keyword_classifiers import *

def syntax_analyzer(lexemes):
    # lexemes = [('flag', 'Variable Identifier'), ('ITZ', 'Variable Declaration'), ('WIN', 'TROOF Literal'), ....]

    # Filtered lexemes
    array_lexemes = comments_remover(lexemes)
    symbol_table = []
    index = 0
    it = 0
    lexemes_length = len(array_lexemes)

    # Consume function: Proceeds to the next token
    def consume(expected_token):
        nonlocal index
        if index < lexemes_length and array_lexemes[index][0] == expected_token:
            # Increment index/position: Next token
            index += 1
        else:
            print(f"Expected '{expected_token}', but got '{array_lexemes[index][0]}'")
    
    # <program> ::= HAI <block> KTHXBYE
    def parse_program():
        nonlocal index
        lexeme = array_lexemes[index][0]
        if lexeme == "HAI":
            consume(lexeme)
            parse_block() 
            consume("KTHXBYE")
        else:
            print(f"Expected 'HAI' at the start, but got '{lexeme}'")

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
                parse_variable_reassignment()
            elif lexeme == "O RLY?":
                parse_if_else_statements()
            elif lexeme == "WTF?":
                parse_switch_case_statement()
            elif lexeme == "IM IN YR":
                parse_loop()
            else:
                break

    # <input> ::= GIMMEH <var_ident> 
    def parse_input():
        nonlocal index, it
        lexeme = array_lexemes[index][0]
        if lexeme == "GIMMEH":
            consume(lexeme)
            if index < lexemes_length and array_lexemes[index][1] == ID_VAR:
                variable = array_lexemes[index][0]
                consume(array_lexemes[index][0])
                # Ask for an input in the terminal
                value = input(f"{variable}: ")
                parsed_value = parse_value(value)
                it = parsed_value
                # Update the symbol table
                update_variable_value(variable, parsed_value)
            else:
                print("1")
                print("Error: Hindi ko pa alam")


    # <output> ::= VISIBLE <expression>
    def parse_output():
        nonlocal index
        lexeme = array_lexemes[index][0]
        if lexeme == "VISIBLE":
            consume(lexeme)
            # Parse the expression until AN is read
            while index < lexemes_length:
                parse_expression()
                if index < lexemes_length and array_lexemes[index][0] == "AN":
                    consume("AN")
                else:
                    break
    
    # ===================================================================== EXPRESSIONS =====================================================================
    # <expression> ::= <arithmetic op> | <smoosh op> | var | literal
    def parse_expression():
        nonlocal it     # this will hold the value of the expression for the if-then
        nonlocal index
        lexeme = array_lexemes[index][0]
        lexeme_type = array_lexemes[index][1]
        if lexeme_type in [LIT_YARN, LIT_NUMBR, LIT_NUMBAR, LIT_TROOF, ID_VAR]:
            consume(lexeme)
            if lexeme_type == LIT_NUMBAR:
                lexeme = float(lexeme)
            elif lexeme_type == LIT_NUMBR:
                lexeme = int(lexeme)
            elif lexeme_type == ID_VAR:
                lexeme = get_variable_value(lexeme)
            return lexeme
        elif lexeme_type == KW_ARITHMETIC:
            value = parse_arithmethic_operations()
            it = value
            print(f"it: {it}")
            return value
        elif lexeme_type == KW_CONCATENATE:
            value = parse_concatenation()
            return value
        elif lexeme_type == KW_BOOLEAN:
            value = parse_boolean_operations()
            it = value
            print(f"it: {it}")
            return value
        elif lexeme_type == KW_COMPARISON:
            value = parse_comparison_operations()
            it = value
            print(f"it: {it}")
            return value
        else:
            print("3")
            print("Error: Hindi ko pa alam")

    # ===================================================================== ARITHMETHIC OPERATIONS =====================================================================
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
        
        elif lexeme_type == LIT_TROOF:
            consume(lexeme)
            if lexeme == "WIN":
                return 1
            else:
                return 0
            
        elif lexeme_type == LIT_YARN:
            consume(lexeme)
            return parse_value(lexeme)
        
        # Evaluate recursively
        elif lexeme_type == KW_ARITHMETIC:
            return parse_arithmethic_operations()
        elif lexeme_type == KW_BOOLEAN:
            return parse_boolean_operations()
        elif lexeme_type == KW_COMPARISON:
            return parse_comparison_operations()

        else:
            print(f"Invalid operand type: {lexeme_type}")

    # ===================================================================== SMOOSH KEYWORD =====================================================================
    # <concatenate> ::= SMOOSH <expr> AN [<expr> | (<expr> AN)*]
    def parse_concatenation():
        nonlocal index
        lexeme = array_lexemes[index][0]
        lexeme_type = array_lexemes[index][1]
        concat_string = ""
        # SMOOSH keyword
        if lexeme_type == KW_CONCATENATE:
            consume(lexeme)
            while index < lexemes_length:
                # expressions
                # concatenate the result of the expressions
                concat_string += str(parse_expression())
                if index < lexemes_length and array_lexemes[index][0] == "AN":
                    consume("AN")
                else:
                    break
            # MKAY delimiter
            if index < lexemes_length and array_lexemes[index][1] == DELIM_EXPR_END:
                consume(array_lexemes[index][0])
            return concat_string
    
    # ===================================================================== VARIABLE REASSIGNMENT =====================================================================
    # <assignment> ::= var_indent R <typecasting> | var_ident R <expr>
    def parse_variable_reassignment():
        nonlocal index
        lexeme = array_lexemes[index][0]
        lexeme_type = array_lexemes[index][1]

        if lexeme_type == ID_VAR:
            variable = lexeme
            # var_ident
            consume(lexeme)
            # R
            if index < lexemes_length and array_lexemes[index][1] == ASSIGNMENT_VAR:
                consume(array_lexemes[index][0])
                # Perform Type casting 
                if index < lexemes_length and array_lexemes[index][1] == KW_TYPECAST:
                    parse_type_casting(variable)
                # Reassign the evaluated expression
                else:
                    update_variable_value(variable, parse_expression())
            # Perform Type casting 
            elif index < lexemes_length and array_lexemes[index][0] == "IS NOW A":
                parse_type_casting(variable)
            else:
                print("2")
                print("Error: Hindi ko pa alam")

    # <typecasting> ::= MAEK var_ident literal | IS NOW A literal
    def parse_type_casting(variable):
        nonlocal index
        lexeme = array_lexemes[index][0]
        lexeme_type = array_lexemes[index][1]
        # <type_casting> ::= MAEK var_ident <literal> 
        if lexeme == "MAEK":
            consume(lexeme)
            # var_ident
            if index < lexemes_length and array_lexemes[index][1] == ID_VAR:
                variable = array_lexemes[index][0]
                consume(variable)
                # Literal
                if index < lexemes_length and array_lexemes[index][1] == LIT:
                    lexeme = array_lexemes[index][0]
                    consume(array_lexemes[index][0])
                    # Update the symbol table given the new recasted value
                    new_type_value = recast_variable_value(variable, lexeme)
                    update_variable_value(variable, new_type_value)
         # <type_casting> ::= IS NOW A <literal> 
        elif lexeme == "IS NOW A":
            consume(lexeme)
            if index < lexemes_length and array_lexemes[index][1] == LIT:
                lexeme = array_lexemes[index][0]
                consume(array_lexemes[index][0])
                 # Update the symbol table given the new recasted value
                new_type_value = recast_variable_value(variable, lexeme)
                update_variable_value(variable, new_type_value)

    # ===================================================================== VARIABLE DECLARATIONS =====================================================================
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
                print("4")
                print("Error: Hindi ko pa alam")

    # <boolean_op> :: = BOTH OF <expr> AN <expr> | EITHER OF <expr> AN <expr> | WON OF <expr> AN <expr> | NOT <expr> | ALL OF <expr> MKAY | ANY OF <expr> MKAY
    def parse_boolean_operations():
        nonlocal index
        lexeme = array_lexemes[index][0]
        lexeme_type = array_lexemes[index][1]

        if lexeme_type == KW_BOOLEAN:
            operator = lexeme
            consume(lexeme)

            operand1 = operand()
            operand2 = None

            # AN 
            if index < lexemes_length and array_lexemes[index][0] == "AN":
                consume("AN")
                operand2 = operand()

            if operator == "BOTH OF":
                if operand2 is not None:
                    print(f"and : {operand1 and operand2}")
                    return operand1 and operand2
            elif operator == "EITHER OF":
                if operand2 is not None:
                    print(f"or : {operand1 or operand2}")
                    return operand1 or operand2

            elif operator == "WON OF":
                if operand2 is not None:
                    print(f"won: {bool(operand1) ^ bool(operand2)}")
                    return bool(operand1) ^ bool(operand2)
                # else:
                #     raise SyntaxError("Expected second operand for 'WON OF'")

            elif operator == "NOT":
                print(f"not : {not operand1}")
                return not operand1
            
            # since ALL OF & ANY OF cannot be nested, separate to other boolean operations that can be nested
            elif operator == "ALL OF" or operator == "ANY OF":
                operands = []
                # get all operands until MKAY
                oper = operand()
                print(f"oper:{oper}")
                if oper not in ["BOTH OF", "EITHER OF", "NOT", "WON OF"]:
                    operands.append(oper)

                while index < lexemes_length and array_lexemes[index][0] != "MKAY":
                    if index < lexemes_length and array_lexemes[index][0] == "AN":
                        consume("AN")
                        oper = operand()
                        print(f"oper:{oper}")
                        operands.append(oper) # append in the list
                    # AN
                    
                # MKAY
                consume("MKAY")

                if operator == "ALL OF":
                    print(f"all : {all(operands)}")
                    return all(operands) 
                elif operator == "ANY OF":
                    print(f"any : {any(operands)}")
                    return any(operands)
            else:
                print(f"Unknown arithmetic operation: {operator}")
    # <comparison_op> ::= BOTH SAEM <expr> AN <expr> | DIFFRINT <expr> AN <expr>
    def parse_comparison_operations():
        nonlocal index
        lexeme = array_lexemes[index][0]
        lexeme_type = array_lexemes[index][1]

        if lexeme_type == KW_COMPARISON:
            operator = lexeme
            consume(lexeme)
            # Operand 1
            operand1 = operand()
            # AN
            if index < lexemes_length and array_lexemes[index][0] == "AN":
                consume("AN")
                # Operand 2
                operand2 = operand()
            if operator == "BOTH SAEM":     # x == y
                print(f"== : {operand1==operand2}")
                return operand1 == operand2
            elif operator ==  "DIFFRINT":   # x != y
                print(f"!= : {operand1!=operand2}")
                return operand1 != operand2
            elif operator == "BIGGR OF":  
                print(f"> : {max(operand1,operand2)}")
                return max(operand1, operand2)
            elif operator == "SMALLR OF": 
                print(f"< : {min(operand1,operand2)}") 
                return min(operand1, operand2)
            else:
                print(f"Unknown arithmetic operation: {operator}")

    #<if-then> ::= <expr><linebreak>O RLY?<linebreak>YA RLY<linebreak> <code_block> <linebreak> <else-if>* <linebreak> NO WAI <linebreak> <code_block> <linebreak>OIC
    def parse_if_else_statements():  # Note: NO MEBBE YET
        nonlocal index, it
        lexeme = array_lexemes[index][0]
        condition = []          
        condition.append(it) 
        if lexeme == "O RLY?":
            consume(lexeme)
            cond = condition[0]
            # while index < lexemes_length and array_lexemes[index][0] != "OIC" or index < lexemes_length and array_lexemes[index][0] != "NO WAI" :
            curr_lexeme = array_lexemes[index][0]
            if cond and curr_lexeme == "YA RLY":
                consume("YA RLY")
                parse_code_block()

            elif not cond and array_lexemes[index][0] == "NO WAI":
                    consume("NO WAI")
                    parse_code_block()
            # Delimter
            if array_lexemes[index][0] == "OIC":
                consume("OIC")

    def parse_code_block():
        nonlocal index
        while index < lexemes_length:
            lexeme = array_lexemes[index][0]
            lexeme_type = array_lexemes[index][1]
            if lexeme == "VISIBLE":
                parse_output()
            elif lexeme == "GIMMEH":
                parse_input()
            elif lexeme_type == ID_VAR:
                parse_variable_reassignment()
            elif lexeme_type == "O RLY?":
                parse_if_else_statements()
            else:
                break

    # <switch-case> ::= WTF? <linebreak> <case>+ <linebreak> <default_case>?  OIC
    def parse_switch_case_statement():
        nonlocal index, it
        lexeme = array_lexemes[index][0]
        # cond = array_lexemes[index-1][0]
        # print(cond)
        # print(get_variable_value(cond))
        condition = it
        matched = False
        if lexeme == "WTF?":
           # operator = lexeme
            consume(lexeme)
            while index < lexemes_length and array_lexemes[index][0] != "OIC":
                curr_lexeme = array_lexemes[index][0]

                if curr_lexeme == "OMG":
                    consume("OMG")
                    print(array_lexemes[index][0])
                    print(type(array_lexemes[index][0]))        # hindi na typecast
                    if not matched and condition == array_lexemes[index][0]:
                        print("in omg")
                        matched = True
                        consume(array_lexemes[index][0])
                        while index < lexemes_length and array_lexemes[index][0] != "GTFO":
                            parse_code_block()
                        consume("GTFO")

                elif not matched and curr_lexeme == "OMGWTF":
                    consume("OMGWTF")
                    while index < lexemes_length and array_lexemes[index][0] != "GTFO":
                        parse_code_block()
                    consume("GTFO")
            # Delimter
            consume("OIC")

    # IM IN YR <label> operation YR varident (<til_op> | <wile_op>) <linebreak> <code_block><linebreak> IM OUTTA YR <label>
    def parse_loop():
        nonlocal index
        lexeme = array_lexemes[index][0]

        if lexeme == "IM IN YR":
            consume("IM IN YR")
            label = array_lexemes[index][0]
            consume(label)
            
            # UPPIN or NERFIN
            operation = array_lexemes[index][0]
            if operation not in ["UPPIN", "NERFIN"]:
               print(f"Expected 'UPPIN' or 'NERFIN', found {operation}")
            consume(operation)
            consume("YR")
            varident = array_lexemes[index][0]
            consume(varident)
            
            # WILE or TIL
            condition_type = array_lexemes[index][0]
            if condition_type not in ["WILE", "TIL"]:
                print(f"Expected 'WILE' or 'TIL', found {condition_type}")
            consume(condition_type)
        
               # WILE 
            if condition_type == 'WILE':
                while parse_comparison_operations():  
                    var_value = get_variable_value(varident)
                    print("in wile")
                    # parse_code_block()
                    if operation == "NERFIN":
                        var_value -= 1
                    else:
                        var_value += 1
                    update_variable_value(varident, var_value)
                    print(var_value)
            else:  # TIL
                while not parse_comparison_operations(): 
                    var_value = get_variable_value(varident)
                    print("in til")
                    # parse_code_block()
                    if operation == "NERFIN":
                        var_value -= 1
                    else:
                        var_value += 1
                    update_variable_value(varident, var_value)
                    print(var_value)

            if array_lexemes[index][0] == "IM OUTTA YR":
                consume("IM OUTTA YR")
                consume(label)  
            
            
    # ------------------- HELPER FUNCTIONS -------------------
    # Function for returning symbol table value
    def get_variable_value(var_name):
        for var, value in symbol_table:
            if var == var_name:
                return value
        print(f"Variable '{var_name}' not found")
    
    # Parser
    def parse_value(value):
        # Remove quotes from YARN literals
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        try:
            return int(value) 
        except ValueError:
            pass 
        try:
            return float(value)  
        except ValueError:
            pass  
        return value

    # Function for updating the symbol table
    def update_variable_value(variable, parsed_value):
        for i in range(len(symbol_table)):
            if symbol_table[i][0] == variable:
                symbol_table[i][1] = parsed_value
                return
        symbol_table.append([variable, parsed_value])

    # Recast function
    def recast_variable_value(variable, new_type):
        for var, value in symbol_table:
    
            if var == variable:
                old_value = value

                # Perform casting 
                if new_type == "NUMBR":
                    try:
                        new_value = int(old_value)  
                    except ValueError:
                        print(f"Cannot cast value '{old_value}' to NUMBR")
                elif new_type == "NUMBAR":
                    try:
                        new_value = float(old_value) 
                    except ValueError:
                        print(f"Cannot cast value '{old_value}' to NUMBAR")
                elif new_type == "YARN":
                    new_value = str(old_value)  
                elif new_type == "TROOF":
                    if isinstance(old_value, (int, float)):
                        if old_value == 0:
                            new_value = False  
                        else:
                            new_value = True 
                    elif isinstance(old_value, str):
                        old_value = old_value.strip().lower()  
                        if old_value in ['true', '1']:
                            new_value = True  
                        else:
                            new_value = False  
                else:
                    print(f"Unsupported type: {new_type}")
                return new_value
        print(f"Variable '{variable}' not found in symbol table.")

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
