#!/usr/bin/env python3
# triviant.py — Triviant in de terminal (Books, easy) met OpenTDB

import requests
import random
import html

API_URL = "https://opentdb.com/api.php"
CATEGORY_ID = 10          # 10 = Entertainment: Books
DIFFICULTY = "easy"       # easy | medium | hard

# 3. get_question(): haalt 1 vraag op en returnt (vraag, juist_antwoord, antwoordenlijst)
def get_question(qtype=None):
    """
    Haal 1 vraag op uit de OpenTDB API voor categorie Books (easy).
    Retourneert: (question:str, correct_answer:str, answers:list[str])
    """
    params = {
        "amount": 1,
        "category": CATEGORY_ID,
        "difficulty": DIFFICULTY,
    }
    if qtype in ("multiple", "boolean"):
        params["type"] = qtype

    try:
        resp = requests.get(API_URL, params=params, timeout=15)
        data = resp.json()  # -> dict
    except Exception as e:
        print(f"[FOUT] API-probleem: {e}")
        return None, None, None

    if data.get("response_code") != 0 or not data.get("results"):
        return None, None, None

    item = data["results"][0]

    # 1) Ruwe waarden
    question_raw = item.get("question", "")
    correct_raw = item.get("correct_answer", "")
    incorrect_raw = item.get("incorrect_answers", [])

    # 2) HTML-codes wegwerken (kan ook met replace, maar html.unescape pakt alles)
    question = html.unescape(question_raw)
    correct = html.unescape(correct_raw)
    answers = [html.unescape(a) for a in incorrect_raw] + [correct]

    # 3) Antwoordenlijst sorteren/shufflen
    if item.get("type") == "boolean":
        # Zorg dat True vóór False komt; tip: reverse=True
        answers = list(set(a.capitalize() for a in answers))
        answers.sort(reverse=True)  # -> ["True","False"]
    else:
        random.shuffle(answers)     # juiste antwoord op willekeurige plek

    return question, correct, answers

# 4. print_question(): toont de vraag + antwoordenlijst
def print_question(question, answers):
    print("\n" + "=" * 60)
    # fallback replace voor geval er nog HTML restjes zijn
    qsafe = (question.replace("&quot;", "\"")
                     .replace("&#039;", "'")
                     .replace("&amp;", "&"))
    print(qsafe)
    print("-" * 60)
    for i, ans in enumerate(answers, start=1):
        safe = (ans.replace("&quot;", "\"")
                   .replace("&#039;", "'")
                   .replace("&amp;", "&"))
        print(f"{i}. {safe}")
    print()

# 5. ask_player_answer(): valideer invoer 1..len(answers)
def ask_player_answer(n_options):
    while True:
        choice = input(f"Kies je antwoord (1-{n_options}) of 'q' om te stoppen: ").strip().lower()
        if choice == 'q':
            return 'q'
        if choice.isdigit():
            num = int(choice)
            if 1 <= num <= n_options:
                return num
        print("Ongeldige invoer. Probeer opnieuw.")

# 6. check_answer(): True/False
def check_answer(player_answer_index, correct_answer, answers):
    return answers[player_answer_index - 1] == correct_answer

# 7. Eén speelbeurt: vraag ophalen, printen, antwoord vragen, controleren
def play_turn(player_name="Speler", qtype_choice="mix"):
    """
    Speelt één vraag voor één speler.
    qtype_choice: 'multiple', 'boolean' of 'mix'
    Retourneert punten (int) of None als gestopt.
    """
    qtype = random.choice(["multiple", "boolean"]) if qtype_choice == "mix" else qtype_choice

    question, correct, answers = get_question(qtype=qtype)
    if not question or not correct or not answers:
        print("[Waarschuwing] Kon geen volledige vraag ophalen. Probeer opnieuw…")
        return play_turn(player_name, qtype_choice)

    print(f"\nBeurt van: {player_name}")
    print_question(question, answers)

    choice = ask_player_answer(len(answers))
    if choice == 'q':
        return None

    good = check_answer(choice, correct, answers)
    if good:
        print("✅ Goed!")
        return 2 if len(answers) == 4 else 1  # multiple=2 punten, boolean=1 punt
    else:
        print(f"❌ Fout. Het juiste antwoord was: {answers.index(correct)+1}. {correct}")
        return 0

# 7b. Complete spel-loop voor single of multi
def play_game(multiplayer=False, qtype_choice="mix"):
    if not multiplayer:
        name = input("Wat is je naam? ").strip() or "Speler"
        points_total = 0
        return_code = True
        while return_code:
            pts = play_turn(name, qtype_choice)
            if pts is None:
                print("Spel gestopt.")
                break
            points_total += pts
            print(f"Huidige score: {points_total}")
            again = input("Nog een keer spelen? (ja/nee): ").strip().lower()
            return_code = again in ("ja", "j", "yes", "y")
        print(f"\nBedankt voor het spelen, {name}! Eindscore: {points_total}")
    else:
        # Bonus: meerdere spelers + score dictionary
        while True:
            try:
                n = int(input("Hoeveel spelers? (2-8): ").strip())
                if 2 <= n <= 8:
                    break
            except ValueError:
                pass
            print("Voer een getal in tussen 2 en 8.")

        scores = {}
        for i in range(1, n + 1):
            pname = input(f"Naam speler {i}: ").strip() or f"Speler{i}"
            while pname in scores:
                pname = input("Naam al gebruikt, kies een andere: ").strip() or f"Speler{i}"
            scores[pname] = 0

        names = list(scores.keys())
        keep_playing = True
        while keep_playing:
            for pname in names:
                pts = play_turn(pname, qtype_choice)
                if pts is None:
                    keep_playing = False
                    break
                scores[pname] += pts
                print(f"Score {pname}: {scores[pname]}")
                print("-" * 40)

            if not keep_playing:
                break

            print("\nScores na deze ronde:")
            for pname in sorted(scores):
                print(f" - {pname}: {scores[pname]}")

            again = input("Nog een ronde spelen? (ja/nee): ").strip().lower()
            keep_playing = again in ("ja", "j", "yes", "y")

        print("\nEindscores:")
        for pname, sc in sorted(scores.items(), key=lambda kv: (-kv[1], kv[0].lower())):
            print(f" - {pname}: {sc}")
        if scores:
            top = max(scores.values())
            winners = [p for p, s in scores.items() if s == top]
            if len(winners) == 1:
                print(f"\n🏆 Winnaar: {winners[0]} met {top} punten! Gefeliciteerd!")
            else:
                print(f"\n🤝 Gedeelde winst voor: {', '.join(winners)} met {top} punten!")
        print("Bedankt voor het spelen!")

# 8. main(): welkom, play_again-loop
def main():
    print("=== Welkom bij Triviant — Books (easy) ===")
    print("Vragen komen uit OpenTDB categorie 'Books' (10), difficulty 'easy'.\n")

    # Vraagmodus
    mode = ""
    while mode not in ("1", "2"):
        print("Kies modus: [1] Singleplayer  [2] Multiplayer (bonus)")
        mode = input("Maak een keuze (1/2): ").strip()

    # Vraagtype
    qsel = ""
    while qsel not in ("1", "2", "3"):
        print("Vraagtype: [1] Alleen multiple choice  [2] Alleen True/False  [3] Mix")
        qsel = input("Maak een keuze (1/2/3): ").strip()
    qtype_choice = {"1": "multiple", "2": "boolean", "3": "mix"}[qsel]

    play_game(multiplayer=(mode == "2"), qtype_choice=qtype_choice)

if __name__ == "__main__":
    main()
