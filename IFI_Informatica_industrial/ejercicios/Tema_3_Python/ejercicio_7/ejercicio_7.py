print("Bienvenido al programa de IMC")
print("Este programa calcula su IMC")


peso = float(input("Cual es su peso? "))
altura = float(input("Cual es su altura? "))

if altura > 3:
    altura = altura / 100


imc = peso / (altura * altura)
print("Su IMC es: ", imc)
