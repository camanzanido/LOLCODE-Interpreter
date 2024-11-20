from src.keyword_classifiers import *

def syntax_analyzer(lexemes):
    # lexemes = [('flag', 'Variable Identifier'), ('ITZ', 'Variable Declaration'), ('WIN', 'TROOF Literal'), ....]

    # Filtered lexemes
    array_lexemes = comments_remover(lexemes)
    symbol_table = [["IT", 0]]
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
            elif lexeme_type == ID_FUNC:
                parse_function()
            elif lexeme == "I IZ":
                parse_function_call()
            elif lexeme_type == KW_COMPARISON:
                parse_comparison_operations()
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
            return value
        elif lexeme == "GIMMEH":
            parse_input()
        elif lexeme == "VISIBLE":
            parse_output()
        elif lexeme_type == KW_CONCATENATE:
            value = parse_concatenation()
            return value
        elif lexeme_type == KW_BOOLEAN:
            value = parse_boolean_operations()
            it = value
            print(f"boolean expr: {it}")
            return value
        elif lexeme_type == KW_COMPARISON:
            value = parse_comparison_operations()
            it = value
            print(f"comparison: {it}")
            return value
        elif lexeme == "O RLY?":
            parse_if_else_statements()
        elif lexeme_type == KW_OUTPUT:
            parse_output()
        elif lexeme == "I IZ":
            parse_function_call()
        elif lexeme == "IT":
            return
        elif lexeme == "AN":    
            consume("AN")
        elif lexeme == "OMG":
            consume("OMG")
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
                print("Error: Hindi ko pa alam")
    # ===================================================================== BOOLEAN OPERATIONS =====================================================================
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
                    return operand1 and operand2
                print("No second Operand")
            elif operator == "EITHER OF":
                if operand2 is not None:
                    return operand1 or operand2
                print("No second Operand")

            elif operator == "WON OF":
                if operand2 is not None:
                    return bool(operand1) ^ bool(operand2)
                print("No second Operand")

            elif operator == "NOT":
                return not operand1
            
            # since ALL OF & ANY OF cannot be nested, separate to other boolean operations that can be nested
            elif operator in ["ALL OF", "ANY OF"]:
                operands = []  
                print(f"Parsing {operator}")

                # Collect all operands until "MKAY"
                while index < lexemes_length and array_lexemes[index][0] != "MKAY":
                 
                    if array_lexemes[index][0] == "AN":
                        consume("AN")
                    
                    if array_lexemes[index][0] in ["ALL OF", "ANY OF"]:
                        print(f"Error: Nested {array_lexemes[index][0]} is not allowed.")
                        return
                    
                    operand_value = operand()
                    if operand_value is not None:
                        operands.append(operand_value)

              
                if index < lexemes_length and array_lexemes[index][0] == "MKAY":
                    consume("MKAY")  

                # Perform the operation
                if operator == "ALL OF":
                    return all(operands)
                elif operator == "ANY OF":
                    return any(operands)
            else:
                print(f"Unknown arithmetic operation: {operator}")

    # ===================================================================== COMPARISON OPERATIONS =====================================================================
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
                return operand1 == operand2
            elif operator ==  "DIFFRINT":   # x != y
                return operand1 != operand2
            elif operator == "BIGGR OF":  
                return max(operand1, operand2)
            elif operator == "SMALLR OF": 
                return min(operand1, operand2)
            else:
                print(f"Unknown boolean operation: {operator}")

    # ===================================================================== CONTROL FLOW =====================================================================
    #<if-then> ::= <expr><linebreak>O RLY?<linebreak>YA RLY<linebreak> <code_block> <linebreak> <else-if>* <linebreak> NO WAI <linebreak> <code_block> <linebreak>OIC
    def parse_if_else_statements():  # Note: NO MEBBE YET
            nonlocal index, it
            lexeme = array_lexemes[index][0]
            # condition = []          
            # condition.append(it) 
            if lexeme == "O RLY?":
                consume(lexeme)
                # cond = condition[0]
                # while index < lexemes_length and array_lexemes[index][0] != "OIC" or index < lexemes_length and array_lexemes[index][0] != "NO WAI" :
                if array_lexemes[index][0] == "YA RLY":
                    consume("YA RLY")
                    while (index < lexemes_length and array_lexemes[index][0] not in ["NO WAI", "OIC"]):
                        parse_expression()
                
                if array_lexemes[index][0] == "NO WAI":
                    consume("NO WAI")
                    while (index < lexemes_length and array_lexemes[index][0] != "OIC"):
                        parse_expression()
                    
                # Delimter
                if array_lexemes[index][0] == "OIC":
                    consume("OIC")
 
     # <switch-case> ::= WTF? <linebreak> <case>+ <linebreak> <default_case>?  OIC
    def parse_switch_case_statement():
        nonlocal index, it
        lexeme = array_lexemes[index][0]
        condition = it
        matched = False

        if lexeme == "WTF?":
            consume(lexeme)
            while index < lexemes_length: 
                curr_lexeme = array_lexemes[index][0]
         
                if curr_lexeme == "OIC":
                    consume("OIC")
                    break
    
                elif curr_lexeme == "OMG":
                    consume("OMG")
                    case_value = array_lexemes[index][0]
                    
                    consume(case_value) 
                    if not matched and condition == int(case_value):  
                        matched = True
                        while (index < lexemes_length and array_lexemes[index][0] not in ["GTFO", "OIC"]):
                            parse_expression() 
                    else:  
                        while (index < lexemes_length and array_lexemes[index][0] not in ["GTFO", "OIC"]):
                            consume(array_lexemes[index][0])

                    if index < lexemes_length and array_lexemes[index][0] == "GTFO":
                        consume("GTFO")

                elif curr_lexeme == "OMGWTF":
                    consume("OMGWTF")
                    if not matched: 
                        matched = True
                        while index < lexemes_length and array_lexemes[index][0] not in ["GTFO", "OIC"]:
                            parse_expression()
                    else:  
                        while index < lexemes_length and array_lexemes[index][0] not in ["GTFO", "OIC"]:
                            consume(array_lexemes[index][0])

                    if index < lexemes_length and array_lexemes[index][0] == "GTFO":
                        consume("GTFO")

                else:
                    print(f"Unexpected token {curr_lexeme} in WTF? statement.")

    # <loop> ::= IM IN YR <label> operation YR varident (<til_op> | <wile_op>) <linebreak> <code_block><linebreak> IM OUTTA YR <label>
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

            comp_index = index # will hold the starting index of the comparison
            continue_index = index  # will hold the index b4 comparison
            
            while True:
                index = comp_index
                condition_met = parse_comparison_operations()

                if (condition_type == "WILE" and condition_met) or (condition_type == "TIL" and not condition_met):
                    var_value = get_variable_value(varident)
                    parse_block()
                    if operation == "NERFIN":
                        var_value -= 1
                    else:
                        var_value += 1
                    update_variable_value(varident, var_value)
                    continue_index = index
                else:
                    index= continue_index
                    break


            if array_lexemes[index][0] == "IM OUTTA YR":
                consume("IM OUTTA YR")
                consume(label)
            
    # ===================================================================== FUNCTIONS =====================================================================
    # <function> ::= HOW IZ I func_ident <parameters> <function_body> <return_statement> IF U SAY SO
    def parse_function():
        nonlocal index
        lexeme = array_lexemes[index][0]
        
        # HOW IZ I
        if lexeme == "HOW IZ I":  
            consume(lexeme)

            # FUNCTION NAME
            if index < lexemes_length and array_lexemes[index][1] == ID_VAR:
                function_name = array_lexemes[index][0]
                consume(array_lexemes[index][0])  
                if index < lexemes_length and array_lexemes[index][0] == "YR":
                    consume(array_lexemes[index][0])  
                    # <parameters> 
                    function_args = []
                    while index < lexemes_length and array_lexemes[index][1] == ID_VAR:
                        function_args.append(array_lexemes[index][0])
                        consume(array_lexemes[index][0])  
                        if index < lexemes_length and array_lexemes[index][0] == "AN":
                            consume(array_lexemes[index][0])
                            if index < lexemes_length and array_lexemes[index][0] == "YR":
                                consume(array_lexemes[index][0])
                        else:
                            break
            # <function_body>
            parse_function_body()
            # <return_statement>
            parse_function_return()
            # IF U SAY SO
            if index < lexemes_length and array_lexemes[index][0] == "IF U SAY SO":
                consume(array_lexemes[index][0])

     # <function_body>
    def parse_function_body():
        while index < lexemes_length and array_lexemes[index][0] not in ["FOUND YR", "IF U SAY SO", "GTFO"]:
            parse_expression()
    # <return_statement>
    def parse_function_return():
        if index < lexemes_length and array_lexemes[index][0] == "FOUND YR":
            consume(array_lexemes[index][0])  
            parse_expression()  
        if index < lexemes_length and array_lexemes[index][0] == "GTFO":
            consume(array_lexemes[index][0])
            while index < lexemes_length and array_lexemes[index][0] != "IF U SAY SO":
                parse_expression()

    # <function_call>
    def parse_function_call():
        nonlocal index
        lexeme = array_lexemes[index][0]
        # I IZ
        if lexeme == "I IZ":  
            consume(lexeme)
            # Function name
            if index < lexemes_length and array_lexemes[index][1] == ID_VAR:
                function_name = array_lexemes[index][0]
                consume(array_lexemes[index][0])  
                # YR
                if index < lexemes_length and array_lexemes[index][0] == "YR":
                    consume(array_lexemes[index][0])  
                    # Parameter 1
                    parse_expression()
                    # the rest of the parameters
                    while index < lexemes_length and array_lexemes[index][0] == "AN":
                        consume(array_lexemes[index][0])  
                        if index < lexemes_length and array_lexemes[index][0] == "YR":
                            consume(array_lexemes[index][0])
                            parse_expression()
                        else:
                            break

    # ------------------- HELPER FUNCTIONS -------------------
    # Function for returning symbol table value
    def get_variable_value(var_name):
        for var, value in symbol_table:
            if var == var_name:
                return value
        return 0
    
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
