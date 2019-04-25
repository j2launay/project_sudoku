#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 13:42:22 2019

@author: julien

"""
import curses
import threading
import _thread
import random
import time
from multiprocessing import Pool, Process
import os

exitFlag = 0

class Block(object):
    """Place un block 3x3 dans le champs."""

    def __init__(self):
        self._block = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    def __setitem__(self, point, value):
        """Enregistre la valeur, regarde si la valeur n'est pas déjà dans le block."""
        
        if abs(self._block[point[1] + 3 * point[0]]) == abs(value):
            self._block[point[1] + 3 * point[0]] = value
            return
        if value != 0 and (value in self._block or -value in self._block):
            raise ValueError("Block contient déjà %d" % value)
        self._block[point[1] + 3 * point[0]] = value

    def __getitem__(self, point):
        """Retourne la valeur au point donnée."""
        return self._block[point[1] + 3 * point[0]]


class Sudoku(object):

    def __init__(self):
        self._field = [Block() for i in range(9)]
        # Valeurs cachées utilisées dans solve() et populate()
        self._values = list(range(1, 10))
        self._points = [(x, y) for y in range(9) for x in range(9)]
    
    def __enter__(self, *a):
        return self
    
    def __exit__(self, *a):
        return self

    def clear(self):
        """Redemarre le jeu à zéro."""
        for b in self._field:
            b._block = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    def candidates(self, point):
        """Retourne tous les candidats au point (x, y)."""
        candidates = set()
        previous = self[point]
        for i in self._values:
            try:
                self[point] = i
            except ValueError:
                pass
            else:
                candidates.add(i)
        self[point] = previous
        return candidates

    def populate(self, n=36):
        """ 
        n est l'indice pour le nombre de valeurs à l'intérieur de la grille.
        Vide le Sudoku, lance le solver en utilisant des valeurs aléatoires et
        retire autant de valeur que possible.
        """
        # Mise en place du hasard dans la liste des points et des valeurs
        random.shuffle(self._points)
        random.shuffle(self._values)
        self.clear()
        self.solve()

        for point in self._points:
            if self[point] == 0:
                continue
            val = self[point]
            for v in self.candidates(point):
                if v == val:
                    continue
                self[point] = v
                if self.solve(True):
                    self[point] = val
                    break
            else:
                if (81 - sum(b._block.count(0) for b in self._field) < n):
                    self[point] = val
                    break
                self[point] = 0

        for point in self._points:
            self[point] *= -1

    def __str__(self):
        """Représente le Sudoku comme une chaine de caractères (Pour le but de debugging)."""
        s = ""
        for y in range(9):
            for x in range(9):
                s += '%d ' % self[x, y]
                if (x + 1) % 3 == 0:
                    s += " "
            s += "\n"
            if (y + 1) % 3 == 0:
                s += "\n"
        return s.strip()

    def __getitem__(self, p):
        pb = (p[0] // 3, p[1] // 3)
        block = self._field[pb[1] + 3 * pb[0]]

        return block[p[0] % 3, p[1] % 3]

    def __setitem__(self, p, val):
        if self[p] < 0 and val >= 0:
            raise ValueError("Valeur au point n %s est pre-definit" % str(p))
        if val != 0:
            for i in range(9):
                if i != p[1] and abs(self[p[0], i]) == abs(val):
                    raise ValueError("Déjà dans la colonne: %d" % val)
                if i != p[0] and abs(self[i, p[1]]) == abs(val):
                    raise ValueError("Déjà dans la ligne: %d" % val)

        pb = (p[0] // 3, p[1] // 3)
        block = self._field[pb[1] + 3 * pb[0]]

        block[p[0] % 3, p[1] % 3] = val

    def is_solved(self):
        return all(0 not in self._field[i]._block for i in range(0, 9))

    def solve(self, reset=False):
        """
        Résoud le Sudoku.
        Si 'reset' est True, regarde juste si le Sudoku est rempli.
        Retourne ensuite le sudoku identique par rapport à avant l'appel.
        """
        if self.is_solved():
            return True

        field = None
        for x in range(9):
            if field is not None:
                break
            for y in range(9):
                if self[x, y] == 0:
                    field = (x, y)
                    break

        if field is None:
            return True

        for new in self._values:
            try:
                self[field] = new
            except ValueError:
                continue
            else:
                if self.solve(reset):
                    if reset:
                        self[field] = 0
                    return True
                else:
                    self[field] = 0

def parallel_solve(threadName):
    """Fonction appelée pour la résolution du sudoku en parallèle."""
    for i in range(10):
        with Sudoku() as sudo:
            sudo.populate(32)
            sudo.solve()
        
class myThread (threading.Thread):
   """Classe initialisant un thread avec son nom et id du thread."""
   def __init__(self, threadID, name):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      
   def run(self):
      print ("Starting " + self.name)
      parallel_solve(self.name)
      print ("Exiting " + self.name)


if __name__ == '__main__':
    file_parallel = open("time_parallel_16threads_32", "w")
    start = time.time()
    
    # Création des nouveaux threads
    thread1 = myThread(1, "Thread-1")
    thread2 = myThread(2, "Thread-2")
    thread3 = myThread(3, "Thread-3")
    thread4 = myThread(4, "Thread-4")
    thread5 = myThread(5, "Thread-5")
    thread6 = myThread(6, "Thread-6")
    thread7 = myThread(7, "Thread-7")
    thread8 = myThread(8, "Thread-8")
    thread9 = myThread(9, "Thread-9")
    thread10 = myThread(10, "Thread-10")
    thread11 = myThread(11, "Thread-11")
    thread12 = myThread(12, "Thread-12")
    thread13 = myThread(13, "Thread-13")
    thread14 = myThread(14, "Thread-14")
    thread15 = myThread(15, "Thread-15")
    thread16 = myThread(16, "Thread-16")
        
    # Lancement des nouveaux threads
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()
    thread6.start()
    thread7.start()
    thread8.start()
    thread9.start()
    thread10.start()
    thread11.start()
    thread12.start()
    thread13.start()
    thread14.start()
    thread15.start()
    thread16.start()
    
    # Attente que tous les threads aient terminés
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    thread5.join()
    thread6.join()
    thread7.join()
    thread8.join()
    thread9.join()
    thread10.join()
    thread11.join()
    thread12.join()
    thread13.join()
    thread14.join()
    thread15.join()
    thread16.join()
    
    end = time.time()
    texte = str( end - start)
    print ("temps requis : ", texte)
    print ("Fin du thread principal")
    file_parallel.write(texte)
    file_parallel.close()
    
    # Démarrage de l'algorithme séquentiel pour la résolution de la grille.
    file_sequentiel = open("time_sequentiel_160_32", "w")
    start = time.time()
    for i in range (160):
        with Sudoku() as sudo:
            sudo.populate(32)
            sudo.solve()
    end = time.time()
    texte = str(end - start)
    print ("temps requis : ", texte)
    file_sequentiel.write(texte)
    file_sequentiel.close()
    