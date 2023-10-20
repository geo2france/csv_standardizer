# csv_standardizer

Un script utilisant [CleverCSV](https://github.com/alan-turing-institute/CleverCSV) permettant
de normaliser un CSV en UTF-8 avec le dialecte [RFC-4180](https://datatracker.ietf.org/doc/html/rfc4180) (séparateur virgule, double quote, etc.).
Les caractéristique du CSV en entrée sont détectés automatiquement.

## Installation

```bash
git clone https://github.com/geo2france/csv_standardizer.git
cd csv_standardizer
pyton3 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Utilisation

Le script utilise l'entrée et la sortie standard, ce qui autorise le chainage (_pipe_) avec d'autres commandes (écrire le CSV sur le disque, exporter vers une base de données, etc.).


## Exemples

```bash
cat moncsvoriginal.csv | python3 standardize_csv.py > moncsvpropre.csv
cat moncsvoriginal.csv | python3 standardize_csv.py > /dev/null # Pour afficher uniquement les informations sur le CSV (dialecte et encodage détectés)
cat moncsvoriginal.csv | python3 standardize_csv.py | ogr2ogr PG:service=mabase -nln monschema.moncsvpropre CSV:/vsistdin/ # Préparer le CSV et l'importer dans une base postgres
cat moncsvoriginal.csv | python3 standardize_csv.py | ogrinfo CSV:/vsistdin/ -al -so # Pour lister les colonnes
```
