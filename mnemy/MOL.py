
import random as rd

cards = ["AH", "KH", "QH", "JH", "TH", "9H", "8H", "7H",\
          "6H", "5H", "4H", "3H", "2H", "AS", "KS", "QS", "JS", "TS", "9S", \
          "8S", "7S", "6S", "5S", "4S", "3S", "2S", "AD", "KD", "QD", "JD", \
          "TD", "9D", "8D", "7D", "6D", "5D", "4D", "3D", "2D", "AC", "KC", \
          "QC", "JC", "TC", "9C", "8C", "7C", "6C", "5C", "4C", "3C", "2C"]
fileCards = "cartes"
fileType = ".bmp"

recall_keys_cards = {97: 'Q', 99: 'C', 100: 'D', 104: 'H', 106: "J", \
         107: 'K', 113: "A", 115: "S", 116: "T", 48: "T", 49 : "1",\
         50: "2", 51: "3", 52: "4", 53:"5", 54:"6", 55:"7",\
         56:"8", 57:"9"}

recall_keys_numbers = {48: "0", 49 : "1",\
         50: "2", 51: "3", 52: "4", 53:"5", 54:"6", 55:"7",\
         56:"8", 57:"9"}

recall_keys_default = {97: 'Q', 99: 'C', 100: 'D', 104: 'H', 106: "J", \
         107: 'K', 113: "A", 115: "S", 116: "T", 48: "0", 49 : "1",\
         50: "2", 51: "3", 52: "4", 53:"5", 54:"6", 55:"7",\
         56:"8", 57:"9"}

class Collection():
    def __init__(self, elements, nb_display, keys = recall_keys_default, txt = True, pictures = None):
        self.elements = elements
        self.nb_elem = len(elements)
        self.nb_display = nb_display
        self.index = 0
        self.recall_keys = keys
        self.isText = txt
        self.pictures = pictures

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= self.nb_elem-1:
            self.index = 0
            raise StopIteration
        self.index = self.index +1
        return self.elements[self.index]

    def isCollection(self):
        return True


class Deck(Collection):
    def __init__(self, nb_display, show_as_text = True):
        deck = list(cards)
        rd.shuffle(deck)
        picts = None
        if not(show_as_text):
            picts = []
            for card in deck:
                pict = fileCards+"/"+card+fileType
                picts.append(pict)
        Collection.__init__(self, deck, nb_display, recall_keys_cards, show_as_text, picts)


        







