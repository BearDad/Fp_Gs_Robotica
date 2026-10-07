def main():
    money = float(input("Ingrese el dinero que quiere invertir: "))
    interest_rate = input("Ingrese el tipo de interés: ")

    if interest_rate.endswith("%"):
        interest_rate = float(interest_rate.strip("%"))
    else:
        interest_rate = float(interest_rate)

    years = int(input("Ingrese el numero de años: "))
    yearly_invest = int(input("Cuanto desea invertir anualmente: "))
    tiempo = int(input("durante cuanto tiempo:"))
    invested_for = 1

    investment = money + yearly_invest * tiempo
    while years > 0:
        interest = money * interest_rate / 100
        print(
            f"Año {invested_for}°: {money:.1f} + {interest:.1f} = {money + interest:.1f}"
        )

        if invested_for <= tiempo:
            total = money + interest + yearly_invest
        else:
            total = money + interest

        money = total
        invested_for += 1
        years -= 1
        delta = money - investment
    print(
        f"{"You've invested a total of:":<30} {f'\033[31m{investment:.2f}€\033[0m':>30}\n"
        + f"{'returning you a total of:':<30} {f'\033[32m{delta:.2f}€\033[0m':>30}\n"
        + f"{'Account balance is:':<30} {f'\033[36m{money:.2f}€\033[0m':>30}\n"
    )


if __name__ == "__main__":
    main()
