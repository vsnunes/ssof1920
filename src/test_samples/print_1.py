a = source(a)
b = a
c = 1
#aqui falha mas não é grave porque o sink de fora iria apenas reportar uma informação que já tinha sido reportada no sink de dentro
print(sink(sink(b), c))