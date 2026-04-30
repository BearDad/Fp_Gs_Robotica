# Version with while loop
# def main():
#     count = 0
#     while True:
#         if count < 100:
#             count += 1
#             if count % 3 == 0 and count % 5 == 0:
#                 print("FizzBuzz")
#             elif count % 3 == 0:
#                 print("Fizz")
#             elif count % 5 == 0:
#                 print("Buzz")
#             else:
#                 print(count)
#         else:
#             break

# Version with for loop
def main():
    for i in range(1, 101):
        if i % 3 == 0 and i % 5 == 0:
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
        else:
            print(i)


if __name__ == "__main__":
    main()
