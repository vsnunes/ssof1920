#!/usr/bin/python3
import glob, os, json
from collections import Counter

TEST_SAMPLE_FOLDER = "test_samples"

results = {}

print("=== Tester ===")
os.chdir("test_samples")

file_list = glob.glob("*.py")

number_of_tests = len(file_list)
generic = {"output": 0, "vuln": 0, "comp": 0}
success = {"sources" : 0, "sanitizers": 0, "sinks": 0}
failed  = {"sources" : 0, "sanitizers": 0, "sinks": 0}
wrong   = {"sources" : 0, "sanitizers": 0, "sinks": 0}
passed  = 0

print("Found {} test(s)!".format(number_of_tests))

for file in file_list:
    sources_ok = False
    sanitizers_ok = False
    sinks_ok = False
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

    #try:
    if not os.path.isfile(output):
        result = "FAILED: No output provided!"
        generic['output'] += 1
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
            generic['vuln'] += 1
        else:

            for i in range(0, len(json_expected)):
                #try:
                if Counter(json_output[i]['source']) == Counter(json_expected[i]['source']):
                    result += "SUCCESS: {}-Sources OK!\n".format(i)
                    success['sources'] += 1
                    sources_ok = True
                else:
                    result += "WRONG:\n\tExpected {}-Sources: {} but got {}\n".format(i, json_expected[i]['source'], json_output[i]['source'])
                    wrong['sources'] += 1
                    sources_ok = False
                #except Exception:
                #    failed['sources'] += 1

                #try:
                if Counter(json_output[i]['sanitizer']) == Counter(json_expected[i]['sanitizer']):
                    result += "SUCCESS: {}-Sanitizers OK!\n".format(i)
                    success['sanitizers'] += 1
                    sanitizers_ok = True
                else:
                    result += "WRONG:\n\tExpected {}-Sanitizers: {} but got {}\n".format(i, json_expected[i]['sanitizer'], json_output[i]['sanitizer'])
                    wrong['sanitizers'] += 1
                    sanitizers_ok = False
                #except Exception:
                #    failed['sanitizers'] += 1
                
                #try:
                if json_output[i]['sink'] == json_expected[i]['sink']:
                    result += "SUCCESS: {}-Sinks OK!\n".format(i)
                    success['sinks'] += 1
                    sinks_ok = True
                else:
                    result += "WRONG:\n\tExpected {}-Sinks: {} but got {}\n".format(i, json_expected[i]['sink'], json_output[i]['sink'])
                    wrong['sinks'] += 1
                    sinks_ok = False
                
                #except Exception:
                #    failed['sinks'] += 1

            if sources_ok and sanitizers_ok and sinks_ok:
                passed += 1
    
    print(filename + "\t\n" + result)
    results[filename] = result
    #except Exception:
    #    generic['comp'] += 1

print("============== Summary ==============")
print("Executed {} test(s)!".format(number_of_tests))
if generic['comp'] > 0:
    print("Program crashed: {}".format(generic['comp']))
if generic['output'] > 0:
    print("No output was provided: {}".format(generic['output']))
if generic['vuln'] > 0:
    print("Different len(vulnerabilities) were given: {}".format(generic['vuln']))
print("Passed with distintion: {}".format(passed))
print("Success:\n\tSources: {}\n\tSanitizers: {}\n\tSinks: {}".format(success['sources'], success['sanitizers'], success['sinks']))
print("Wrong:\n\tSources: {}\n\tSanitizers: {}\n\tSinks: {}".format(wrong['sources'], wrong['sanitizers'], wrong['sinks']))
print("Failed:\n\tSources: {}\n\tSanitizers: {}\n\tSinks: {}".format(failed['sources'], failed['sanitizers'], failed['sinks']))
print(" ")
print("Overall score: ({}/{}) {}".format(passed, number_of_tests, (passed / number_of_tests)))