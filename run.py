global_symbol_table = SymbolTable()
global_symbol_table.set("None", Number(0)) 


def run(fn, text):
    print("running")
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    
    for item in tokens:
        if isinstance(item, list):
            tokens.remove(item)

    parser = Parser(tokens)
    #result, parseError = parser.parse()
    ast = parser.parse()
    print("ast: ", ast)

    #ast is a list of ParseResult instances
    for item in ast:
        print("type of ast node", type(item.node))
        if item.error: 
            return None, item.error
    

    # Run program
    result = []
    result_errors = []
    interpreter = Interpreter()
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    
    for item in ast:
        print("item type: ", type(item.node))
        # res returns an RTResult instance
        # RTResult can have a value and an error
        # item.node is the current node
        res = interpreter.visit(item.node, context)
        print("res type in run: ", type(res.value))
        print("res value: ", res.value)
        if isinstance(res.value, IfNode):
            print("FOUND ifnode")
            
        if isinstance(res.value, SaturnCallNode):
            print("FOUND SATURN CALL IN RES")
            print("value node: ", type(res.value.value_node))
            result.append(res.value.value_node)
            return result, result_errors
        if isinstance(res.value, OuterNode):
            print("found outer node")
            string_concat = ""
            for i in res.value.value_node:
                #result.append(i)   
                if res.error:
                    # lagay natin sa errors list
                    result_errors.append(res.error)
                    
                else:
                    # else ilagay sa result list
                    # remember yung result list is yung IDIDISPLAY SA USER
                    # we append the RTResult instance sa list
                    string_concat += str(i.value)
            result.append(String(string_concat))
        # * PLEASE READ
        # this is used to check if the current node is a saturn node
        # if hindi SaturnNode, wag ilagay sa list na ididisplay
        # used to control ano madidisplay sa user
        # for now, VarAssignNode palang iccheck  nya since yun palang nagagawa natin
        # here yung node ng ParseResult parin iccheck natin
        # pero an ilalagay natin sa list ay RTResult instance
        if isinstance(item.node, SaturnCallNode) or isinstance(item.node, OuterNode):
            print("saturn or outer found")
            if isinstance(item.node, OuterNode):
                print("found outer node")
                string_concat = ""
                for i in res.value:
                    #result.append(i)   
                    if res.error:
                        # lagay natin sa errors list
                        result_errors.append(res.error)
                        
                    else:
                        # else ilagay sa result list
                        # remember yung result list is yung IDIDISPLAY SA USER
                        # we append the RTResult instance sa list
                        string_concat += str(i.value)
                result.append(String(string_concat))
            else:
                if res.error:
                    # lagay natin sa errors list
                    result_errors.append(res.error)
                    
                else:
                    # else ilagay sa result list
                    # remember yung result list is yung IDIDISPLAY SA USER
                    # we append the RTResult instance sa list
                    result.append(res)
        else:
            if res.error:
                # if may error sa VarAssignNode, ilagay yung error sa list of errors
                result_errors.append(res.error)
            else:
                #if wala error sa VarAssignNode, skip lang natin
                # wag natin append sa result list para
                # di makita ng user yung var assignment natin
                # dat babalik lang pag nag call ng saturn yung user
                
                continue
            #if SaturnNode naman, check for errors parin
           
       
        
        
        print("item node: ",  item.node)
        print("item node: ",  item.error)
    
    print("result: ", result)

    # so this should return a value now
    
    # this returns a list of result, and list of result_errors
    context.symbol_table.symbols = {}
    return result, result_errors
    