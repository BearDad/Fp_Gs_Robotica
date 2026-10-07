print("Farolitas")
try:
    lumens = float(input("Cuantos lumenes hay fuera? "))
except ValueError:
    print("Error: not a number")
    exit()

if lumens >= 300.0:
    print("OFF")
else:
    print("ON")

