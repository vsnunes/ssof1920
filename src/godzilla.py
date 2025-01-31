#!/usr/bin/python3
import glob, os, json, sys
from collections import Counter
import subprocess
from threading import Timer

TEST_SAMPLE_FOLDER = "test_samples"

results = {}

filename = ""



def main(argv, arg):
    def display(filename, type, msg):
        if (type == "s" and displaySuccess) or (type == "f" and displayFail) or (type == "w" and displayWrong):
            results[filename] += msg + "\n"

    displaySuccess = True
    displayFail = True
    displayWrong = True

    if arg > 1:
        if argv[1] == "-onlyWF" or argv[1] == "-onlyFW":
            displaySuccess = False
            
        elif argv[1] == "-onlyW":
            displaySuccess = False
            displayFail = False

        elif argv[1] == "-onlyF":
            displaySuccess = False
            displayWrong = False

        elif argv[1] == "-onlyS":
            displayWrong = False
            displayFail = False

    print("=== Tester ===")
    os.chdir("test_samples")

    file_list = glob.glob("*.py")

    number_of_tests = len(file_list)
    generic = {"output": 0, "vuln": 0, "comp": 0, "time": 0}
    success = {"sources" : 0, "sanitizers": 0, "sinks": 0}
    failed  = {"sources" : 0, "sanitizers": 0, "sinks": 0}
    wrong   = {"sources" : 0, "sanitizers": 0, "sinks": 0}
    passed  = 0

    tests_with_fails = set()
    tests_with_wrong = set()
    tests_with_time_exceeded = set()

    print("Found {} test(s)!".format(number_of_tests))

    for file in file_list:
        sources_ok = False
        sanitizers_ok = False
        sinks_ok = False
        filename = file[:file.index(".")]
        file_json = filename + ".json"
        config = filename + ".conf"
        output = filename + ".output.json"
        expected = filename + ".out"
        results[filename] = ""
        #print("Preparing for testing: ", file)
        #print("Loading configuration: ", config)
        #print("Loading expected output: ", expected)

        if not os.path.isfile(config):
            config = "simple.conf"

        os.system("astexport -p <" + file + " > " + file_json)

        kill = lambda process: process.kill()
        FNULL = open(os.devnull, 'w')
        cmd = ['../tool', file_json, config]
        tool = subprocess.Popen(
            cmd, stdout=FNULL, stderr=subprocess.PIPE)

        my_timer = Timer(5, kill, [tool])

        try:
            my_timer.start()
            stdout, stderr = tool.communicate()
        finally:
            my_timer.cancel()

        try:
            subprocess.run(cmd, timeout=5)
        except subprocess.TimeoutExpired:
            print("FAILED: Time limit exceed for test ", filename)
            generic['time'] += 1
            tests_with_time_exceeded.add(file)
            continue

        #os.system("../tool " + file_json + " " + config +  " > /dev/null")

        try:
            if not os.path.isfile(output):
                display(filename, "f", "FAILED: No output provided!")
                generic['output'] += 1
                tests_with_fails.add(file)
            else:
                with open(output, 'r') as output_file:
                    out = output_file.read()
                    json_output = json.loads(out)

                with open(expected, 'r') as expected_file:
                    exp = expected_file.read()
                    json_expected = json.loads(exp)
                
                if len(json_output) != len(json_expected):
                    display(filename, "w", "WRONG:\n\tExpected {} vulnerability(s) but got {} vulnerability(s)".format(len(json_expected), len(json_output)))
                    generic['vuln'] += 1
                    tests_with_wrong.add(file)
                else:

                    for i in range(0, len(json_expected)):
                        try:
                            if Counter(json_output[i]['source']) == Counter(json_expected[i]['source']):
                                display(filename, "s", "SUCCESS: {}-Sources OK!".format(i))
                                success['sources'] += 1
                                sources_ok = True
                            else:
                                display(filename, "w", "WRONG:\n\tExpected {}-Sources: {} but got {}".format(i, json_expected[i]['source'], json_output[i]['source']))
                                wrong['sources'] += 1
                                sources_ok = False
                                tests_with_wrong.add(file)
                        except Exception:
                            failed['sources'] += 1

                        try:
                            if Counter(json_output[i]['sanitizer']) == Counter(json_expected[i]['sanitizer']):
                                display(filename, "s", "SUCCESS: {}-Sanitizers OK!".format(i))
                                success['sanitizers'] += 1
                                sanitizers_ok = True
                            else:
                                display(filename, "w", "WRONG:\n\tExpected {}-Sanitizers: {} but got {}".format(i, json_expected[i]['sanitizer'], json_output[i]['sanitizer']))
                                wrong['sanitizers'] += 1
                                sanitizers_ok = False
                                tests_with_wrong.add(file)
                        except Exception:
                            failed['sanitizers'] += 1

                        try:
                            if json_output[i]['sink'] == json_expected[i]['sink']:
                                display(filename, "s", "SUCCESS: {}-Sinks OK!".format(i))
                                success['sinks'] += 1
                                sinks_ok = True
                            else:
                                display(filename, "w",
                                        "WRONG:\n\tExpected {}-Sinks: {} but got {}".format(i, json_expected[i]['sink'], json_output[i]['sink']))
                                wrong['sinks'] += 1
                                sinks_ok = False
                                tests_with_wrong.add(file)

                        except Exception:
                            failed['sinks'] += 1

                    if len(json_expected) == 0:
                        sources_ok = True
                        sanitizers_ok = True
                        sinks_ok = True
                        display(filename, "s", "SUCCESS: No vulnerabilities found OK!")

                    if sources_ok and sanitizers_ok and sinks_ok:
                        passed += 1
            
            if results[filename] != "":
                print("{}\n{}".format(filename, results[filename]))
        except Exception:
            print("FAILED: No output or config file provided for test ", filename)
            generic['comp'] += 1

    print("============== Summary ==============")
    print("Executed {} test(s)!".format(number_of_tests))
    if generic['comp'] > 0:
        print("Program crashed: {}".format(generic['comp']))
    if generic['output'] > 0:
        print("No output was provided: {}".format(generic['output']))
    if generic['vuln'] > 0:
        print("Different len(vulnerabilities) were given: {}".format(generic['vuln']))
    if generic['time'] > 0:
        print("Time limit exceeded in {} test(s)!".format(generic['time']))
    print("Passed with distintion: {}".format(passed))
    print("Type     (Sources/Sanitizers/Sinks)")
    print("Success: ({:03}/{:03}/{:03})".format(success['sources'], success['sanitizers'], success['sinks']))
    print("Wrong  : ({:03}/{:03}/{:03})".format(wrong['sources'], wrong['sanitizers'], wrong['sinks']))
    print("Failed : ({:03}/{:03}/{:03})".format(failed['sources'], failed['sanitizers'], failed['sinks']))
    print(" ")
    if len(tests_with_fails) > 0:
        print("Tests with fails: {}".format(tests_with_fails))
    if len(tests_with_wrong) > 0:
        print("Tests with wrong answers: {}".format(tests_with_wrong))
    if len(tests_with_time_exceeded) > 0:
        print("Tests with time limit exceeded: {}".format(tests_with_time_exceeded))
    print(" ")
    total = success['sources'] + wrong['sources'] + failed['sources']
    print("Sources    score:\t({:03}/{:03})\t{:>7.2%}".format(success['sources'], total, (success['sources'] / total)))
    total = success['sanitizers'] + wrong['sanitizers'] + failed['sanitizers']
    print("Sanitizers score:\t({:03}/{:03})\t{:>7.2%}".format(success['sanitizers'], total, (success['sanitizers'] / total)))
    total = success['sinks'] + wrong['sinks'] + failed['sinks']
    print("Sinks      score:\t({:03}/{:03})\t{:>7.2%}".format(success['sinks'], total, (success['sinks'] / total)))
    print(format("_", "_>50"))
    print("Overall    score:\t({:03}/{:03})\t{:>7.2%}".format(passed, number_of_tests, (passed / number_of_tests)))

if __name__== "__main__":
    main(sys.argv, len(sys.argv))