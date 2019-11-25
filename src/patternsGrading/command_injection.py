import subprocess
from shlex import quote

from subprocess import call

fileName = input("Input to cat -> ")
command = "cat {}".format(quote(fileName))
call(command, shell=True)