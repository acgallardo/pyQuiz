#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pyQuiz.

History:
0.1 wip
"""
import sqlite3
import os


class PyQuiz(object):
    """PyQuiz object."""

    def __init__(self):
        """Inicializa el objeto."""
        self._init_db()

    def _init_db(self):
        """Inicializa la base de datos."""
        self.db = sqlite3.connect("misdatos.db")
        self.cursor = self.db.cursor()

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS temas(
            id_tema INTEGER PRIMARY KEY AUTOINCREMENT,
            tema TEXT)
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS preguntas(
            id_pregunta INTEGER PRIMARY KEY AUTOINCREMENT,
            id_tema INTEGER NOT NULL,
            pregunta TEXT)
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS respuestas(
            id_respuesta INTEGER PRIMARY KEY AUTOINCREMENT,
            id_pregunta INTEGER NOT NULL,
            correcta INTEGER NOT NULL DEFAULT (0),
            respuesta TEXT NOT NULL)
        ''')

        self.db.commit()

        # self.carga_datos()

    # def carga_datos(self):
    #     """Carga de datos."""
    #     self.cursor.execute('''
    #         INSERT INTO temas(tema) values ("CENEC LPIC101 Tema 16")
    #     ''')
    #
    #     self.cursor.execute('''
    #         INSERT INTO preguntas(id_tema, pregunta) values (? , ?)
    # ''', (self.cursor.lastrowid, 'The first stage of the boot process is:'))
    #
    #     id_pregunta = self.cursor.lastrowid
    #
    #     self.cursor.execute('''
    #         INSERT INTO respuestas(id_pregunta, correcta, respuesta)
    #         values(?, ? , ?)
    #     ''', (id_pregunta, 0, 'The kernel phase'))
    #
    #     self.db.commit()

    def get_examen(self, preguntas):
        """Devuelve las preguntas que componen el examen/quiz."""
        self.cursor.execute('''
        SELECT * FROM preguntas ORDER BY RANDOM() LIMIT ?
        ''', (preguntas,))

        examen = self.cursor.fetchall()

        return examen

    def get_respuestas(self, idpregunta):
        """."""
        self.cursor.execute('''
            SELECT * from respuestas WHERE id_pregunta=?
        ''', (idpregunta,))

        respuetas = self.cursor.fetchall()

        return respuetas

    def __del__(self):
        """El ultimo que salga que cierre."""
        self.db.close()


class Menu(object):
    """Menu simple."""

    def __init__(self):
        """Se inicializa el menu y el obeto que proporciona la informacion."""
        self.preguntas = PyQuiz()
        self._menu_principal()

    def _menu_principal(self):
        """Menu principal."""
        exit = False
        while(exit is False):

            self.cls()

            print("\n --- Menu principal ---\n")
            print("  1   Hacer test")
            print("  2   Gestionar preguntas")
            print("  0   Salir ")
            print("\n\n")
            seleccion = int(input("[0-2]>"))

            if(seleccion == 0):
                exit = True
            elif seleccion == 1:
                exit = True
                self._menu_test()
            elif seleccion == 2:
                pass

    def _menu_test(self):

        examen = self.preguntas.get_examen(10)

        for pregunta in examen:
            print(pregunta[2])
            respuestas = self.preguntas.get_respuestas(pregunta[0])

            for counter, respuesta in enumerate(respuestas):
                print(counter)
                print(respuesta)

            print("Indique su respuesta y pulse intro")
            input(">")

    def cls(self):
        """Borrar la pantalla."""
        os.system('cls' if os.name == 'nt' else 'clear')


def main():
    """Main."""
    Menu()


if __name__ == '__main__':
    main()
