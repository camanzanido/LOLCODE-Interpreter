from src.keyword_classifiers import *
import copy

# lexemes = [('flag', 'Variable Identifier'), ('ITZ', 'Variable Declaration'), ('WIN', 'TROOF Literal'), ....]

# Filtered lexemes
array_lexemes = []

# Initial variables
index = 0
it = 0
lexemes_length = 0
status = SYNTAX

# Arrays
symbol_table = [["IT", 1]]
functions_array = []
output_array = []
errors = []


def syntax_analyzer(lexemes):
    global index
    global array_lexemes
    global symbol_table
    global output_array
    global lexemes_length
    # Remove comments from the lexemes
    array_lexemes = comments_remover(lexemes)
    lexemes_length = len(array_lexemes)
    # Start parsing the program
    parse_program()
    print("========== Syntax analysis successful! ==========")
    display_symbol_table(symbol_table)
    display_output(output_array)
    return symbol_table, output_array

# Consume function: Proceeds to the next token
def consume(expected_token):
    global index
    global array_lexemes
    global symbol_table
    global output_array
    global lexemes_length
    
    if index < lexemes_length and array_lexemes[index][0] == expected_token:
        # Increment index/position: Next token
        index += 1
    else:
        add_error(f"Expected '{expected_token}', but got '{array_lexemes[index][0]}'")
        print(f"Expected '{expected_token}', but got '{array_lexemes[index][0]}'")

# <program> ::= HAI <block> KTHXBYE
def parse_program():
    global index
    global array_lexemes
    global symbol_table
    global output_array
    global lexemes_length
    # HAI
    if index < lexemes_length and array_lexemes[index][0] == "HAI":
        consume("HAI")
        # CODE BLOCK
        parse_block()
        if index < lexemes_length and array_lexemes[index][0] == "KTHXBYE":
            # KTHXBYE
            consume("KTHXBYE")
            if index < lexemes_length and array_lexemes[index+1][0]:
                print("NOTHING SHOULD BE AFTER KTHXBYE")
                exit()
        else:
            add_error("Expected 'KTHXBYE' to end the program")
    else:
        add_error("Expected 'HAI' at the start of the program")

# <block> ::= <output> | <variable_declarations> | <input> | <variable_assignment>
#            | <conditional_statement> | <switch_statement> | <function_statement>
#            | <function_call> | <comparison_statement>
def parse_block():
    global index
    global array_lexemes
    global symbol_table
    global output_array
    global lexemes_length
    global status

    # Parse line by line (by its first keyword)
    while index < lexemes_length:
        lexeme = array_lexemes[index][0]
        lexeme_type = array_lexemes[index][1]
        # <output>
        if lexeme == "VISIBLE":
            parse_output()
        # <variable_declarations> 
        elif lexeme == "WAZZUP":
            parse_variable_declarations()
        # <input>    
        elif lexeme == "GIMMEH":
            status = SEMANTICS
            parse_input()
            status = SYNTAX
        # <variable_assignment>
        elif lexeme_type == ID_VAR:
            parse_variable_reassignment()
        # <conditional_statement>
        elif lexeme == "O RLY?":
            parse_if_else_statements()
        # <switch_statement>
        elif lexeme == "WTF?":
            parse_switch_case_statement()
        #  <function_statement>
        elif lexeme == "IM IN YR":
            parse_loop()
        elif lexeme_type == ID_FUNC:
            parse_function()
        # <function_call> 
        elif lexeme == "I IZ":
            parse_function_call()
        # <comparison_statement>
        elif lexeme_type == KW_COMPARISON:
            value = parse_comparison_operations()
            update_IT(value)
        # Delimiter
        elif lexeme == "KTHXBYE":
            break
        else:
            add_error(f"Unexpected token '{lexeme}'")
            break
        
# ===================================================================== INPUT/OUTPUT =====================================================================


# <input> ::= GIMMEH <var_ident> 
def parse_input():
    global index
    global array_lexemes
    global symbol_table
    global output_array
    global lexemes_length
    global status

    lexeme = array_lexemes[index][0]
    # GIMMEH
    if lexeme == "GIMMEH":
        consume(lexeme)
        # Variable Identifier
        if index < lexemes_length and array_lexemes[index][1] == ID_VAR:
            variable = array_lexemes[index][0]
            consume(array_lexemes[index][0])
            if status == SEMANTICS:
                # Ask for an input in the terminal
                value = input(f"{variable}: ")
                parsed_value = parse_value(value)
                update_IT(parsed_value)
                # Update the symbol table
                update_variable_value(variable, parsed_value)
        else:
            add_error("Expected 'GIMMEH' to read input")

# <output> ::= VISIBLE <expression> [AN <expression>...]
def parse_output():
    global index
    global array_lexemes
    global symbol_table
    global output_array
    global lexemes_length
    lexeme = array_lexemes[index][0]
    # VISIBLE
    if lexeme == "VISIBLE":
        consume(lexeme)
        string_to_print = ""
        
        # Parse the expression until there is AN
        while index < lexemes_length:
            string_to_print += str(parse_expression())
            # AN
            if index < lexemes_length and array_lexemes[index][0] == "AN":
                consume(array_lexemes[index][0])
            else:
                # Append the string to the output array
                output_array.append(string_to_print)
                update_IT(string_to_print)
                break    

# ===================================================================== EXPRESSIONS =====================================================================
# <expression> ::= <variable> | <literals> | <arithmetic_op> | <input> | <output> | <smoosh> | <boolean_op>
#                  <comparison_op> | <conditional_statement> | <function_call>
def parse_expression():    
    global index
    global array_lexemes
    global symbol_table
    global output_array
    global lexemes_length
    lexeme = array_lexemes[index][0]
    lexeme_type = array_lexemes[index][1]
    
    # <variable> | <literals>
    if lexeme_type in [LIT_YARN, LIT_NUMBR, LIT_NUMBAR, LIT_TROOF, ID_VAR]:
        consume(lexeme)
        # Typecasting the lexemes
        if lexeme_type == LIT_NUMBAR:
            lexeme = float(lexeme)
        elif lexeme_type == LIT_NUMBR:
            lexeme = int(lexeme)
        elif lexeme_type == ID_VAR:
            lexeme = get_variable_value(lexeme)
        update_IT(lexeme)
        return lexeme
    # <arithmetic_op>
    elif lexeme_type == KW_ARITHMETIC:
        value = parse_arithmethic_operations()
        update_IT(value)
        return value
    # <input>
    elif lexeme == "GIMMEH":
        parse_input()
    # <output>
    elif lexeme == "VISIBLE":
        parse_output()
    # <smoosh>
    elif lexeme_type == KW_CONCATENATE:
        value = parse_concatenation()
        update_IT(value)
        return value
    # <boolean_operation>
    elif lexeme_type == KW_BOOLEAN:
        value = parse_boolean_operations()
        update_IT(value)
        return value
    # <comparison_operation>
    elif lexeme_type == KW_COMPARISON:
        value = parse_comparison_operations()
        update_IT(value)
        return value
    # <conditional_statement>
    elif lexeme == "O RLY?":
        parse_if_else_statements()
    # <function_call>
    elif lexeme == "I IZ":
        value = parse_function_call()
        update_IT(value)
        return value
    elif lexeme == "IT":
        consume(lexeme)
        return symbol_table[0][1]
    elif lexeme == "AN":    
        consume("AN")
    elif lexeme == "OMG":
        consume("OMG")
    elif lexeme == "KTHXBYE":
        return
    else:
        add_error("Invalid expression")

# ===================================================================== ARITHMETHIC OPERATIONS =====================================================================
# <arithmethic> ::= <operations> <literal|var_indent|arithmethic> AN <literal|var_indent|arithmethic>
def parse_arithmethic_operations():
    global index
    global array_lexemes
    global symbol_table
    global output_array
    global lexemes_length
    lexeme = array_lexemes[index][0]
    lexeme_type = array_lexemes[index][1]
    
    # Operation
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
            add_error("Unsupported operation")

# <literal|var_indent|arithmethic>
def operand():
    global index
    global array_lexemes
    global symbol_table
    global output_array
    global lexemes_length
    lexeme = array_lexemes[index][0]
    lexeme_type = array_lexemes[index][1]
    # Return the literal value or variable value
    if lexeme_type == ID_VAR:
        consume(lexeme)
        # Retrieve the variable's value from the symbol table
        value = get_variable_value(lexeme)
        return parse_value(value)

    # Perform typecasting
    elif lexeme_type == LIT_NUMBR:
        consume(lexeme)
        return int(lexeme)

    elif lexeme_type == LIT_NUMBAR:
        consume(lexeme)
        return float(lexeme)
    
    # Evaluate TROOF
    elif lexeme_type == LIT_TROOF:
        consume(lexeme)
        if lexeme == "WIN":
            return 1
        else:
            return 0
    # YARN
    elif lexeme_type == LIT_YARN:
        consume(lexeme)
        return parse_value(lexeme)
    
    elif lexeme == "NOOB":
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
        exit()

# ===================================================================== SMOOSH KEYWORD =====================================================================
# <concatenate> ::= SMOOSH <expr> AN [<expr> | (<expr> AN)*]
def parse_concatenation():
    global index
    global array_lexemes
    global symbol_table
    global output_array
    global lexemes_length
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
            # AN
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
    global index
    global array_lexemes
    global symbol_table
    global output_array
    global lexemes_length
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
        elif index < lexemes_length and array_lexemes[index][0] in ["WTF?", "O RLY?"]:
            return
        else:
            print("Error: Invalid variable reassignment syntax.")

# <typecasting> ::= MAEK var_ident literal | IS NOW A literal
def parse_type_casting(variable):
    global index
    global array_lexemes
    global symbol_table
    global output_array
    global lexemes_length
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
    global index
    global array_lexemes
    global symbol_table
    global output_array
    global lexemes_length
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
    global index
    global array_lexemes
    global symbol_table
    global output_array
    global lexemes_length
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
                print("hello")
                consume("ITZ")
                # expr
                symbol_table.append([variable, parse_expression()])
            else:
                symbol_table.append([variable, "NOOB"])
        else:
            print(f"Error: Unexpected token '{array_lexemes[index][0]}' found while parsing variable declaration.")

# ===================================================================== BOOLEAN OPERATIONS =====================================================================
# <boolean_op> :: = BOTH OF <expr> AN <expr> | EITHER OF <expr> AN <expr> | WON OF <expr> AN <expr> | NOT <expr> | ALL OF <expr> MKAY | ANY OF <expr> MKAY
def parse_boolean_operations():
    global index
    global array_lexemes
    global symbol_table
    global output_array
    global lexemes_length
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
    global index
    global array_lexemes
    global symbol_table
    global output_array
    global lexemes_length
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
    global index
    global array_lexemes
    global symbol_table
    global output_array
    global lexemes_length
    global status
    global output_array
    global symbol_table
    
    # store initial values
    init_output_array = copy.deepcopy(output_array)
    init_symbol_table = copy.deepcopy(symbol_table)

    lexeme = array_lexemes[index][0]
    # condition = []          
    # condition.append(it) 
    if lexeme == "O RLY?":
        no_wai_line_number = -1
        init_index = index
        consume(lexeme)
        # cond = condition[0]
        # while index < lexemes_length and array_lexemes[index][0] != "OIC" or index < lexemes_length and array_lexemes[index][0] != "NO WAI" :
        if array_lexemes[index][0] == "YA RLY":
            consume("YA RLY")
            while (index < lexemes_length and array_lexemes[index][0] not in ["NO WAI", "OIC"]):
                parse_expression()
        
        if array_lexemes[index][0] == "NO WAI":
            no_wai_line_number = array_lexemes[index][2]
            consume("NO WAI")
            while (index < lexemes_length and array_lexemes[index][0] != "OIC"):
                parse_expression()
            
        # Delimter
        if array_lexemes[index][0] == "OIC":
            consume("OIC")

        # reset these after parsing the function
        output_array = copy.deepcopy(init_output_array)
        symbol_table = copy.deepcopy(init_symbol_table)

        last_index = index
        status = SEMANTICS
        sem_execute_if_else_statement(init_index, no_wai_line_number)
        status = SYNTAX
        index = last_index

# <switch-case> ::= WTF? <linebreak> <case>+ <linebreak> <default_case>?  OIC
def parse_switch_case_statement():
    global index
    global array_lexemes
    global symbol_table
    global output_array
    global lexemes_length
    global status

            
        # store initial values
    init_output_array = copy.deepcopy(output_array)
    init_symbol_table = copy.deepcopy(symbol_table)
    lexeme = array_lexemes[index][0]
    semantic_indx  = index
    if lexeme == "WTF?":
        consume(lexeme)
        while index < lexemes_length: 
            curr_lexeme = array_lexemes[index][0]
        
            if curr_lexeme == "OIC":
                consume("OIC")
                break

            elif curr_lexeme == "OMG":
                # ====================== NEW ==================
                # OMG KEYWORD
                consume("OMG")
                # Case value
                if index < lexemes_length and array_lexemes[index][1] in [LIT_YARN, LIT_NUMBR, LIT_NUMBAR, LIT_TROOF, ID_VAR]:
                    consume(array_lexemes[index][0])
                    # Expressions
                    while (index < lexemes_length and array_lexemes[index][0] not in ["GTFO", "OIC", "OMG", "OMGWTF"]):
                        parse_expression() 
                    # GTFO
                    if index < lexemes_length and array_lexemes[index][0] == "GTFO":
                        consume("GTFO")

                # ================ ORIGINAL =============
                    
                # if not matched and condition == int(case_value):  
                #     matched = True
                #     while (index < lexemes_length and array_lexemes[index][0] not in ["GTFO", "OIC", ]):
                #         parse_expression() 
                # else:  
                #     while (index < lexemes_length and array_lexemes[index][0] not in ["GTFO", "OIC"]):
                #         print(array_lexemes[index][0]) #print ko to
                #         consume(array_lexemes[index][0])


            elif curr_lexeme == "OMGWTF":
                consume("OMGWTF")
                # ================ ORIGINAL =============
                # if not matched: 
                #     matched = True
                #     while index < lexemes_length and array_lexemes[index][0] not in ["GTFO", "OIC"]:
                #         parse_expression()
                # else:  
                #     while index < lexemes_length and array_lexemes[index][0] not in ["GTFO", "OIC"]:
                #         consume(array_lexemes[index][0])

                # ====================== NEW ==================
                while index < lexemes_length and array_lexemes[index][0] not in ["GTFO", "OIC"]:
                    parse_expression()
                if index < lexemes_length and array_lexemes[index][0] == "GTFO":
                    consume("GTFO")
                

            else:
                print(f"Unexpected token {curr_lexeme} in WTF? statement.")
                break

        output_array = copy.deepcopy(init_output_array)
        symbol_table = copy.deepcopy(init_symbol_table)
        status = SEMANTICS
        execute_switch(semantic_indx)
        status = SYNTAX

def execute_switch(semantic_index):
    global index
    global array_lexemes
    global symbol_table
    global output_array
    global it 

    condition = it
    matched = False

    index_backup = index  
    index = semantic_index

    if isinstance(array_lexemes[index-1][0], str):  # check if the lexeme is a string(variable),
        condition = get_variable_value(array_lexemes[index-1][0]) # get its value

    consume("WTF?")  
    while index < lexemes_length : 
        curr_lexeme = array_lexemes[index][0]
        print(f"current lexeme: {curr_lexeme}")
        if curr_lexeme == "OIC":
            consume("OIC")
            break

        elif curr_lexeme == "OMG":
            consume("OMG")
            
            if index < lexemes_length and array_lexemes[index][1] in [LIT_YARN, LIT_NUMBR, LIT_NUMBAR, LIT_TROOF, ID_VAR]:
                case_value = array_lexemes[index][0]
                if condition == int(case_value) and not matched:      
                    print("matched")
                    matched = True
                    consume(case_value)
                    print(case_value)
                    
                    # execute the block
                    while (index < lexemes_length and array_lexemes[index][0] not in ["GTFO", "OIC", "OMG", "OMGWTF"]):
                        parse_expression() 
                    if index < lexemes_length and array_lexemes[index][0] == "GTFO":
                        consume("GTFO")
                    break
                else:
                    consume(case_value)
                    while (index < lexemes_length and array_lexemes[index][0] not in ["GTFO", "OIC", "OMG", "OMGWTF"]):
                        index += 1
                    
                    if index < lexemes_length and array_lexemes[index][0] == "GTFO":
                        consume("GTFO")

        elif curr_lexeme == "OMGWTF": # default case
            if not matched:
                consume("OMGWTF")
                while index < lexemes_length and array_lexemes[index][0] not in ["GTFO", "OIC"]:
                    parse_expression()
                
                if index < lexemes_length and array_lexemes[index][0] == "GTFO":
                    consume("GTFO")
                break

    # Restore the index
    index = index_backup

    

# <loop> ::= IM IN YR <label> operation YR varident (<til_op> | <wile_op>) <linebreak> <code_block><linebreak> IM OUTTA YR <label>
def parse_loop():
    global index
    global array_lexemes
    global symbol_table
    global output_array
    global lexemes_length

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
    global output_array
    global symbol_table
    
    # store initial values
    init_output_array = copy.deepcopy(output_array)
    init_symbol_table = copy.deepcopy(symbol_table)

    global index
    global array_lexemes
    global lexemes_length

    lexeme = array_lexemes[index][0]

    # HOW IZ I
    if lexeme == "HOW IZ I": 
        function_index = index 
        consume(lexeme)
        # FUNCTION NAME
        if index < lexemes_length and array_lexemes[index][1] == ID_VAR:
            function_name = array_lexemes[index][0]
            # Checks if the function name is existing
            if check_function_name(function_name):
                consume(array_lexemes[index][0])  
                # YR
                if index < lexemes_length and array_lexemes[index][0] == "YR":
                    consume(array_lexemes[index][0])  
                    # <parameters> 
                    function_args = []
                    while index < lexemes_length and array_lexemes[index][1] == ID_VAR:
                        # Append parameter
                        function_args.append(array_lexemes[index][0])
                        consume(array_lexemes[index][0])  
                        if index < lexemes_length and array_lexemes[index][0] == "AN":
                            consume(array_lexemes[index][0])
                            if index < lexemes_length and array_lexemes[index][0] == "YR":
                                consume(array_lexemes[index][0])
                        else:
                            functions_array.append([function_name, function_index, function_args])
                            break
                # <function_body>
                parse_function_body()
                # <return_statement>
                parse_function_return()
                # IF U SAY SO
                if index < lexemes_length and array_lexemes[index][0] == "IF U SAY SO":
                    consume(array_lexemes[index][0])
        else:
            print("Error, function name is missing")

    # reset these after parsing the function
    output_array = copy.deepcopy(init_output_array)
    symbol_table = copy.deepcopy(init_symbol_table)


    # <function_body>
def parse_function_body():
    while index < lexemes_length and array_lexemes[index][0] not in ["FOUND YR", "IF U SAY SO", "GTFO"]:
        parse_expression()
        
# <return_statement>
def parse_function_return():
    if index < lexemes_length and array_lexemes[index][0] == "FOUND YR":
        consume(array_lexemes[index][0])  
        # return value
        return parse_expression()  
    if index < lexemes_length and array_lexemes[index][0] == "GTFO":
        consume(array_lexemes[index][0])
        # return NOob
        return "NOOB"

# <function_call>
def parse_function_call():
    global symbol_table
    global index
    global array_lexemes
    global symbol_table
    global output_array
    global lexemes_length
    global status
    lexeme = array_lexemes[index][0]
    return_value = "NOOB"
    
    # Initial symbol table
    copy_symbol_table = copy.deepcopy(symbol_table[1:])

    # I IZ
    if lexeme == "I IZ":  
        consume(lexeme)
        # Function name
        if index < lexemes_length and array_lexemes[index][1] == ID_VAR:
            function_name = array_lexemes[index][0]
            func_index = find_function_index(function_name)

            # Checks if function name exists
            if func_index != -1:
                function_index = functions_array[func_index][1]
                func_param_length = len(functions_array[func_index][2])
                func_args_length = 0
                consume(array_lexemes[index][0])  
                # YR
                if index < lexemes_length and array_lexemes[index][0] == "YR":
                    consume(array_lexemes[index][0]) 
                    if index < lexemes_length and array_lexemes[index][1]: 
                        # Parameter 1
                        variable = functions_array[func_index][2][func_args_length]
                        symbol_table.append([variable, parse_expression()])
                        func_args_length += 1
                        # the rest of the parameters
                        while index < lexemes_length and array_lexemes[index][0] == "AN":
                            consume(array_lexemes[index][0])  
                            if index < lexemes_length and array_lexemes[index][0] == "YR":
                                consume(array_lexemes[index][0])
                                if index < lexemes_length and array_lexemes[index][1]:
                                    if func_args_length < func_param_length:
                                        variable = functions_array[func_index][2][func_args_length]
                                        symbol_table.append([variable, parse_expression()])
                                        func_args_length += 1
                                    else:
                                        print("Error: More arguments than function parameters")
                                else:
                                    print("Error: Missing parameter after YR")
                                    return()
                            else:
                                print("Error: Missing YR after AN")
                                return()
                        
                        # Execute function if equal number of parameters and arguments
                        if func_param_length == func_args_length:
                            status = SEMANTICS
                            return_value = sem_execute_function(function_index)
                            status = SYNTAX
                        elif func_args_length > func_param_length:
                            print("Error: More arguments than function parameters")
                            exit()
                        else:
                            print("Error: Missing arguments")
                            exit()
            else:
                print(f"Error: Function '{function_name}' not found or declared")
                exit()
    
    # Reset 
    symbol_table[1:] = copy.deepcopy(copy_symbol_table)
    return return_value

# ======================================================== SEMANTICS ANALYSIS FUNCTIONS ======================================================== 

# Call and execute the function
def sem_execute_function(temp_index):
    global index
    global array_lexemes
    global symbol_table
    global output_array
    global lexemes_length
    # Store initial index
    init_index = index
    # Jump to the function
    index = temp_index
    lexeme = array_lexemes[index][0]
    # HOW IZ I
    if lexeme == "HOW IZ I": 
        consume(lexeme)
        # FUNCTION NAME
        if index < lexemes_length and array_lexemes[index][1] == ID_VAR:
            consume(array_lexemes[index][0])  
            if index < lexemes_length and array_lexemes[index][0] == "YR":
                consume(array_lexemes[index][0])  
                # <parameters> 
                while index < lexemes_length and array_lexemes[index][1] == ID_VAR:
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
        else:
            print("Error, function name is missing")

    # Jump back
    index = init_index

# Execute if-else statement
def sem_execute_if_else_statement(temp_index, no_wai_line_number):
    global index
    global array_lexemes
    global symbol_table
    global output_array
    global lexemes_length
    # Index of the O RLY?
    index = temp_index

    if array_lexemes[index][0] == "O RLY?":
        # Extracts the line number
        line_number = array_lexemes[index][2]
        # Find the index of the expression (linenumber-1)
        index = find_expression(line_number-1)
        # Parse that expression
        troof_result = parse_expression()
        # If true: Perform YA RLY
        if troof_result:
            while array_lexemes[index][0] != "YA RLY":
                index +=1
            consume("YA RLY")
            while array_lexemes[index][0] not in ["NO WAI", "OIC"]:
                parse_expression()
        # If false: Perform NO WAI if existing
        else:
            if no_wai_line_number != -1:
                index = find_expression(no_wai_line_number)
                consume(array_lexemes[index][0])
                while array_lexemes[index][0] != "OIC":
                    parse_expression()
        
# ------------------- HELPER FUNCTIONS -------------------
# Function for returning symbol table value
def get_variable_value(var_name):
    global symbol_table

    for var, value in reversed(symbol_table):
        if var == var_name:
            return value
    return 0

def end_of_code_checker(lexemes):
    for i in range(lexemes):
        if lexemes[i][0] == "KTHXBYE":
            break
    if i >= len(lexemes):
        return 0
    else:
        return 1
# Parser
def parse_value(value):
    if value == "NOOB":
        return 0
    try:
        return int(value) 
    except ValueError:
        pass 
    try:
        return float(value)  
    except ValueError:
        pass  
    try:
        # Remove quotes from YARN literals
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
    except ValueError:
        pass      
    return value

# Function for updating the symbol table
def update_variable_value(variable, parsed_value):
    global symbol_table
    for i in range(len(symbol_table)):
        if symbol_table[i][0] == variable:
            symbol_table[i][1] = parsed_value
            return
    symbol_table.append([variable, parsed_value])

def update_IT(value):
    global symbol_table
    symbol_table[0][1] = value

# Recast function
def recast_variable_value(variable, new_type):
    global symbol_table

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

# Helper to add error messages
def add_error(message):
    global lexemes_length

    if index < lexemes_length:
        lexeme = array_lexemes[index]
        errors.append(f"Error at token '{lexeme[0]}': {message}")
    else:
        errors.append(f"Error at end of input: {message}")

# Checks if function name exists
def check_function_name(function_name):
    global functions_array
    if function_name in functions_array:
        print(f"Error: The function '{function_name}' already exists.")
        return False
    else:
        return True

# Function for finding the location of a function
def find_function_index(function_name):
    global functions_array
    for i in range(len(functions_array)):
        if functions_array[i][0] == function_name:
            return i
    return -1  

# Function for finding the expression before an if-else
def find_expression(line_number):
    global array_lexemes

    for i in range(len(array_lexemes)):
        if array_lexemes[i][2] == line_number:
            return i
    return -1  

def comments_remover(array_lexemes):
    filtered_lexemes = []

    for tokens in array_lexemes:
        type_of_token = tokens[1]

        if type_of_token not in [KW_COMMENT_START, COMMENT, KW_COMMENT_DELIM]:
            # If the condition is met, add the item to the filtered_data list
            filtered_lexemes.append(tokens)

    # Return or print the filtered data list
    return filtered_lexemes

def display_symbol_table(symbol_table):

    print("\tSymbol Table")
    print("-" * 30)
    
    print(f"{'Lexeme':<15}{'Type':<15}")
    print("-" * 30)
    
    for lexeme, type_ in symbol_table:
        print(f"{lexeme:<15}{type_:<15}")
    
    print("=" * 30)

def display_output(output_array):

    print(" " * 12, end="")
    print("Output")
    print("-" * 30)
    
    for output in output_array:
        print(output)
    print("=" * 30)

