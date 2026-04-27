def main():
    print("Que materiales vas a comprar: ")
    material =   input("material 1: ")
    material_2 = input("material 2: ")
    material_3 = input("material 3: ")
    material_4 = input("material 4: ")
    material_5 = input("material 5: ")
    material_6 = input("material 6: ")
    material_7 = input("material 7: ")
    material_8 = input("material 8: ")
    material_9 = input("material 9: ")
    material_10 = input("material 10: ")
 
    # materiales = [material, material_2, material_3, material_4, material_5, material_6, material_7, material_8, material_9, material_10]
    # for i in materiales:
    #     print(f"vas a comprar {i}" )

    print(f"Vas a comprar {material}, {material_2}, {material_3}, {material_4}, {material_5}, {material_6}, {material_7}, {material_8}, {material_9}, {material_10}")

    x = input("¿Quieres continuar?\n")
    if type(x) == str :
        if x == "s" or x == "S" or x == "si" or x == "Si":
            print("continuamos")








if __name__ == "__main__":
    main()
