fileToRemove = request.args.get('file')
if fileToRemove != None:
    sanitizedFile = secure_filename(fileToRemove)
    remove(sanitizedFile)
    return "removed: " + fileToRemove
return "No file removed"