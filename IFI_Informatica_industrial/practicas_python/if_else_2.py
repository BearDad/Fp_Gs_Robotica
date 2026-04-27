print("Riego de las plantitas\n\n")
try:
    quant = float(input("Cantidad de agua: "))
except ValueError:
    print("Error: not a number")
    exit()

if quant >= 0 and quant <= 20:
    print("Continuo")
elif quant > 20 and quant <= 50:
    print("Peligro")
elif quant > 50 and quant <= 100:
    print("Off")



