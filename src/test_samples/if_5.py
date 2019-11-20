a = source()
b = 1
if a:
    a = 2
    if b:
        a = source3()
    elif c:
        a = source4()
    else:
        a = source5()
else:
    a = source2()
c = sink(a)
sink(c)