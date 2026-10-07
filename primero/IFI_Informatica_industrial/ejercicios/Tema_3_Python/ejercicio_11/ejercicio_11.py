money = float(input("cuanto dinero hay en la cuenta: "))

interest_rate = float(4)

years = 3
while years > 0:
    interest = money * interest_rate / 100
    total = money + interest
    print(
        f"dinero en la cuenta: {money:.2f} + interes: {interest:.2f}"
        + f" = {total:.2f}"
    )

    money += interest
    years -= 1
