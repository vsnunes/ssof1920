#!/usr/bin/python3
import glob, os, json
from collections import Counter

TEST_SAMPLE_FOLDER = "test_samples"

results = {}

print("=== Tester ===")
os.chdir("test_samples")

file_list = glob.glob("*.py")

print("Found {} test(s)!".format(len(file_list)))

for file in file_list:
    filename = file[:file.index(".")]
    file_json = filename + ".json"
    config = "simple.conf"
    output = filename + ".out.json"
    expected = filename + ".out"

    #print("Preparing for testing: ", file)
    #print("Loading configuration: ", config)
    #print("Loading expected output: ", expected)

    if not os.path.isfile(file_json):
        os.system("astexport -p <" + file + " > " + file_json)

    os.system("../tool " + file_json + " " + config +  " > /dev/null")

    if not os.path.isfile(output):
        result = "FAILED: No output provided!"
    else:
        with open(output, 'r') as output_file:
            out = output_file.read()
            json_output = json.loads(out)

        with open(expected, 'r') as expected_file:
            exp = expected_file.read()
            json_expected = json.loads(exp)

        result = ""
        
        if len(json_output) != len(json_expected):
            result += "WRONG:\n\tExpected {} vulnerability(s) but got {} vulnerability(s)\n".format(len(json_expected), len(json_output))
        else:

            for i in range(0, len(json_expected)):

                if Counter(json_output[i]['sources']) == Counter(json_expected[i]['sources']):
                    result += "SUCCESS: {}-Sources OK!\n".format(i)
                else:
                    result += "WRONG:\n\tExpected {}-Sources: {} but got {}\n".format(i, json_expected[i]['sources'], json_output[i]['sources'])
                
                if Counter(json_output[i]['sanitizers']) == Counter(json_expected[i]['sanitizers']):
                    result += "SUCCESS: {}-Sanitizers OK!\n".format(i)
                else:
                    result += "WRONG:\n\tExpected {}-Sanitizers: {} but got {}\n".format(i, json_expected[i]['sanitizers'], json_output[i]['sanitizers'])
                
                if Counter(json_output[i]['sinks']) == Counter(json_expected[i]['sinks']):
                    result += "SUCCESS: {}-Sinks OK!\n".format(i)
                else:
                    result += "WRONG:\n\tExpected {}-Sinks: {} but got {}\n".format(i, json_expected[i]['sinks'], json_output[i]['sinks'])
    
    print(filename + "\t\n" + result)
    results[filename] = result