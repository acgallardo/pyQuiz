#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Importador de preguntas.

Requiere que exita la base de datos ejecute una vez al menos pyquiz.
Renombre plantilla_datos.csv a datos.csv.
No deje celdas vacias.
Importar mas de una vez duplica los datos.

History:
0.1 wip
"""
import sqlite3
import csv
import os


def file_import(datos):
    db = sqlite3.connect("misdatos.db")
    cursor = db.cursor()

    last_tema = ""
    last_tema_id = 0
    last_pregunta = ""
    last_pregunta_id = 0

    tema = 0
    peso = 1
    pregunta = 2
    correcta = 3
    respuesta = 4
    tipo_pregunta = 5


    with open(datos, newline='') as f:
        reader = csv.reader(f, delimiter=';', quotechar='"')
        next(reader, None)  # Nos saltamos las cabeceras
        for row in reader:
            if row[tema] != last_tema:
                cursor.execute('''
                    INSERT INTO temas(tema) values (?)
                ''', (row[tema],))
                last_tema = row[tema]
                last_tema_id = cursor.lastrowid

            if row[pregunta] != last_pregunta:
                cursor.execute('''
                    INSERT INTO preguntas(id_tema, id_tipo_pregunta, peso, pregunta) values (? , ?, ?, ?)
                ''', (last_tema_id, row[tipo_pregunta], row[peso], row[pregunta]))
                last_pregunta_id = cursor.lastrowid
                last_pregunta = row[pregunta]

            cursor.execute('''
                INSERT INTO respuestas(id_pregunta, correcta, respuesta)
                values(?, ? , ?)
            ''', (last_pregunta_id, row[correcta], row[respuesta]))

        db.commit()


def main():
    """Main."""
    topdir = 'rawdata'
    for root, dirnames, filenames in os.walk(topdir, topdown=True, followlinks=True):
        dirnames.sort()
        filenames.sort()
        for filename in filenames:
            if filename.endswith(('.csv',)):
                print(os.path.join(root, filename))
                file_import(os.path.join(root, filename))


if __name__ == '__main__':
    main()
