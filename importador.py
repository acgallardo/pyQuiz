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


def main():
    """Main."""
    db = sqlite3.connect("misdatos.db")
    cursor = db.cursor()

    last_tema = ""
    last_tema_id = 0
    last_pregunta = ""
    last_pregunta_id = 0

    with open('datos.csv', newline='') as f:
        reader = csv.reader(f, delimiter=';', quotechar='"')
        next(reader, None)  # Nos saltamos las cabeceras
        for row in reader:
            if row[0] != last_tema:
                cursor.execute('''
                    INSERT INTO temas(tema) values (?)
                ''', (row[0],))
                last_tema = row[0]
                last_tema_id = cursor.lastrowid

            if row[1] != last_pregunta:
                cursor.execute('''
                    INSERT INTO preguntas(id_tema, pregunta) values (? , ?)
                ''', (last_tema_id, row[1]))
                last_pregunta_id = cursor.lastrowid
                last_pregunta = row[1]

            cursor.execute('''
                INSERT INTO respuestas(id_pregunta, correcta, respuesta)
                values(?, ? , ?)
            ''', (last_pregunta_id, row[2], row[3]))

            db.commit()


if __name__ == '__main__':
    main()
