#!/usr/bin/env python

import io
from sys import stdout, stdin, stderr

import clevercsv
import chardet

"""
Script permettant de lire un csv sur l'entrée standard, et de retourner sur la sortie un CSV RFC-4180 en UTF-8.
Le script detecte l'encoding (chardet) et le dialect (clevercsv).

Exemples : 

  Utilisation basique :
  cat moncsvpourri.csv | python standardize_csv.py > moncsvclean.csv
  
  Pour afficher seulement les caractéristiques du csv (encoding et dialect) :
  cat moncsvpourri.csv | python standardize_csv.py > /dev/null

  Utilisation avec ogr2ogr :
  cat moncsvpourri.csv | python standardize_csv.py | ogr2ogr target.gpkg CSV:/vsistdin/
  
TODO : I/O fichiers 
TODO2 : Générer un csvt ?
"""

def standardize():
    def rename_duplicates(lst):
        """
        Pour renommer les entêtes identiques (col, col_1, col_2, etc.)
        """
        seen = {}
        new_lst = []
        for item in lst:
            if item not in seen:
                seen[item] = 1
                new_lst.append(item)
            else:
                seen[item] += 1
                new_lst.append(f"{item}_{seen[item] - 1}")
        return new_lst


    input_data = stdin.buffer.read() # read as binary
    encoding_detection = chardet.detect(input_data)
    encoding, confidence = encoding_detection['encoding'], round(encoding_detection['confidence'],2)

    print('Encoding : {} (with {} confidence)'.format(encoding, confidence), file=stderr)

    csvfile = io.StringIO(input_data.decode(encoding))
    dialect = clevercsv.Sniffer().sniff(csvfile.read())
    print('Dialect : {}'.format(dialect.to_dict()), file=stderr)

    csvfile.seek(0)
    reader = clevercsv.reader(csvfile, dialect)
    rows = reader

    ## Write new file
    writer = clevercsv.write.writer(stdout, encoding='utf8') #Print to stdout
    header = True
    for row in rows :
        if header :
            row = rename_duplicates(row)
        header = False
        writer.writerow(row)

if __name__ == '__main__':
    standardize()


