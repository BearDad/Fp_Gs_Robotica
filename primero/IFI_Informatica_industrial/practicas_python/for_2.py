herramientas = ["Alicate", "Polímetro", "Pelacables", "Destornillador", "Tubo"]
for h in herramientas:
    print("En el almacén hay:", h)

placas = [24.5, 23.8, 24.1, 19.5, 24.2]
for voltaje in placas:
    if voltaje < 20:
        print("El voltaje es", voltaje, "- ¡ALERTA! Panel defectuoso.")
    else:
        print("El voltaje es", voltaje, "- Panel correcto.")
