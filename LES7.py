import requests

url = "https://pokeapi.co/api/v2/pokemon/pikachu"

response = requests.get(url)

if response.status_code == 200:
    print("Succes! Data ontvangen:")
    data = response.json()
    print(f"Naam: {data['name']}")
    print(f"Hoogte: {data['height']}")
    print(f"Gewicht: {data['weight']}")
else:
    print("Er is iets misgegaan:", response.status_code)
