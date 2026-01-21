money = float(input("Ingrese el dinero que quiere invertir: "))

interest_rate = input("Ingrese el tipo de interés: ")
if interest_rate.endswith("%"):
    interest_rate = float(interest_rate.strip("%"))
else:
    interest_rate = float(interest_rate)

years = int(input("Ingrese el numero de años: "))

while years > 0:
    interest = money * interest_rate / 100
    money += interest
    years -= 1
