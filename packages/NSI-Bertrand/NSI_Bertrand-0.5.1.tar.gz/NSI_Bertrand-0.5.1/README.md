# Outils pour l'enseignement NSI

## Installation

    pip install --upgrade Bertrand_NSI

# Outils

## Fonctions de tri

    >>> from Bertrand_NSI.tri import tri
    >>> tri.bulles([1, 23, 2, 4, 15])
    [1, 2, 4, 15, 23]

## Blackjack

Correction du jeu de blackjack pour l'aide aux élèves.

    >>> from Bertrand_NSI.blackjack import Player
    >>> p = Player(1)
    >>> print(p)
    <Player 1: []>
