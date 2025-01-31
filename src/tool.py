#!/usr/bin/python3
import sys, json, ntpath, os
from AST.root import Root
from AST.block import Block
from AST.assign import Assign
from AST.variable import Variable
from AST.expression import Expression
from AST.binop import BinaryOperation
from AST.boolop import BooleanOperation
from AST.compare import Compare
from AST.ifelse import If
from AST.whileelse import While
from AST.symtable import SymTable
from AST.functioncall import FunctionCall
from AST.attribute import Attribute
from vuln.vulnerability import Vulnerability
from AST.tuple import Tuple
from AST.list import List
from AST.implicitstack import ImplicitStack

from AST.visitors.debugger import Debugger

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

    output_name = os.path.splitext(argv[1])[0] + ".output.json"

    data = []
    with open(output_name, 'w') as outfile:
        json.dump(data, outfile)

    for vuln in parsed_vulnerabilities:
        if not isInVuln(vuln_list, vuln):
            vuln_list.append(Vulnerability(vuln["vulnerability"], vuln["sources"], vuln["sanitizers"], vuln["sinks"], output_name))      
    

    parsed_json = json.loads(json_code)

    
    
    for vuln in vuln_list:
        implicitStack = ImplicitStack()
        program_block = createNodes(parsed_json, None, vuln, implicitStack)
        #For each vulnerability mark each function as source, sanitizer or sink
        #debugger = Debugger()
        #program_block.traverse(debugger)
                
def createNodes(parsed_json, symtable=None, vuln=None, implicitStack=None):
    #case where you have a list of instructions
    if(type(parsed_json) == list):
        instruction_nodes = []

        for instruction in parsed_json:
            node = createNodes(instruction, symtable, vuln, implicitStack)

            if node is not None: #discarded instruction simply ignore
                instruction_nodes.append(node)
        return instruction_nodes
    
    elif (type(parsed_json) == dict):
        nodeType = parsed_json['ast_type']

        if (nodeType == "Module"):
            instructions = []
            symt = SymTable()
            for instruction in parsed_json['body']:
                instructions.append(createNodes(instruction, symt, vuln, implicitStack))
            return Root(Block(symt, instructions))

        elif(nodeType == "Assign"):
            def perform_assign(targets, value, implicitStack):
                srcs = deepcopy(implicitStack.getSources())
                # normal variable assign
                targets.tainted = value.tainted
                targets.sources = value.sources
                if value.tainted:
                    targets.sanitizers = value.sanitizers

                #adds implicit sources to left variables
                #srcs = implicitStack.getSources()
                for implicitSource in srcs:
                    if implicitSource not in targets.sources:
                        targets.sources.append(implicitSource)
                if value.tainted:
                    targets.sanitizers += implicitStack.getSanitizers()

                if len(srcs) > 0:
                    targets.tainted = True

                # correct left value to remove source tag
                targets.type = ""

            leftValues = []
            for target in parsed_json['targets']:
                targets = createNodes(target, symtable, vuln, implicitStack)
                leftValues.append(targets)
                value = createNodes(parsed_json['value'], symtable, vuln, implicitStack)
                
                if (targets.__class__.__name__ == "Tuple" and value.__class__.__name__ == "Tuple") or \
                    (targets.__class__.__name__ == "List" and value.__class__.__name__ == "List"):
                    for i in range(0, len(targets.elements)):
                        perform_assign(targets.elements[i], value.elements[i], implicitStack)
                else:
                    perform_assign(targets, value, implicitStack)

            return Assign(leftValues, value)

        elif(nodeType == "If"):
            condition = createNodes(parsed_json['test'], symtable, vuln, implicitStack)

            implicitStack.push(condition)
            
            symtableBody = deepcopy(symtable)
            symtableElse = deepcopy(symtable)

            body = Block(symtableBody, createNodes(parsed_json['body'], symtableBody, vuln, implicitStack))
            orelse = Block(symtableElse, createNodes(parsed_json['orelse'], symtableElse, vuln, implicitStack))

            clearsymtableBody = body.symtable
            clearsymtableElse = orelse.symtable

            #if else is empty then clearsymtableElse will be equal to symtable
            ifsymtable, inBoth = clearsymtableBody.inBoth(clearsymtableElse)

            symtable.concatWithInBoth(ifsymtable, inBoth)

            implicitStack.pop()

            return If(condition, body, orelse)
                
        elif(nodeType == "Expr"):
            return Expression(createNodes(parsed_json['value'], symtable, vuln, implicitStack))

        elif(nodeType == "Tuple"):
            return Tuple(createNodes(parsed_json['elts'], symtable, vuln, implicitStack))

        elif(nodeType == "List"):
            return List(createNodes(parsed_json['elts'], symtable, vuln, implicitStack))

        elif(nodeType == "Compare"):
            comparators = createNodes(parsed_json['comparators'], symtable, vuln, implicitStack)
            left = createNodes(parsed_json['left'], symtable, vuln, implicitStack)

            # if the variable is tainted or the expression then the result is tainted
            return Compare(left, comparators)

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
            return createNodes(parsed_json['n'], symtable, vuln, implicitStack)

        elif(nodeType == "Str"):
            return Expression(None, False)

        elif(nodeType == "int"):
            return Expression(None, False)

        elif(nodeType == "BinOp"):
            left = createNodes(parsed_json['left'], symtable, vuln, implicitStack)
            right = createNodes(parsed_json['right'], symtable, vuln, implicitStack)
            return BinaryOperation(left, right)

        elif(nodeType == "While"):

            symtableBody = deepcopy(symtable)
            symtableElse = deepcopy(symtable)
            
            #Special case when vulnerabilities are only detected with multiple body loop iterations
            lastSymtable = None
            while True:
                condition = createNodes(parsed_json['test'], symtableBody, vuln, implicitStack)

                implicitStack.push(condition)

                body = Block(symtableBody, createNodes(parsed_json['body'], symtableBody, vuln, implicitStack))

                if lastSymtable is not None:
                    oldLastSymtable = deepcopy(lastSymtable)
                    lastSymtable = lastSymtable + deepcopy(symtableBody)
                    if oldLastSymtable == lastSymtable:
                        break
                else:
                    lastSymtable = deepcopy(symtableBody)
                implicitStack.pop()


            orelse = Block(symtableElse, createNodes(parsed_json['orelse'], symtableElse, vuln, implicitStack))

            clearsymtableBody = lastSymtable
            clearsymtableElse = orelse.symtable

            whilesymtable, inBoth = clearsymtableBody.inBoth(clearsymtableElse)

            symtable.concatWithInBoth(whilesymtable, inBoth)

            implicitStack.pop()

            return While(condition, body, orelse)

        elif(nodeType == "NameConstant"):
            return Expression(None, False)

        elif(nodeType == "Call"):
            args = createNodes(parsed_json['args'], symtable, vuln, implicitStack)
            # Special case when calling objects functions
            if parsed_json['func']['ast_type'] == "Attribute":
                value = createNodes(parsed_json['func']['value'], symtable, vuln, implicitStack)
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
                sanitizersDict = {}
                alreadySanitized = []
                noSanitizer = []
                for obj in fcall.sanitizers:
                    if obj not in sanitizersDict:
                        sanitizersDict[obj] = []
                    for source in obj.sources:
                        sanitizersDict[obj].append(source)
                        alreadySanitized.append(source)

                for obj in fcall.sources:
                    if obj not in alreadySanitized:
                        noSanitizer.append(obj)


                with open(vuln.output, "r") as jsonFile:
                    data = json.load(jsonFile)

                for key in sanitizersDict:
                    ids = []
                    for source in sanitizersDict[key]:
                        if source.getID() not in ids:
                            ids.append(source.getID())

                    if len(ids) > 1:
                        container = {'vulnerability': vuln.name, 'sink': fcall.name, 'source': ids, 'sanitizer': key.getID()}
                    else:
                        container = {'vulnerability': vuln.name, 'sink': fcall.name, 'source': ids[0],
                                     'sanitizer': key.getID()}
                    
                    if container not in data:
                        data.append(container)
                        #print("************************\n"+"Vulnerability: {}\nSink: {}\nSources: {}\nSanitizer: {}\n************************".format(vuln.name, fcall.name, ids, key.getID()))
                        
                    with open(vuln.output, 'w') as outfile:
                        json.dump(data, outfile, ensure_ascii=False, indent=4)

                ids = []
                for source in noSanitizer:
                    if source.getID() not in ids:
                        ids.append(source.getID())

                if len(noSanitizer) > 0:
                    if len(ids) > 1:
                        container = {'vulnerability': vuln.name, 'sink': fcall.name, 'source': ids, 'sanitizer': ""}
                    else:
                        container = {'vulnerability': vuln.name, 'sink': fcall.name, 'source': ids[0],
                                     'sanitizer': ""}

                    if container not in data:
                        data.append(container)
                        #print("************************\n"+"Vulnerability: {}\nSink: {}\nSources: {}\nSanitizer: {}\n************************".format(vuln.name, fcall.name, ids, []))

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

            value = createNodes(parsed_json['value'], symtable, vuln, implicitStack)

            return Attribute(variable, value)

        elif(nodeType == "BoolOp"):
            return BooleanOperation(createNodes(parsed_json['values'], symtable, vuln, implicitStack))

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
