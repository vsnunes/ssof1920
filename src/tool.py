#!/usr/bin/python3
import sys, json
from AST.block import Block
from AST.assign import Assign
from AST.variable import Variable
from AST.expression import Expression
from AST.binop import BinaryOperation

from AST.visitors.debuger import Debugger

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
    nodeType = parsed_json['ast_type']

    if (nodeType == "Module"):
        instructions = []
        for instruction in parsed_json['body']:
            instructions.append(createNodes(instruction))
        return Block(instructions)

    elif(nodeType == "Assign"):
        targets = createNodes(parsed_json['targets'][0])
        value = createNodes(parsed_json['value'])
        return Assign(targets, value)

    elif(nodeType == "If"):
        print("\t" + nodeType)
        
    elif(nodeType == "Expr"):
        value = createNodes(parsed_json['value'])
        return Expression(value)

    elif(nodeType == "Call"):
        print("\t" + nodeType)

    elif(nodeType == "Name"):
        return Variable(parsed_json['id'])

    elif(nodeType == "Num"):
        return createNodes(parsed_json['n'])

    elif(nodeType == "Str"):
        return Expression(parsed_json['s'])

    elif(nodeType == "int"):
        return Expression(parsed_json['n'])

    elif(nodeType == "BinOp"):
        left = createNodes(parsed_json['left'])
        right = createNodes(parsed_json['right'])
        return BinaryOperation(left, right)


if __name__== "__main__":
    main(sys.argv, len(sys.argv))