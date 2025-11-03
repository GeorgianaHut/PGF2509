# import requests
#
# url = "https://pokeapi.co/api/v2/pokemon/pikachu"
#
# response = requests.get(url)
#
# if response.status_code == 200:
#     print("Succes! Data ontvangen:")
#     data = response.json()
#     print(f"Naam: {data['name']}")
#     print(f"Hoogte: {data['height']}")
#     print(f"Gewicht: {data['weight']}")
# else:
#     print("Er is iets misgegaan:", response.status_code)

# Opdracht: Euro naar Dollar Converter met API
import requests

# Gebruik de Frankfurter API (gratis en zonder API key)
url = "https://api.frankfurter.app/latest?from=RON&to=EUR"
response = requests.get(url)
data = response.json()

# Controleer of het gelukt is
if response.status_code == 200 and "rates" in data:
    rate = data["rates"]["EUR"]
    print(f"Huidige RON/EUR koers: {rate}")

    # Vraag een bedrag in lei
    lei = float(input("Voer een bedrag in lei in: "))
    euro = lei * rate
    print(f"{lei} lei is gelijk aan {euro:.2f} euro.")
else:
    print("Er is iets misgegaan met de API-aanvraag:", response.status_code)
    print(data)
