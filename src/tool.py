#!/usr/bin/python3
import sys, json, ntpath, os
from AST.root import Root
from AST.block import Block
from AST.assign import Assign
from AST.variable import Variable
from AST.expression import Expression
from AST.binop import BinaryOperation
from AST.boolop import BooleanOperation
from AST.ifelse import If
from AST.whileelse import While
from AST.symtable import SymTable
from AST.functioncall import FunctionCall
from AST.attribute import Attribute
from vuln.vulnerability import Vulnerability
from AST.tuple import Tuple
from AST.list import List

from AST.visitors.debugger import Debugger
from AST.visitors.explicitleaks import MarkExplicitLeaks

from copy import deepcopy


vuln_list = []

def main(argv, arg):

    if(arg != 3):
        print("Usage: ./tool.py codeSlice.json vulnerabilityPattern.json")
        sys.exit(1)

    try:
        with open(argv[1], 'r') as myfile:
            json_code = myfile.read()
    except FileNotFoundError:
        print("Wrong codeSlice file or path")
        sys.exit(1)

    try:
        with open(argv[2], 'r') as myfile:
            json_vulnPatterns = myfile.read()
    except FileNotFoundError:
        print("Wrong vulnerabilityPattern file or path")
        sys.exit(1)

    parsed_vulnerabilities = json.loads(json_vulnPatterns)

    output_name = ntpath.basename(argv[1]).split('.json')[0] + ".out.json"

    data = []
    with open(output_name, 'w') as outfile:
        json.dump(data, outfile)

    for vuln in parsed_vulnerabilities:
        if not isInVuln(vuln_list, vuln):
            vuln_list.append(Vulnerability(vuln["vulnerability"], vuln["sources"], vuln["sanitizers"], vuln["sinks"], output_name))      
    

    parsed_json = json.loads(json_code)

    
    
    for vuln in vuln_list:
        program_block = createNodes(parsed_json, None, vuln)
        #For each vulnerability mark each function as source, sanitizer or sink
        #print tree
        #debugger = Debugger()
        #program_block.traverse(debugger)
        #detect explicit -> append to file
        #explicitleaks = MarkExplicitLeaks()
        #program_block.traverse(explicitleaks)
        #debugger = Debugger()
        #program_block.traverse(debugger)
        #detect implicit -> append to file
    

                
def createNodes(parsed_json, symtable=None, vuln=None):
    #case where you have a list of instructions
    if(type(parsed_json) == list):
        instruction_nodes = []

        for instruction in parsed_json:
            node = createNodes(instruction, symtable, vuln)

            if node is not None: #discarded instruction simply ignore
                instruction_nodes.append(node)
        return instruction_nodes
    
    elif (type(parsed_json) == dict):
        nodeType = parsed_json['ast_type']

        if (nodeType == "Module"):
            instructions = []
            symt = SymTable()
            for instruction in parsed_json['body']:
                instructions.append(createNodes(instruction, symt, vuln))
            return Root(Block(symt, instructions))

        elif(nodeType == "Assign"):
            targets = createNodes(parsed_json['targets'][0], symtable, vuln)
            value = createNodes(parsed_json['value'], symtable, vuln)
                 
            # normal variable assign
            targets.tainted = value.tainted
            targets.sources = value.sources
            targets.sanitizers = value.sanitizers

            # correct left value to remove source tag
            targets.type = ""

            return Assign(targets, value)

        elif(nodeType == "If"):
            condition = createNodes(parsed_json['test'], symtable, vuln)  
            
            symtableBody = deepcopy(symtable)
            symtableElse = deepcopy(symtable)

            body = Block(symtableBody, createNodes(parsed_json['body'], symtableBody, vuln))
            orelse = Block(symtableElse, createNodes(parsed_json['orelse'], symtableElse, vuln))

            clearsymtableBody = body.symtable
            clearsymtableElse = orelse.symtable

            #if else is empty then clearsymtableElse will be equal to symtable
            ifsymtable = clearsymtableBody + clearsymtableElse

            symtable.concat(ifsymtable) 

            return If(condition, body, orelse)
                
        elif(nodeType == "Expr"):
            return Expression(createNodes(parsed_json['value'], symtable, vuln))

        elif(nodeType == "Tuple"):
            return Tuple(createNodes(parsed_json['elts'], symtable, vuln))

        elif(nodeType == "List"):
            return List(createNodes(parsed_json['elts'], symtable, vuln))

        elif(nodeType == "Compare"):
            comparators = createNodes(parsed_json['comparators'], symtable, vuln)
            variable = createNodes(parsed_json['left'], symtable, vuln)

            isTainted = False
            for expression in comparators:
                if(expression.tainted):
                    isTainted = True
                    break
                    
            # if the variable is tainted or the expression then the result is tainted
            return Expression(None, isTainted or variable.tainted)

        elif(nodeType == "Name"):
            #check if id is in symtable
            # yes -> get object
            # no -> create

            variable = symtable.getVariable(parsed_json['id'])
            if variable is None:
                variable = Variable(parsed_json['id'])
                variable.type = "source"
                variable.sources.append(variable)            
                symtable.addEntry(variable)

            return variable

        elif(nodeType == "Num"):
            return createNodes(parsed_json['n'], symtable, vuln)

        elif(nodeType == "Str"):
            return Expression(None, False)

        elif(nodeType == "int"):
            return Expression(None, False)

        elif(nodeType == "BinOp"):
            left = createNodes(parsed_json['left'], symtable, vuln)
            right = createNodes(parsed_json['right'], symtable, vuln)
            return BinaryOperation(left, right)

        elif(nodeType == "While"):

            condition = createNodes(parsed_json['test'], symtable, vuln)

            symtableBody = deepcopy(symtable)
            symtableElse = deepcopy(symtable)
            
            #Special case when vulnerabilities are only detected with multiple body loop iterations
            lastSymtable = None
            while True:
                body = Block(symtableBody, createNodes(parsed_json['body'], symtableBody, vuln))

                if lastSymtable is not None:
                    oldLastSymtable = deepcopy(lastSymtable)
                    lastSymtable = lastSymtable + deepcopy(symtableBody)
                    if oldLastSymtable == lastSymtable:
                        break
                else:
                    lastSymtable = deepcopy(symtableBody)

                
            orelse = Block(symtableElse, createNodes(parsed_json['orelse'], symtableElse, vuln))

            clearsymtableBody = lastSymtable
            clearsymtableElse = orelse.symtable
            
            whilesymtable = clearsymtableBody + clearsymtableElse
            symtable.concat(whilesymtable)

            return While(condition, body, orelse)

        elif(nodeType == "NameConstant"):
            return Expression(None, False)

        elif(nodeType == "Call"):
            args = createNodes(parsed_json['args'], symtable, vuln)
            # Special case when calling objects functions
            if parsed_json['func']['ast_type'] == "Attribute":
                value = createNodes(parsed_json['func']['value'], symtable, vuln)
                fcall = FunctionCall(parsed_json['func']['attr'], args, value)
                fcall.type = vuln.getType(fcall.name)
                
            else:
                name = parsed_json['func']['id']

                fcall = FunctionCall(name, args)
                fcall.type = vuln.getType(fcall.name)

            if fcall.type == "source":
                fcall.tainted = True
                fcall.sources.append(fcall)
            
            elif fcall.type == "sink" and fcall.tainted:
                listIDs = []
                listSanIDs = []
                for obj in fcall.sources:
                    listIDs.append(obj.getID())
                for obj in fcall.sanitizers:
                    listSanIDs.append(obj.getID())
                print("************************\n"+"Vulnerability: {}\nSink: {}\nSources: {}\nSanitizers: {}\n************************".format(vuln.name, fcall.name, list(set(listIDs)),list(set(listSanIDs))))
                container = {'vulnerability': vuln.name, 'sink': fcall.name, 'source': list(set(listIDs)), 'sanitizer': list(set(listSanIDs))}
            
                with open(vuln.output, "r") as jsonFile:
                    data = json.load(jsonFile)
                tmp = data
                data.append(container)
                with open(vuln.output, 'w') as outfile:
                    json.dump(data, outfile, ensure_ascii=False, indent=4)

            elif fcall.type == "sanitizer":
                fcall.sanitizers.append(fcall)
            
            return fcall

        elif(nodeType == "Attribute"):
            variable = symtable.getVariable(parsed_json['attr'])
            if variable is None:
                variable = Variable(parsed_json['attr'])
                variable.type = "source"
                variable.sources.append(variable)            
                symtable.addEntry(variable)

            value = createNodes(parsed_json['value'], symtable, vuln)

            return Attribute(variable, value)

        elif(nodeType == "BoolOp"):
            return BooleanOperation(createNodes(parsed_json['values'], symtable, vuln))

        else: #discard this instruction
            return None

def isInVuln(vuln_list, vuln):
    for vuln_elm in vuln_list:
            if vuln_elm.name == vuln["vulnerability"]:
                vuln_elm.addSources(vuln["sources"])
                vuln_elm.addSanitizers(vuln["sanitizers"])
                vuln_elm.addSinks(vuln["sinks"])
                return True
    return False

if __name__== "__main__":
    main(sys.argv, len(sys.argv))