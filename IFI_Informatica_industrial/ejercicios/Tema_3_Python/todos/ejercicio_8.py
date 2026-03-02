n = int(input("Ingrese un numero: "))
m = int(input("Ingrese otro numero: "))
c = n // m
if c * m != n:
    r = n - (c * m)
else:
    r = 0

print("El resultado es: ", c)
if r != 0:
    print("El resto es: ", r)
