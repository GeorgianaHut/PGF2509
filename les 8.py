TODO = "TODO.txt"

def read_file():
    with open(TODO, "r") as file:
        print(file.readlines())


def write_file():
    new_todo = input("\nVoer een nieuwe TODO in: ").strip()
    if new_todo == "":
        print("Lege TODO wordt niet toegevoegd.")
        return
    with open(TODO, "a") as file:
        file.write(new_todo + "\n")
    print(f'TODO toegevoegd: "{new_todo}"')

def delete_file():
    pass

def main():
    while True:
        print("\nTODO Applicatie")
        print("1. Bekijk TODO-lijst")
        print("2. Voeg TODO-item toe")
        print("3. Verwijder TODO-item")
        print("4. Stop")
        keuze = int(input("Maak uw keuze (1-4): ").strip())

        if keuze == 1:
            read_file()
        elif keuze == 2:
            write_file()
        elif keuze == 3:
            delete_file()
        elif keuze == 4:
            print("Je verlaat de TODO list")
            break
        else:
            print("Ongeldige keuze")


main()