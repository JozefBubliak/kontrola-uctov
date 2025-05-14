from flask import Flask, render_template, request
import csv

app = Flask(__name__)

# Funkcia na načítanie IBAN zoznamu zo súboru CSV
def load_iban_list():
    iban_list = {}
    prefixes = {}
    with open("ucty_utf8.csv", "r", encoding="cp1250") as f:
        csv_reader = csv.reader(f, delimiter=';')
        next(csv_reader)  # Preskočíme hlavičku
        for row in csv_reader:
            if len(row) < 3:
                continue
            raw = row[0].strip().replace(" ", "")
            description = row[1].strip()
            note = row[2].strip()

            if len(raw) > 12:
                iban_list[raw] = {'description': description, 'note': note}
            elif len(raw) == 6 and raw.isdigit():
                prefixes[raw] = {'description': description, 'note': note}

    return iban_list, prefixes

iban_list, prefixes = load_iban_list()

@app.route('/')
def home():
    return render_template('form.html')

@app.route('/check', methods=['POST'])
def check_iban():
    ibans = request.form['ibans'].split('\n')
    results = []

    for iban in ibans:
        iban = iban.strip().replace(" ", "")
        if not iban:
            continue

        # Kontrola, či je IBAN úplne zhodný
        if iban in iban_list:
            result = f"✅ IBAN: {iban} nájdený! Popis: {iban_list[iban]['description']}, Poznámka: {iban_list[iban]['note']}"
        else:
            found_prefix = False
            # Kontrola predčíslia
            for prefix, data in prefixes.items():
                pattern = prefix + '8'  # Predčíslie + osmička
                if pattern in iban:
                    result = f"🟪 IBAN: {iban} obsahuje známe predčíslie {prefix}. Popis: {data['description']}, Poznámka: {data['note']}"
                    found_prefix = True
                    break
            if not found_prefix:
                result = f"❌ IBAN: {iban} nie je v zozname a neobsahuje známe predčíslie."
        results.append(result)

    return render_template('results.html', results=results)

if __name__ == "__main__":
    app.run(debug=True)
