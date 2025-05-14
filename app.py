from flask import Flask, render_template, request
import csv

app = Flask(__name__)

# Funkcia na načítanie IBAN zoznamu zo súboru CSV
def load_iban_list():
    iban_list = {}
    with open("ucty_utf8.csv", "r", encoding="cp1250") as f:  # ← zmena tu
        csv_reader = csv.reader(f, delimiter=';')
        next(csv_reader)  # Preskočíme hlavičku
        for row in csv_reader:
            if len(row) < 3:
                continue  # Preskočí neúplné riadky
            iban = row[0].strip().replace(" ", "")  # Odstráni medzery
            description = row[1].strip()
            note = row[2].strip()
            iban_list[iban] = {'description': description, 'note': note}
    return iban_list


iban_list = load_iban_list()

@app.route('/')
def home():
    return render_template('form.html')

@app.route('/check', methods=['POST'])
def check_iban():
    ibans = request.form['ibans'].split('\n')  # Získame IBANy z formulára, každý IBAN je v novom riadku
    results = []
    
    # Pre každý zadaný IBAN skontrolujeme, či je v zozname
    for iban in ibans:
        iban = iban.strip().replace(" ", "")  # Odstránime medzery z IBANu
        if iban in iban_list:
            result = f"IBAN: {iban} nájdený! Popis: {iban_list[iban]['description']}, Poznámka: {iban_list[iban]['note']}"
        else:
            result = f"IBAN: {iban} nie je v zozname."
        results.append(result)
    
    return render_template('results.html', results=results)

if __name__ == "__main__":
    app.run(debug=True)
