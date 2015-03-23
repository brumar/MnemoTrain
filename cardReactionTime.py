# -*- coding: cp1252 -*-
import pygame as pg
import mnemy.PygameExperiment as pe
import mnemy.MOL as MOL

if __name__ == "__main__":
    #try:
    system = raw_input('images to train [PAP, PA(default), P or A] : ')
    if(system==''):
        system="PA"
    e = pe.PygameExperiment(system=system)
    D = MOL.Deck(3, show_as_text=False)
    e.add_collection(D, True)
    e.freeDisplay(1)
    e.ending()


