
import subprocess
import semantic
# from semantic import ShipNode, CropAssignNode, CropInitNode, CropDecNode, CropAccessNode
# import subprocess
# import sys

import os

import sys
sys.path.append(r"C:\Users\sayso\Desktop\JunimoCode\built_in.py")


import keyword

def is_python_keyword(s):
    return s in keyword.kwlist

class LineTracker:
    def __init__(self) -> None:
        self.tracker_dict = {}
        self.current_line = 1
        # self.advance()
    def advance(self):
        self.current_line += 1
        
    def set(self, custom_pos):
        self.tracker_dict[self.current_line] = custom_pos
        
    #used to track the current_line number
line_tracker = LineTracker()
def read_value_nodes(node):
    pass
    #if CropAccessNode
    #if BinOpNode
    #if ValueNodes


def read_nodes(item, symbol_table, current_indention = 0):
    condition_to_list = []
    if isinstance(item, semantic.ShipNode):
        string = "" #dawnsantos
        print_items = []
        for output in item.body:

            if isinstance(output, semantic.CropAccessNode):
                print_items.append(f"{output.crop_name_tok.value}")
                
            elif isinstance(output, semantic.BinOpNode):
                # print("found bin op!")
                left = read_nodes(output.left_node, symbol_table)
                # print("left:", left)
                right = read_nodes(output.right_node, symbol_table)
                # print("right:", right)
                # print("get val right: ", type(right))
                # print("get val left: ", type(left))
                if output.op_tok.token == semantic.PLUS:
                    if isinstance(left, semantic.String):
                        # print("left is a string")
                        print_items.append(f"'{left.value}'+'{right.value}'")
                    else:
                        # print("not a string: ", type(left))
                        print_items.append(f"{left}+{right}")
                    # print("print_items: ", print_items)
                if output.op_tok.token == semantic.MINUS:
                    if isinstance(left, semantic.String):
                        print_items.append(f"'{left}'-'{right}'")
                    else:
                        print_items.append(f"{left}-{right}")
                    # print("prin/t_items: ", print_items) 
                if output.op_tok.token == semantic.MUL:
                    if isinstance(left, semantic.String):
                        print_items.append(f"'{left}'*'{right}'")
                    else:
                        print_items.append(f"{left}*{right}")
                    # print("print_items: ", print_items)
                if output.op_tok.token == semantic.DIV:
                    # print("found div")
                    if isinstance(left, semantic.String):
                        print_items.append(f"'{left}'/'{right}'")
                    else:
                        print_items.append(f"{left}/{right}")
                    # print("print_items: ", print_items)
                if output.op_tok.token == semantic.MODULUS:
                    if isinstance(left, semantic.String):
                        print_items.append(f"'{left}'+'{right}'")
                    else:
                        print_items.append(f"{left}+{right}")
                    # print("print_items: ", print_items)
            elif isinstance(output, semantic.CraftCallNode):
                params = []
                for call_param in output.parameters:
                    # Convert call_param.tok.value to string explicitly
                    if isinstance(call_param, semantic.ListCallNode):
                        index = read_nodes(call_param.index, {}, symbol_table)
                        param_value = f"{call_param.crop_name.crop_name_tok.value}[{index}]"
                        params.append(param_value)
                    elif isinstance(call_param, semantic.CropAccessNode):
                        
                        param_value = f"{call_param.crop_name_tok.value}"
                        params.append(param_value)
                    else:
                        param_value = str(call_param.tok.value)
                        params.append(param_value)
                parameters = ",".join(params)
                # print("parameters: ", parameters)
                # print_items.append(f"{output.identifier.value}({parameters})")
                if is_python_keyword(output.identifier.value):
                    print_items.append(f"{output.identifier.value}1({parameters})")
                    
                else:
                    print_items.append(f"{output.identifier.value}({parameters})")
                    
            elif isinstance(output, semantic.ListCallNode):
                if is_python_keyword(output.crop_name.crop_name_tok.value):
                    print_items.append(f"{output.crop_name.crop_name_tok.value}1[{output.index.value}]")
                    # print_items.append(f"{output.identifier.value}1({parameters})")
                    
                else:
                    if isinstance(output.index, semantic.BinOpNode):
                        index = read_nodes(output.index, {}, symbol_table)
                        print_items.append(f"{output.crop_name.crop_name_tok.value}[{index}]")
                    elif isinstance(output.index, semantic.CropAccessNode):
                        print_items.append(f"{output.crop_name.crop_name_tok.value}[{output.index.crop_name_tok.value}]")
                    elif isinstance(output.index, semantic.NumberNode):
                        print_items.append(f"{output.crop_name.crop_name_tok.value}[{output.index.tok.value}]")
                    else:
                    # print_items.append(f"{output.identifier.value}({parameters})")
                # index = read_nodes(output.crop_name)
                        print_items.append(f"{output.crop_name.crop_name_tok.value}[{output.index.value}]")
            else:  
                string += str(output.tok.value)
                print_items.append(f"{output.tok.value}")
                # print("string token position: ", output.tok.pos_start.ln+1)
                # python_code.append(f"{' ' * current_indentation}print('{string}')")
        x = ",".join(print_items)
        # print("x: ", x)
        # print("outer pos start: ", item.pos_start.ln+1)
        # print("outer current line: ", line_tracker.current_line)
        line_tracker.set(item.pos_start.ln+1)
        # print("line tracker outer: ",line_tracker.tracker_dict)
        line_tracker.advance()
        # print("current line outer: ", line_tracker.current_line)
        # print("line tracker outer: ", line_tracker.tracker_dict)
        return f"{' ' * current_indention}custom_print({x})"
    elif isinstance(item, semantic.NumberNode):
        # print("Numbernode: ", item.tok.value)
        value = item.tok.value
        return value
    elif isinstance(item, semantic.StringNode):
        # print("Numbernode: ", item.tok.value)
        value = item.tok.value
        return f"'{value}'"
    elif isinstance(item, semantic.BinOpNode):
        # print("found bin op!")
        
        # print("left node: ", item.left_node)
        left = read_nodes(item.left_node, symbol_table)
        # print("left:", type(left))
        right = read_nodes(item.right_node, symbol_table)
        # print("right:", type(right))
        if item.notted == False:
            
            if item.op_tok.token == semantic.PLUS:
                if isinstance(left, semantic.String):
                    
                    return semantic.String(left.value+right.value)
                else:
                    return f"({left}+{right})"
            if item.op_tok.token == semantic.MINUS:
                return f"({left}-{right})"
            if item.op_tok.token == semantic.MUL:
                return f"({left}*{right})"
            if item.op_tok.token == semantic.DIV:
                # print("found div bin op")
                return f"({left}/{right})"
            if item.op_tok.token == semantic.MODULUS:
                # print("modulus")
                return f"({left}%{right})"
            if item.op_tok.token == semantic.GREATER_THAN:
                return f"({left}>{right})"
            if item.op_tok.token == semantic.GREATER_THAN_EQUAL:
                return f"({left}>={right})"
            if item.op_tok.token == semantic.LESS_THAN:
                return f"({left}<{right})"
            if item.op_tok.token == semantic.LESS_THAN_EQUAL:
                return f"({left}<={right})"
            if item.op_tok.token == semantic.E_EQUAL:
                # print("in ==")
                # if isinstance(left,semantic.String):
                #     print('left is a string e_equal')
                #     # if isinstance(right, semantic.String):
                #     #     return f"'{left.value}'=='{right.value}'"
                #     return f"'{left.value}'=={right}"
                if isinstance(left, str):
                    # print('left is a string e_equal')
                    if isinstance(right, str):
                        # print("right is a str")
                        condition_to_list.append(left)
                        condition_to_list.append(item.op_tok.token)
                        condition_to_list.append(right)
                        # print("condition to list: ", condition_to_list)
                        str_cond = ''.join(condition_to_list)
                        return str_cond
                        # return f"'{left}' == '{right}'"
                        # "mel" == "mel"' == "hihi"
                    elif isinstance(right,semantic.String):
                        # print('right is a String')
                        return left + item.op_tok.token + f"'{right.value}'"
                    elif isinstance(right, int):
                        return f"({left}=={right})"
                    else:
                        return f"({left}=={right.value})"
                elif isinstance(left,int):
                    return f"({left}=={right})"
                elif isinstance(left,semantic.Number):
                    return f"({left}=={right})"
        else:
            # item.notted = False
            if item.op_tok.token == semantic.PLUS:
                if isinstance(left, semantic.String):
                    
                    return semantic.String(left.value+right.value)
                else:
                    return f"not ({left}+{right})"
            if item.op_tok.token == semantic.MINUS:
                return f"not ({left}-{right})"
            if item.op_tok.token == semantic.MUL:
                return f"not ({left}*{right})"
            if item.op_tok.token == semantic.DIV:
                print("found div bin op")
                return f"not ({left}/{right})"
            if item.op_tok.token == semantic.MODULUS:
                print("modulus")
                return f"not ({left}%{right})"
            if item.op_tok.token == semantic.GREATER_THAN:
                return f"not ({left}>{right})"
            if item.op_tok.token == semantic.GREATER_THAN_EQUAL:
                return f"not ({left}>={right})"
            if item.op_tok.token == semantic.LESS_THAN:
                return f"not ({left}<{right})"
            if item.op_tok.token == semantic.LESS_THAN_EQUAL:
                return f"not ({left}<={right})"
            if item.op_tok.token == semantic.E_EQUAL:
                print("in ==")
                if isinstance(left,semantic.String):
                    print('left is a string e_equal')
                    if isinstance(right, semantic.String):
                        return f"'not {left.value}'=='{right.value}'"
                    return f"'not {left.value}'=={right}"
                elif isinstance(left, str):
                    print('left is a string e_equal')
                    if isinstance(right, str):
                        print("right is a str")
                        condition_to_list.append(left)
                        condition_to_list.append(item.op_tok.token)
                        condition_to_list.append(right)
                        print("condition to list: ", condition_to_list)
                        str_cond = ''.join(condition_to_list)
                        return str_cond
                        # return f"'{left}' == '{right}'"
                        # "mel" == "mel"' == "hihi"
                    elif isinstance(right,semantic.String):
                        print('right is a String')
                        return left + item.op_tok.token + f"'{right.value}'"
                    elif isinstance(right, int):
                        return f"not ({left}=={right})"
                    else:
                        return f"not ({left}=={right.value})"
                elif isinstance(left,int):
                    return f"not ({left}=={right})"
                elif isinstance(left,semantic.Number):
                    return f"not ({left}=={right})"
                
        if item.op_tok.token == semantic.NOT_EQUAL:
            # print("in !=")
            if isinstance(left,semantic.String):
                # print('left is a string not equal')
                if isinstance(right, semantic.String):
                    return f"'{left.value}'!='{right.value}'"
                return f"'{left.value}'!={right}"
            elif isinstance(left, str):
                # print('left is a string e_equal')
                if isinstance(right, str):
                    # print("right is a str")
                    condition_to_list.append(left)
                    condition_to_list.append(item.op_tok.token)
                    condition_to_list.append(right)
                    print("condition to list: ", condition_to_list)
                    str_cond = ''.join(condition_to_list)
                    return str_cond
                    # return f"'{left}' == '{right}'"
                    # "mel" == "mel"' == "hihi"
                elif isinstance(right,semantic.String):
                    # print('right is a String')
                    return left + item.op_tok.token + f"'{right.value}'"
                elif isinstance(right, int):
                    return f"({left}!={right})"

                else:
                    
                    return f"({left}!={right.value})"

            elif isinstance(left,int):
                return f"({left}!={right})"
            elif isinstance(left,semantic.Number):
                return f"({left}!={right})"
        if item.op_tok.token == semantic.AND_OP:
            return f"({left} and {right})"
        if item.op_tok.token == semantic.OR_OP:
            return f"({left} or {right})"
        # print("reached the end of the bin op: ", item.op_tok.token)
    elif isinstance (item, semantic.CropAssignNode):
        # print("var assign line tracker: ", line_tracker.current_line)
        line_tracker.set(item.crop_name_tok.pos_start.ln+1)
        line_tracker.advance()
        # print("in var assign node transpiler: ", item.value_node)
        if isinstance(item.value_node, semantic.VoidNode):
            # print("found void node")
            if is_python_keyword(item.crop_name_tok.value):
            
                return f"{' '* current_indention}{item.crop_name_tok.value}1 = void()"
            else:
                return f"{' '* current_indention}{item.crop_name_tok.value} = void()"
        #key error wala sha sa dict
        
        # print("symbol table call: ", symbol_table.symbols)
        # value = symbol_table.symbols[item.crop_name_tok.value]
        # print("var assign value node: ", item.value_node)
        elif isinstance(item.value_node, semantic.CraftCallNode):
            form_params = []
            # should append the function call
            for param in item.value_node.parameters:
                # print("argument: ", param)
                if isinstance(param, semantic.NumberNode):
                    form_params.append(f"{param.tok.value}")
                elif isinstance(param, semantic.StringNode):
                    form_params.append(f"'{param.tok.value}'")
                elif isinstance(param, semantic.BinOpNode):
                    bin_op_param = read_nodes(param, {}, symbol_table)
                    form_params.append(f"{bin_op_param}")
                else:
                    form_params.append(f"{param.crop_name_tok.value}")
            # print("form param: ", form_params)
            # print(f"assign form call: {item.crop_name_tok.value} = '{value.value.value}'")
            if is_python_keyword(item.value_node.identifier.value):
                # print_items.append(f"{output.identifier.value}1({parameters})")
                return f"{' '* current_indention}{item.crop_name_tok.value} = {item.value_node.identifier.value}1({','.join(form_params)})"
                    
            else:
                # print_items.append(f"{output.identifier.value}({parameters})")
                return f"{' '* current_indention}{item.crop_name_tok.value} = {item.value_node.identifier.value}({','.join(form_params)})"
        elif isinstance(item.value_node, semantic.ListCallNode):
            if isinstance(item.value_node.index, CropAccessNode):
                return f"{' '* current_indention}{item.crop_name_tok.value} = {item.value_node.crop_name.crop_name_tok.value}[{item.value_node.index.crop_name_tok.value}]"
            else:
                return f"{' '* current_indention}{item.crop_name_tok.value} = {item.value_node.crop_name.crop_name_tok.value}[{item.value_node.index.value}]"
        value = read_nodes(item.value_node, symbol_table, current_indention)
        # print("value type var assign: ", type(value))
        
        
        if isinstance(value, list):
            # print("found list transpiler")
            if is_python_keyword(item.crop_name_tok.value):
            
                return f"{' '* current_indention}{item.crop_name_tok.value}1 = {value}"
            else:
                return f"{' '* current_indention}{item.crop_name_tok.value} = {value}"
            
        else:
            if is_python_keyword(item.crop_name_tok.value):
                
                return f"{' '* current_indention}{item.crop_name_tok.value}1 = {value}"
            else:
                return f"{' '* current_indention}{item.crop_name_tok.value} = {value}"

    elif isinstance(item, semantic.CollectNode):
        print("FOUND COLLECT NODE TRANSPILER")
        # print("inner node pos: ", line_tracker.current_line)
        line_tracker.set(item.variable_node.pos_start.ln+1)
        line_tracker.advance()
        ##crop_name = i.variable_node.crop_name_tok.value
        var_node = item.variable_node
        if isinstance(var_node, semantic.CropAccessNode):
            print("found varaccessnode")
            crop_name_tok = var_node.crop_name_tok
            return f" custom_input({item.prompt.value})"
    elif isinstance(item, semantic.CropInitNode):
        # print("var init: ", type(item.crop_name_tok))
        line_tracker.set(item.pos_start.ln+1)
        line_tracker.advance()
        if isinstance(item.value_node, semantic.VoidNode):
            # print("found void node")
            if isinstance(item.crop_name_tok, semantic.ListCallNode):
                index = read_nodes(item.crop_name_tok.index, {}, symbol_table)
                if is_python_keyword(item.crop_name_tok.crop_name.value):
                    return f"{' '* current_indention}{item.crop_name_tok.crop_name.value}1[{index}] = void()"
                else:
                    return f"{' '* current_indention}{item.crop_name_tok.crop_name.value}[{index}] = void()"
            else:
                if is_python_keyword(item.crop_name_tok.value):
                
                    return f"{' '* current_indention}{item.crop_name_tok.value}1 = void()"
                else:
                    return f"{' '* current_indention}{item.crop_name_tok.value} = void()"
        #key error wala sha sa dict
        
        # print("symbol table call: ", symbol_table.symbols)
        # value = symbol_table.symbols[item.crop_name_tok.value]
        # print("var assign value node: ", item.value_node)
        elif isinstance(item.value_node, semantic.CraftCallNode):
            form_params = []
            # should append the function call
            for param in item.value_node.parameters:
                # print("argument: ", param)
                if isinstance(param, semantic.NumberNode):
                    form_params.append(f"{param.tok.value}")
                else:
                    form_params.append(f"{param.crop_name_tok.value}")
            # print("form param: ", form_params)
            # print(f"assign form call: {item.crop_name_tok.value} = '{value.value.value}'")
            return f"{' '* current_indention}{item.crop_name_tok.value} = {item.value_node.identifier.value}({','.join(form_params)})"
        #if value us a list
        elif isinstance(item.value_node, semantic.ListCallNode):
            index = read_nodes(item.value_node.index, {}, symbol_table)
            if not isinstance(item.crop_name_tok, semantic.Token):
                index = read_nodes(item.crop_name_tok.index, {}, symbol_table)
                if isinstance(item.crop_name_tok, semantic.ListCallNode):
                    return f"{' '* current_indention}{item.crop_name_tok.crop_name.value}[{index}] {item.operation.value} {item.value_node.crop_name.crop_name_tok.value}[{item.value_node.index.crop_name_tok.value}]"
                else:
                    return f"{' '* current_indention}{item.crop_name_tok.value} {item.operation.value} {item.value_node.crop_name.crop_name_tok.value}[{item.value_node.index.value}]"
            else:
                return f"{' '* current_indention}{item.crop_name_tok.value} {item.operation.value}  {item.value_node.crop_name.crop_name_tok.value}[{index}]"

        value = read_nodes(item.value_node, {}, current_indention)
        #if the name is not a token
        if not isinstance(item.crop_name_tok, semantic.Token):
            # print("here")
            if isinstance(item.crop_name_tok.index, semantic.BinOpNode):
                index = read_nodes(item.crop_name_tok.index, {}, symbol_table)
                return f"{' '* current_indention}{item.crop_name_tok.crop_name.value}[{index}] {item.operation.value} {value}"
        if isinstance(item.crop_name_tok, semantic.ListCallNode):
            # print("list init")
            index = read_nodes(item.crop_name_tok.index, {}, symbol_table)
            return f"{' '* current_indention}{item.crop_name_tok.crop_name.value}[{index}] {item.operation.value} {value}"
        # print('wat')
        return f"{' '* current_indention}{item.crop_name_tok.value} {item.operation.value} {value}"
    elif isinstance(item, semantic.CraftCallNode):
        # print("called form")
        line_tracker.set(item.pos_start.ln+1)
        line_tracker.advance()
        params = []
        for call_param in item.parameters:
            # Convert call_param.tok.value to string explicitly
            if isinstance(call_param, semantic.CropAccessNode):
                # print("param var access")
                param_value = f"{call_param.crop_name_tok.value}"
                # print("param val: ", param_value)
            elif isinstance(call_param, semantic.NumberNode):

                param_value = f"{call_param.tok.value}"
            elif isinstance(call_param, semantic.ListCallNode):
                index = read_nodes(call_param.index, {}, symbol_table)
                param_value = f"{call_param.crop_name.crop_name_tok.value}[{index}]"
            else:
                param_value = f"'{call_param.tok.value}'"
            params.append(param_value)
        # print("params: ", params)
        parameters = ",".join(params)
        # print("parameters: ", parameters)
        if is_python_keyword(item.identifier.value):
            return f"{' '* current_indention}{item.identifier.value}1({parameters})"
        else:
            return f"{' '* current_indention}{item.identifier.value}({parameters})"


    elif isinstance(item, semantic.StarNode):
        line_tracker.set(item.pos_start.ln+1)
        line_tracker.advance()
        cases_code = []
        else_case_code = []
        for idx, (condition, statements) in enumerate(item.cases):
            # print("condition: ", condition)
            # print("statements: ", statements)
            # print('condition type: ', type(condition))
            condition_code = read_nodes(condition, symbol_table,current_indention)
            # print("condition code: ", condition_code)
            # print("current indention: ", current_indention)
            
            if idx == 0:
                # print("condition code: ", condition_code)
                # cases_code.append(f"if {condition_code}:")
                if isinstance(condition_code,semantic.SemanticTrue):
                    cases_code.append(f"{' ' * current_indention}if True:")
                elif isinstance(condition_code,semantic.SemanticFalse):
                    cases_code.append(f"{' ' * current_indention}if False:")
                else:
                    cases_code.append(f"{' ' * current_indention}if {condition_code}:")
            else:  # Subsequent conditions are processed as 'elif' statements
                # cases_code.append(f"{' ' * current_indention}elif {condition_code}:")
                if isinstance(condition_code,semantic.SemanticTrue):
                    cases_code.append(f"{' ' * current_indention}elif True:")
                elif isinstance(condition_code,semantic.SemanticFalse):
                    cases_code.append(f"{' ' * current_indention}elif False:")
                else:
                    cases_code.append(f"{' ' * current_indention}elif {condition_code}:")

            current_indention += 4
            if statements:
                for i in statements:
                    statements_code = read_nodes(i, symbol_table, current_indention)
                    
                    cases_code.append(f"{statements_code}")
            else:
                cases_code.append(f"{' '* current_indention}pass")
                
            current_indention -= 4
        # print("else case: ", item.else_case)
        if item.dew_case:
            line_tracker.advance()
            line_tracker.set(item.pos_start.ln+1)
            else_case_code.append(f"{' ' * current_indention}else:")
            current_indention += 4
            for j in item.dew_case:
                
                else_case_code.append(read_nodes(j, symbol_table, current_indention))
                

        else:
            "pass"
            
        current_indention -= 4
        return "\n".join(cases_code + else_case_code)
    elif isinstance(item, semantic.WinterNode):
        line_tracker.set(item.pos_start.ln+1)
        line_tracker.advance()
        whirl_code = []
        print("whirl node in transpiler cond: ", type(item.condition))
        condition = read_nodes(item.condition, {}, current_indention)
        print("whirl cond: ", condition)
        whirl_code.append(f"{' '* current_indention}while {condition}: ")
        current_indention += 4
        if item.body:
            for i in item.body:
                val = read_nodes(i, {}, current_indention)
                whirl_code.append(val)
            current_indention -= 4
        else:
            whirl_code.append(f"{' '* current_indention}break ")
        return "\n".join(whirl_code)
    elif isinstance(item, semantic.CropAccessNode):
        # print("visiting var access read nodes")
        if is_python_keyword(item.crop_name_tok.value):
            
            return f"{item.crop_name_tok.value}1"
        else:
            return f"{item.crop_name_tok.value}"

    elif isinstance (item, semantic.HarvestCallNode):
        line_tracker.set(item.pos_start.ln+1)
        # line_tracker.advance()
        # print("in saturn call transpiler")
        # value = item.value
        value = read_nodes(item.value_node, symbol_table, current_indention)
        # line_tracker.advance()
        # print("saturn val transpiler: ", value)
        # print("saturn val transpiler: ", value)
        return f"{' ' * current_indention}return {value}"
    elif isinstance(item, semantic.ListNode):
        # print("in list node")
        list_node_items = []
        for i in item.items:
            # print("item in list: ", i)
            # print("i type: ", type(i))
            if isinstance(i, semantic.CropAccessNode):
                list_node_items.append(i.crop_name_tok.value)
            elif isinstance(i, semantic.BooleanNode):
                list_node_items.append('True')
            elif isinstance(i, semantic.NumberNode):
                list_node_items.append(str(i.tok.value))
                
            else:
                value = read_nodes(i, symbol_table, current_indention)
                # print("value type list item: ", type(value))
                list_node_items.append(value)
        list_as_string = ', '.join(list_node_items)

        return f"[{list_as_string}]"
    elif isinstance(item, semantic.BooleanNode):
        if item.value == 0:
            return False
        else:
            return True
    elif isinstance(item, semantic.PostUnaryNode):
        line_tracker.set(item.pos_start.ln+1)
        line_tracker.advance()
        # print('post unary node transpiler')
        if item.operation.token == semantic.DECRE:
            return f"{' ' * current_indention}{item.tok.crop_name_tok.value}-=1"
        elif item.operation.token == semantic.INCRE:
            return f"{' ' * current_indention}{item.tok.crop_name_tok.value}+=1"
    elif isinstance(item, semantic.PreUnaryNode):
        line_tracker.set(item.pos_start.ln+1)
        line_tracker.advance()
        # print('post unary node transpiler')
        if item.operation.token == semantic.DECRE:
            return f"{' ' * current_indention}{item.tok.crop_name_tok.value}-=1"
        elif item.operation.token == semantic.INCRE:
            return f"{' ' * current_indention}{item.tok.crop_name_tok.value}+=1"
    elif isinstance(item, semantic.NextNode):
        line_tracker.set(item.pos_start.ln + 1)
        line_tracker.advance()
        return f"{' ' * current_indention}continue"
    elif isinstance(item, semantic.BreakNode):
        line_tracker.set(item.pos_start.ln + 1)
        line_tracker.advance()
        return f"{' ' * current_indention}break"
    
    elif isinstance(item, semantic.FallNode):
        # print("in force node transpiler")
        line_tracker.set(item.pos_start.ln + 1)
        line_tracker.advance()
        print("force condition: ", item.condition)
        force_code = []
        var_init = read_nodes(item.variable, {}, current_indention)
        condition = read_nodes(item.condition, {}, current_indention)
        force_code.append(f"{var_init}")
        force_code.append(f"{' '* current_indention}while {condition}: ")
        current_indention += 4
        if item.body:
            for i in item.body:
                val = read_nodes(i, {}, current_indention)
                force_code.append(val)
        else:
            force_code.append(f"{' '* current_indention}break")

        unary = read_nodes(item.unary, {}, current_indention)
        # if isinstance(item.unary, semantic.PostUnaryNode):
        #     force_code.insert(2, f"{unary}")
        # elif isinstance(item.unary, semantic.PreUnaryNode):
        force_code.append(f"{unary}")
        
        current_indention -= 4
        return "\n".join(force_code)
    # elif isinstance(item, semantic.DoWinterNode):
    #     # print("do tok pos: ", item.do_tok.pos_start.ln+1)
    #     do_whirl_code = []
    #     if item.body:
    #         for i in item.body:
    #             val = read_nodes(i, {}, current_indention)
    #             do_whirl_code.append(val)
    #             # line_tracker.advance()
    #         # print("current pos after : ", line_tracker.current_line)
    #         # print("do whirl condition: ", type(item.condition))
    #         condition = read_nodes(item.condition, {}, current_indention)
    #         # print("dowhirl do tok pos start: ", item.do_tok.pos_start.ln+1)
    #         # print("condition pos : ", item.condition.pos_start.ln+1)
    #         do_whirl_code.append(f"{' '* current_indention}while {condition}: ")
    #         current_indention += 4
    #         line_tracker.set(item.condition.pos_start.ln + 1)
    #         line_tracker.advance()
    #         for i in item.body:
    #             val = read_nodes(i, {}, current_indention)
    #             do_whirl_code.append(val)
    #         line_tracker.set(item.pos_start.ln + 1)
    #         current_indention -= 4
    #     # else:
    #     #     force_code.append(f"{' '* current_indention}break")
    #     # return f"{' ' * current_indention}"
    #     return "\n".join(do_whirl_code)
    elif isinstance(item, semantic.ListCallNode):
        if isinstance(item.index, semantic.NumberNode):
            return f"{item.crop_name.crop_name_tok.value}[{item.index.tok.value}]"
        elif isinstance(item.index, semantic.CropAccessNode):
            return f"{item.crop_name.crop_name_tok.value}[{item.index.crop_name_tok.value}]"
        elif isinstance(item.index, semantic.BinOpNode):
            val = read_nodes(item.index,{}, symbol_table)
            return f"{item.crop_name.crop_name_tok.value}[{val}]"
        else:
            return f"{item.crop_name.crop_name_tok.value}[{item.index.value}]"

def convert_text_file_to_python_and_execute(ast, python_file):
    line_tracker.current_line = 1
    #ast is a Program instance
    python_code = []
    current_indentation = 0
    print("----------------")
    # ast.display()
    
    python_code = ["from built_in import custom_input, custom_print, load_dict_from_file, read_list_from_file, void, append, remove, length", "import sys", "import traceback", "line_map = load_dict_from_file('line_map.txt')", "lines = read_list_from_file('get_line.txt')","try:"]
    #advance line tracker 4 times coz we appended 4 items
    line_tracker.advance()
    line_tracker.advance()
    line_tracker.advance()
    
    line_tracker.advance()
    line_tracker.advance()
    # line_tracker.advance()
    current_indentation += 4
    for item in ast.body:
        if isinstance(item, semantic.CropAssignNode):
            # print("var assign line tracker: ", line_tracker.current_line)
            line_tracker.advance()
            line_tracker.set(item.crop_name_tok.pos_start.ln+1)
            # print("in var assign node transpiler")
            if isinstance(item.value_node, semantic.VoidNode):
                # print("found void node")
                python_code.append(f"{' '* current_indentation}{item.crop_name_tok.value} = void()")
            elif isinstance(item.value_node, semantic.ListCallNode):
                python_code.append(f"{' '* current_indentation}{item.crop_name_tok.value} = {item.value_node.crop_name.crop_name_tok.value}[{item.value_node.index.value}]")
            value = read_nodes(item.value_node, {}, current_indentation)
            #key error wala sha sa dict
            python_code.append(f"{' '* current_indentation}{item.crop_name_tok.value} = {value}")

        elif isinstance(item, semantic.CraftNode):
            params = []
            for p in item.parameters:
                params.append(p.crop_name_tok.value)
            parameters = ",".join(params)

            line_tracker.set(item.identifier.pos_start.ln+1)
            line_tracker.advance()
            if is_python_keyword(item.identifier.value):
                python_code.append(f"{' ' * current_indentation}def {item.identifier.value}1 ({parameters}):")
            else:
                python_code.append(f"{' ' * current_indentation}def {item.identifier.value} ({parameters}):")
            # print("python code: ", python_code)
            current_indentation += 4
            line_tracker.advance()
            if item.body:
                
                for i in item.body:
                    res = read_nodes(i, item.symbol_table, current_indentation)
                    python_code.append(f"{res}")
                    # line_tracker.advance()
                    # line_tracker.set(i.pos_start.ln+1)
                
            else:
                print("function no body")
                python_code.append(f"{' ' * current_indentation}pass")
            current_indentation -= 4


        elif isinstance(item, semantic.PelicanNode):
            # print("theres a galaxy node")
            if item.body:
                line_tracker.advance()
                
                for i in item.body:
                    res = read_nodes(i,item.symbol_table, current_indentation)
                    # print("galaxy context table:",i.context.symbol_table)
                    # print("line tracker in galaxy(): ", line_tracker.tracker_dict)
                    python_code.append(f"{res}")
                    
                    #todo call read_nodes(i)
                    
                # def line_map():
                #     return line_tracker.tracker_dict
            else:
                python_code.append(f"{' '* current_indentation}pass")
        else:
            # Handle unknown or unsupported statements
            raise ValueError(f"Unsupported statement: {item}")

            # # Reset ignore_next_semicolon after processing
            # ignore_next_semicolon = False
    current_indentation -= 4
    python_code.append(f"{' ' * current_indentation}except Exception as e:")
    current_indentation += 4
    # print("current indentation: ", current_indentation)
    python_code.append(f"{' ' * current_indentation}exc_type, exc_value, exc_traceback = sys.exc_info()")
    # python_code.append(f"{' ' * current_indentation}print('Runtime Error:', exc_type.__name__)")
    python_code.append(f"{' ' * current_indentation}tb = traceback.extract_tb(e.__traceback__)")
    # python_code.append(f"{' ' * current_indentation}filename, line_number, _, _ = tb[-1]")
    # python_code.append(f"{' ' * current_indentation}print(f'Error: {e}')")
    python_code.append(f"{' ' * current_indentation}print('-------------')")
    python_code.append(f"{' ' * current_indentation}print(f'Runtime Error: {{e}}')")
    # python_code.append(f"{' ' * current_indentation}print(f'Traceback: ')")
    python_code.append(f"{' ' * current_indentation}for frame in tb:")
    current_indentation += 4
    python_code.append(f"{' ' * current_indentation}_, line_number, func_name, text = frame")
    python_code.append(f"{' ' * current_indentation}if func_name == '<module>':")
    current_indentation += 4
    python_code.append(f"{' ' * current_indentation}func_name = 'pelican()'")
    current_indentation -= 4
    python_code.append(f"{' ' * current_indentation}try:")
    current_indentation += 4
    python_code.append(f"{' ' * current_indentation}print(f'File <{{func_name}}>, line {{line_map[str(line_number)]}}')")
    # python_code.append(f"{' ' * current_indentation}print(f'Line number: {{line_map[str(line_number)]}}')")
    python_code.append(f"{' ' * current_indentation}index = int(line_map[str(line_number)])")
    python_code.append(f"{' ' * current_indentation}print(f'{{lines[index-1]}}')")
    current_indentation -= 4
    python_code.append(f"{' ' * current_indentation}except:")
    current_indentation += 4
    python_code.append(f"{' ' * current_indentation}pass")
    
    # print("global line tracker: ", line_tracker.tracker_dict)
    #set the line tracking so we can use in generated script
    # Write the generated Python code to the specified Python file
    with open('line_map.txt', 'w') as file:
        for key, value in line_tracker.tracker_dict.items():
            file.write(f"{key}:{value}\n")
    line_tracker.tracker_dict = {}
    
    

    # Write the Python code to a file
    with open(python_file, 'w') as f:
        f.write("\n".join(python_code))

    # Determine the current platform
    platform = sys.platform

    try:
        if platform == "win32":
            # Windows
            process = subprocess.Popen(['start', 'cmd', '/k', 'python', python_file], shell=True)
        elif platform == "darwin":
            # macOS
            process = subprocess.Popen(['open', '-a', 'Terminal', python_file])
        else:
            # Linux/Unix
            process = subprocess.Popen(['gnome-terminal', '--', 'python3', python_file])
        
        # Wait for the process to finish
        # process.wait()
        

        # Check the process return code
        if process.returncode != 0:
            return f"Error executing generated Python script: Return code {process.returncode}"
    except Exception as e:
        print(f"An error occurred: {e}")    
    # Terminate the process explicitly (optional, but recommended)
    # process.terminate()




# Example usage:
text_file_path = "program.cosmic"
python_file = "generated_script.py"

# print("global line map: ", line_map)
# Generate the Python script file from the custom text file
# convert_text_file_to_python_and_execute(body, python_file)
