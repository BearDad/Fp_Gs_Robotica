pan = 3.49
pan_dia = 200
pan_viejo = 100


def calcular_pan(pan_dia, pan_viejo):
    total = (pan * pan_dia) + (pan_viejo * pan * 0.6)
    return total


total = calcular_pan(pan_dia, pan_viejo)
print(f"En total tendra que pagar {total}€")
