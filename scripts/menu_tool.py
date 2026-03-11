while True:
    print("\n==== MY TOOL ====")
    print("1. Say Hello")
    print("2. Simple Calculator")
    print("3. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        name = input("Enter your name: ")
        print("Hello", name)

    elif choice == "2":
        a = int(input("First number: "))
        b = int(input("Second number: "))
        print("Answer:", a + b)

    elif choice == "3":
        print("Goodbye!")
        break

    else:
        print("Invalid option")
