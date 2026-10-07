

print("Inicializando sistema...")
try:
    temp = float(input("Ingresa la temperatura actual: "))
except ValueError:
    print("is u stupid? ")
    exit()

if temp >= 300.0:
    print("is u in the sun?")
elif temp >= 50.0:
    print("que estas en el desierto?")
elif temp >= 30.0:
    print("La temperatura es muy alta")
elif temp <= 20.0:
    print("La temperatura es muy baja")
else:
    print("Tamos CHILL de cojones")

