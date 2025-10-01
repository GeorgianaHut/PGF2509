# Les3 - Pizza Lijst Oefening

# stap 1: maak een lijst met toppings
toppings = ["salami", "kaas", "tomaat", "ananas", "banaan"]

# stap 2: laat verschillende items uit de lijst zien
print("De eerste topping is:", toppings[0])
print("De derde topping is:", toppings[2])
print("De laatste topping is:", toppings[-1])
print("Alle toppings op je pizza:", toppings)

# stap 3: gebruiker mag een extra topping toevoegen
extra = input("Welke topping wil je toevoegen? ")
toppings.append(extra)
print("Nieuwe lijst met toppings:", toppings)

# stap 4: gebruiker mag een topping verwijderen
remove = input("Welke topping vind je niet lekker? ")

if remove in toppings:
    toppings.remove(remove)
    print("Na verwijderen:", toppings)
else:
    print(remove, "zit niet in de lijst.")
