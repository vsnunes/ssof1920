from flask import Flask, request
from os import remove
from werkzeug.utils import secure_filename
app = Flask(__name__)


@app.route('/')
def vulnFunction():
    fileToRemove = request.args.get('file')
    if fileToRemove != None:
        sanitizedFile = secure_filename(fileToRemove)
        remove(sanitizedFile)
        return "removed: " fileToRemove
return "No file removed"

if __name__ == '__main__':
    app.run()