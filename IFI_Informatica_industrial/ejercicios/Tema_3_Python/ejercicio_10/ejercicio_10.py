weight_clow = 0.112
weight_doll = 0.075


def main():
    dolls_sold = int(input("How many dolls where sold? "))
    clowns_sold = int(input("How many clowns where sold? "))
    print(
        "The total weight of the packet is: ",
        weight_clow * clowns_sold + weight_doll * dolls_sold,
        "kg",
    )


if __name__ == "__main__":
    main()
