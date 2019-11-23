a = source()
b = sanitizer3(sanitizer2(a))
if a:
    b = sanitizer(a)

sink(b)