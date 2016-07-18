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
        self.numero_preguntas = 10
        self.preguntas = PyQuiz()
        self._menu_principal()

    def _menu_principal(self):
        """Menu principal."""
        exit = False
        while(exit is False):

            self.cls()

            print("\n --- Menu principal ---\n")
            print("  1   Hacer test")
            print("  2   Configurar test")
            print("  0   Salir ")
            print("\n\n")

            try:
                seleccion = int(input("[0-2]>"))
            except ValueError:
                seleccion = -1

            if(seleccion == 0):
                exit = True
            elif seleccion == 1:
                exit = True
                self._menu_test()
            elif seleccion == 2:
                self._config_test()

    def _menu_test(self):

        # examen contiene sólo las peguntas
        examen = self.preguntas.get_examen(self.numero_preguntas)
        puntuacion = 0

        for pregunta in examen:
            self.cls()

            print("\n" + pregunta[2] + "\n")

            # obtenemos las preguntas de la base de datos
            respuestas = self.preguntas.get_respuestas(pregunta[0])

            # variable que almacena las respuestas correctas para compararlas
            # con las respuestas del usuario
            correctas = []

            # mostramos las preguntas en pantalla a la vez que guardamos
            # las respuestas correctas.
            for counter, respuesta in enumerate(respuestas):
                print("   " + str(counter+1) + ") " + respuesta[3])
                if(respuesta[2] == 1):
                    correctas.append(counter+1)

            # obtenemos las repuestas del usuario
            print("\nIndique su respuesta/as separadas por comas y pulse intro")
            userInput = input(">")

            # variable que contendá las respuestas válidas del usuaruio
            respuesta_usuario_clean = []

            respuestas_usuario = userInput.split(",")

            # eliminamos todo lo que no sean respuestas.
            for respuesta_usuario in respuestas_usuario:
                if respuesta_usuario.isnumeric():
                    respuesta_usuario_clean.append(int(respuesta_usuario))

            # Vemos si las respuestas del usuario son correctas.
            if set(correctas) == set(respuesta_usuario_clean):
                puntuacion += 1
                print ("\n\nCorrecto!!")
            else:
                print ("\n\nIncorrecto!!")
                print ("La(s) respuesta(s) correcta(s) son: " + " ".join(str(x) for x in correctas))

            print ("\n\nPulse intro para continuar")
            input(">")

        print("Ha acertado " + str(puntuacion))

    def _config_test(self):
        self.cls()

        print("El número de preguntas actual es " + str(self.numero_preguntas))
        try:
            preguntas = int(input("Número de preguntas que tendrá el examen: "))
        except ValueError:
            print("Entrada no válida")
            preguntas = self.numero_preguntas

        self.numero_preguntas = preguntas


    def cls(self):
        """Borrar la pantalla."""
        os.system('cls' if os.name == 'nt' else 'clear')


def main():
    """Main."""
    Menu()


if __name__ == '__main__':
    main()
