#!/usr/bin/python3
import sys, json
from AST.root import Root
from AST.assign import Assign
from AST.variable import Variable
from AST.expression import Expression
from AST.binop import BinaryOperation
from AST.ifelse import If


from AST.visitors.debugger import Debugger

def main(argv, arg):

    if(arg != 3):
        print("Usage: ./tool.py codeSlice.json vulnerabilityPattern.json")
        sys.exit(1)

    with open(argv[1], 'r') as myfile:
        json_code = myfile.read()

    parsed_json = json.loads(json_code)
    
    program_block = createNodes(parsed_json)
    debugger = Debugger()
    program_block.traverse(debugger)
  
def createNodes(parsed_json):
    #case where you have a list of instructions
    if(type(parsed_json) == list):
        instruction_nodes = []

        for instruction in parsed_json:
            node = createNodes(instruction)

            if node is not None: #discarded instruction simply ignore
                instruction_nodes.append(node)
        return instruction_nodes
    
    elif (type(parsed_json) == dict):
        nodeType = parsed_json['ast_type']

        if (nodeType == "Module"):
            instructions = []
            for instruction in parsed_json['body']:
                instructions.append(createNodes(instruction))
            return Root(instructions)

        elif(nodeType == "Assign"):
            targets = createNodes(parsed_json['targets'][0])
            value = createNodes(parsed_json['value'])
            return Assign(targets, value)

        elif(nodeType == "If"):
            condition = createNodes(parsed_json['test'])  
            body = createNodes(parsed_json['body'])
            orelse = createNodes(parsed_json['orelse'])
            return If(condition, body, orelse)
                
        elif(nodeType == "Expr"):
            return Expression(False)

        elif(nodeType == "Compare"):
            # a == 2
            comparators = createNodes(parsed_json['comparators'])
            variable = createNodes(parsed_json['left'])

            isTainted = False
            for expression in comparators:
                if(expression.tainted):
                    isTainted = True
                    break
                    
            # if the variable is tainted or the expression then the result is tainted
            return Expression(isTainted or variable.tainted)

        elif(nodeType == "Call"):
            print("\t" + nodeType)

        elif(nodeType == "Name"):
            return Variable(parsed_json['id'])

        elif(nodeType == "Num"):
            return createNodes(parsed_json['n'])

        elif(nodeType == "Str"):
            return Expression(False)

        elif(nodeType == "int"):
            return Expression(False)

        elif(nodeType == "BinOp"):
            left = createNodes(parsed_json['left'])
            right = createNodes(parsed_json['right'])
            return BinaryOperation(left, right)

        else: #discard this instruction
            return None

if __name__== "__main__":
    main(sys.argv, len(sys.argv))