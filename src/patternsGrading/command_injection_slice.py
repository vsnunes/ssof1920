fileName = input("Input to cat -> ")
command = "cat {}".format(quote(fileName))
call(command, shell=True)