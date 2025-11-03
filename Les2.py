
print("Welkom! We gaan een restaurant kiezen.")

# Laag 1: Kies keuken
keuken = input("Welke keuken wil je? (italiaans/aziatisch/grill): ")

# Laag 2: Kies budget
budget = input("Wat is je budget? (low/mid/high): ")

# Laag 3: Kies sfeer
sfeer = input("Welke sfeer zoek je? (rustig/snel/gezellig): ")

print("\nAdvies:")

if keuken == "italiaans":
    if budget == "low":
        print("Pizza Pronto – goedkoop en snel.")
    elif budget == "mid":
        print("Trattoria Roma – goede prijs en gezellig.")
    else:
        print("Il Teatro – luxe Italiaans restaurant.")

elif keuken == "aziatisch":
    if budget == "low":
        print("Noodle Bar – snelle en goedkope ramen.")
    elif budget == "mid":
        print("Sushibar – sushibar, middenklasse.")
    else:
        print(" Zen – luxe Japans diner.")

elif keuken == "grill":
    if budget == "low":
        print("Grill & Go – burgers en friet.")
    elif budget == "mid":
        print("Urban Grill – steakhouse, gezellig.")
    else:
        print("Steak & Oak – luxe grillrestaurant.")

else:
    print("Ongeldige keuze, probeer opnieuw.")
