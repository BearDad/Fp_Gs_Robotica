temp_deseada = int(input("Que temperatura desea? "))
temp = 10
if temp_deseada >= temp and temp_deseada <= 30:

    while temp != temp_deseada:
        print("La temperatura es", temp)
        temp += 1
    if temp == temp_deseada:
        print("Alcanzo la temperatura deseada")
        exit()
else:
    print("La temperatura esta fuera de rango")
