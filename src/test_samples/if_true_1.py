a = source()
if True:
    b = source2()
    c = a + b

sink(c)

#Provavelmente nao aconteceria num caso real. C nao esta inicializado antes do if.
#Não faria sentido gramaticalmente: dentro do if uma variavel pode levar atribuição, 
#mas depois fora pode ser invocada diretamente sem prévia atribuição. 
#É como se no mesmo programa uma variável pudesse tomar, dependendo do branch, 
#simultaneamente uma atribuição ou então ser um ponto de entrada (input())