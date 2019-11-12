#!/usr/bin/python3
import sys, json

def main(argv, arg):

    if(arg != 3):
        print("Usage: ./tool.py codeSlice.json vulnerabilityPattern.json")
        sys.exit(1)

    with open(argv[1], 'r') as myfile:
        json_code = myfile.read()

    parsed_json = json.loads(json_code)
    print(parsed_json)
    createNodes(parsed_json) 
  
def createNodes(parsed_json):
    nodeType = parsed_json['ast_type']

    if (nodeType == "Module"):
        for instruction in parsed_json['body']:
            createNodes(instruction)
    elif(nodeType == "Assign"):
        print("\t" + nodeType)
        print(parsed_json)
        a = createNodes(parsed_json['targets'][0])
        b = createNodes(parsed_json['value'])
        #return Assign(a, b)
    elif(nodeType == "If"):
        print("\t" + nodeType)
    elif(nodeType == "Expr"):
        print("\t" + nodeType)
    elif(nodeType == "Call"):
        print("\t" + nodeType)


if __name__== "__main__":
    main(sys.argv, len(sys.argv))