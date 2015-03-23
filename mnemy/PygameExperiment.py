# -*- coding: cp1252 -*-

"""
Created on Tue Mar 12 19:57:40 2013
Contient les fonctions permettant d'interagir avec pygame

@author: Timothée
"""

import pygame as pg
import random as rd
import time

background_color = (155, 155, 155)
text_color = (10, 10, 10)
font_instructions = "timesnewroman"
font_stimuli = "lucidaconsole"
font_size = 32
error_color = (255, 0, 0)
input_keys = {97: 'q', 98: 'b', 99: 'c', 100: 'd', 101 : 'e', \
                 102: 'f', 103: 'g', 104: 'h', 105: 'i', 106: 'j', \
                 107: 'k', 108: 'l', 59: 'm', 110: 'n', 111: 'o',\
                 112: 'p', 113: 'a', 114: 'r', 115: 's', 116: 't',\
                 117: 'u', 118: 'v', 119: 'z', 120: 'x', 121: 'y',\
                 122: 'w', 50 : 'é', 55 : 'è', 48: "0", 49 : "1",\
                 50: "2", 51: "3", 52: "4", 53:"5", 54:"6", 55:"7",\
                 56:"8", 57:"9"}

time_highlight = 500

class PygameExperiment():

    def __init__(self, filename=None, subject = "John Doe", debug = False,system="PA"):
        self.debub=debug
        self.data_file = filename
        self.subject = subject
        self.background_color = background_color
        self.text_color = text_color
        self.font_size = font_size
        self.font_instructions = font_instructions
        self.font_stimuli = font_stimuli
        #self.write(time.strftime('%d/%m/%y %H:%M',time.localtime()))
        self.starting_time = pg.time.get_ticks()
        self.input_keys = input_keys
        self.time_highlight = time_highlight
        self.collection = None
        self.rToutput=open('./rawDatas/reactionTimes.csv', 'a')#temp
        self.system=system
        self.solution=[]
        self.viewingTime=0
        #Image    indexItem    timestamp    time    item    context    extra_1    extra_2

    def pgInit(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode([0,0], pg.FULLSCREEN | pg.DOUBLEBUF)
        self.screen_w, self.screen_h = self.screen.get_size()
        self.screen_center = (self.screen_w/2, self.screen_h/2)

    def ending(self):
        self.write("Total time : " + str(pg.time.get_ticks()-self.starting_time))
        #self.data_file.close()
        pg.quit()

    def get_time(self):
        return pg.time.get_ticks() - self.starting_time

    def write(self, t, new_line=True):
        pass
##        self.data_file.write(t)
##        if new_line:
##            self.data_file.write("\n")

    def writeRt(self,trials,timeElapsed,item):

        self.rToutput.write(self.system+";"+str(trials)+";"+str(time.time())+";"+str(timeElapsed)+";"+str(item)+ ";cardsV1\n")

    def pictureToTextNotation(self,pic):
        pic=pic.replace("cartes/","")
        pic=pic.replace(".bmp","")
        return pic;

    def map_data_file(self, headers, *args):
        if type(headers).__name__ != "list":
            raise Exception("Headers are not a list")
        if len(headers) <= 0:
            raise Exception("Headers must contain at least one string")
        for h in headers:
            if type(h).__name__ != "str":
                raise Exception("All headers must be strings")
        if len(headers) != len(args):
            raise Exception("There must be as much headers as argument")
        for arg in args:
            if len(arg) != len(args[0]):
                raise Exception("All args must have the same exact length")

        nb_arg = len(args)
        nb_lines = len(args[0])
        self.write(self.make_str(headers, "\t")) #changer de file ???

        for j in range(nb_lines):
            buf = []
            for i in range(nb_arg):
                buf.append(str(args[i][j]))
            self.write(self.make_str(buf, "\t"))


    def save_proc(self):
        pg.time.wait(5)

    def wait(self, x):
        pg.time.wait(x)

    def wait_input(self, k):
    #pause tant qu'on appuie pas sur une des keys
        keys = []
        if type(k).__name__ == "int": #on veut une liste de ints
            keys.append(k)
        elif type(k).__name__== "list":
            for key in k:
                keys.append(k)

        for event in pg.event.get():
            pass
        t = True
        while t:
            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    raise Exception()
                elif event.type==pg.KEYDOWN and event.key in keys:
                    t = False
                    return event.key
            self.save_proc()

    def user_input(self): #à réécrire sous forme de "seqAction"?
        raise Exception() #cette fonction est à corriger!!
        buffer = []
        time_first_keystroke = 0
        first_keystroke = True
        nsp = False
        while True:
            self.save_proc()
            for event in pg.event.get():
                if self.debug:
                    if event.type == pg.QUIT:
                        raise Exception()
                if event.type==pg.KEYDOWN:
                    if event.key in self.input_keys:
                        if (first_keystroke):
                            first_keystroke = False
                            time_first_keystroke = pg.time.get_ticks()
                        if nsp:
                            buffer = []
                            nsp = False
                        if len(buffer)<50:
                            buffer.append(self.input_keys[event.key])
                        self.write_instruction(self.make_str(buffer))
                    elif event.key == pg.K_RETURN:
                        if buffer != []:
                            return(self.make_str(buffer), time_first_keystroke)
                    elif event.key == pg.K_BACKSPACE:
                        if nsp:
                            buffer = []
                            nsp = False
                        if len(buffer) > 0:
                            j=buffer.pop()
                        self.write_instruction(self.make_str(buffer))

                    elif event.key == pg.K_SPACE:
                        if (first_keystroke):
                            first_keystroke = False
                            time_first_keystroke = pg.time.get_ticks()#FAUX
                        if not(nsp):
                            nsp = True
                            buffer = "Ne sais plus"
                        self.write_instruction(self.make_str(buffer))

                    elif event.key == pg.K_ESCAPE:
                        pass
                        #=======================================================
                        # if _debug:
                        #     raise Exception()
                        # else:
                        #     pass
                        # #it was buggy, _debug undefined
                        #=======================================================
    def blank(self):
        self.screen.fill(self.background_color)
        pg.display.flip()

    def display_pictures(self, pics_list):
        #display pictures (horizontally)
        self.screen.fill(self.background_color)
        tot_w = 0
        max_h = 0
        big_p = []
        # 1 : all the images are loaded in a list
        for pic in pics_list:
            p = pg.image.load(pic)
            tot_w = tot_w+p.get_width()
            if p.get_height() > max_h:
                max_h = p.get_height()
            big_p.append(p)

        glob_p = pg.Surface((tot_w, max_h))
        glob_p.fill(self.background_color)
        w_act = 0
        # 2 : each images are blited
        for p in big_p:
            p_pos = (w_act, glob_p.get_height()/2 - p.get_height()/2)
            glob_p.blit(p, p_pos)
            w_act = w_act+ p.get_width() ##ICI pour + espace vide

        glob_p_pos = (self.screen_center[0] - glob_p.get_width()/2, self.screen_center[1] - glob_p.get_height()/2)
        self.screen.blit(glob_p, glob_p_pos)
        pg.display.flip()

    def write_instruction(self, text, name_font = None):
        #write instruction (vertically)
        #each element in text is written on a new line
        if name_font == None:
            name_font = self.font_instructions
        inst = []
        if type(text).__name__ == "str": #on veut une liste de string, pas une string
            inst.append(text)
        elif type(text).__name__== "list":
            for st in text:
                inst.append(st)
        else:
            raise Exception()

        self.screen.fill(self.background_color)
        myFont = pg.font.Font(pg.font.match_font(name_font), self.font_size)
        text = []
        tot_h = 0
        max_w = 0
        for st in inst:
            m = myFont.render(st, 1, self.text_color)
            tot_h = tot_h + m.get_height()
            if m.get_width() > max_w:
                max_w = m.get_width()
            text.append(m)

        glob_t = pg.Surface((max_w, tot_h))
        glob_t.fill(self.background_color)
        h_act = 0
        for t in text:
            t_pos = (glob_t.get_width()/2 - t.get_width()/2, h_act)
            glob_t.blit(t, t_pos)
            h_act = h_act + t.get_height()

        glob_t_pos = (self.screen_center[0] - glob_t.get_width()/2, self.screen_center[1] - glob_t.get_height()/2)
        self.screen.blit(glob_t, glob_t_pos)
        pg.display.flip()

    def wait_space(self):
        self.wait_input(pg.K_SPACE)

    def space_instruction(self, text, name_font = None):
        if name_font == None:
            name_font = self.font_instructions
        self.write_instruction(text, name_font)
        self.wait_space()

    def make_str(self,l, sp = ""):
        #transforme une liste de string en une seule string
        r =''
        try:
            for s in l:
                r = r+s+sp
        except TypeError:
            return ''
        return r

    def make_text_from_tab(self,t, nb_items, items_per_line, char_per_item, highlighted, on):
        assert len(t) == nb_items * char_per_item
        save = t[highlighted]
        if not(on):
            t[highlighted] = " "
        text_final = []
        text_buffer = ""

        for i in range(nb_items):
            if i>0:
                if(i%items_per_line==0): #on commence une nouvelle ligne
                    text_final.append(text_buffer)
                    text_buffer = ""
            p= i*char_per_item
            text_buffer = text_buffer + self.make_str(t[p:p+char_per_item]) + " "
        text_final.append(text_buffer)
        t[highlighted] = save
        return text_final


#________Fonctions "MOL", qui fonctionnent à l'aide d'un objet Collection

    def add_collection(self, c, describe = False):
        #vérifier que l'objet envoyé est bien une collection
        if c.isCollection():
            self.collection = c
        else:
            raise Exception("This is not a Collection")

        if describe:
            self.write(str(c.elements))


    def has_collection(self):
        return self.collection != None

    def randomPickPictures(self,numberAsked):
        pictures = self.collection.pictures
        chosenpictures=[]
        for i in range(numberAsked):
            index=rd.randint(0,len(self.collection.pictures)-1)
            chosenpictures.append(self.collection.pictures[index])
        return chosenpictures


    def freeDisplay(self,nbDisplay):
        self.pgInit()
        # nb display is now an argument
        # will work only for pictures
        textual = self.collection.isText
        toExplore = self.collection.elements
        if not(textual):
            pictures = self.collection.pictures
        c = True
        log = []
        timeLog = []
        start = pg.time.get_ticks()
        last_time = start
        trials=0
        self.write_instruction("espace to pass, q to quit", self.font_stimuli)
        while c:
            pg.display.flip()
            for event in pg.event.get():
                if event.type==pg.KEYDOWN:
                    if event.key == pg.K_RETURN :
                        pictures=self.randomPickPictures(nbDisplay)  # Pick pictures
                        self.display_pictures(pictures)
                        trials+=1
                        time=pg.time.get_ticks()- last_time
                        item=""
                        for picture in pictures:
                            item+=self.pictureToTextNotation(picture) #not really fancy but do the trick for the moment
                        self.writeRt(trials, float(time)/1000, item)
                        last_time=pg.time.get_ticks()
                    if event.key == pg.K_ESCAPE:
                        c = False
                        break

    def explore(self, can_quit = True, record = True, startPos = 1):
        self.pgInit()
        assert self.has_collection()
        nbDisplay = self.collection.nb_display
        textual = self.collection.isText == True
        toExplore = self.collection.elements
        if not(textual):
            pictures = self.collection.pictures
            for picture in pictures:
                self.solution.append(self.pictureToTextNotation(picture))
        pos = startPos
        c = True
        lastPos = int(len(toExplore)/nbDisplay)

        log = []
        timeLog = []
        for i in range(lastPos):
            timeLog.append(0)
        start = pg.time.get_ticks()
        last_time = start
        log.append(str([pos, 0]))

        while c:
            if textual:
                self.write_instruction(toExplore[(pos-1)*nbDisplay:(pos)*nbDisplay], self.font_stimuli)

            else:
                if((pos+1)*nbDisplay-1<len(pictures)):
         # handle the case of the number of cards don't fit with the system.
                    self.display_pictures(pictures[(pos-1)*nbDisplay:(pos)*nbDisplay])
                else:
                    self.display_pictures(pictures[(pos-1)*nbDisplay:])

            pg.display.flip()

            for event in pg.event.get():
                if event.type==pg.KEYDOWN:
                    if event.key == pg.K_LEFT:
                        pos -= 1
                        if pos<1:
                            pos = 1
                        else:
                            timeLog[pos] = timeLog[pos] + pg.time.get_ticks()- last_time
                            last_time = pg.time.get_ticks()
                            log.append(str([pos, last_time-start]))
                    if event.key == pg.K_RIGHT:
                        pos += 1
                        if pos>lastPos:
                            pos = lastPos
                        else:
                            timeLog[pos-2] = timeLog[pos-2] + pg.time.get_ticks()- last_time
                            last_time = pg.time.get_ticks()
                            log.append(str([pos, last_time-start]))
                    if event.key == pg.K_RETURN:
                        timeLog[pos-1] = timeLog[pos-1] + pg.time.get_ticks()- last_time
                        c = False
                    if can_quit:
                        if (event.key == pg.K_ESCAPE):
                            raise Exception()
            self.viewingTime=pg.time.get_ticks()-start
            self.save_proc()

        total_time = pg.time.get_ticks()-start
        if record:
            self.write("Phase d'exploration")
            self.write("Log des changements de position :"+str(log))
            self.write("Temps totaux d'exploration :")
            for i in range(len(timeLog)):
                self.write("Position "+str(i+1)+": "+str(timeLog[i]))
            self.write("__________\n")
        return timeLog, total_time

    def recall_input(self, items_per_line, record = True):
        #A faire : mettre des symboles pique/coeur, etc
        #return tab
        assert self.has_collection()
        toRecall = self.collection.elements
        nb_items = len(toRecall)
        nChar = len(toRecall[0])
        inser = False
        highlighted = 0
        tab = []
        c = 0
        for i in range(nb_items * nChar):
            tab.append("-")

        start = pg.time.get_ticks()
        while True:
            self.save_proc()
            for event in pg.event.get():
                if self.debug:
                    if event.type == pg.QUIT:
                        raise Exception()
                if event.type==pg.KEYDOWN:
                    #touche correspondant à rappel
                    if event.key in self.collection.recall_keys:
                        if inser:
                            tab.insert(highlighted, self.collection.recall_keys[event.key])
                            tab.pop()
                        else:
                            tab[highlighted]= self.collection.recall_keys[event.key]
                            highlighted += 1
                            if highlighted >= len(tab):
                                highlighted = len(tab)-1

                    #espace = "je ne sais pas"
                    elif event.key == pg.K_SPACE:
                        posDeb = highlighted
                        if highlighted % nChar != 0:
                            posDeb = posDeb - (highlighted % nChar)
                        for i in range(nChar):
                            tab[posDeb+i] = "X"
                        highlighted = posDeb+nChar
                        if highlighted >= len(tab):
                            highlighted = len(tab)-1

                    #touches pour naviguer
                    elif event.key == pg.K_LEFT:
                        highlighted -= 1
                        if highlighted < 0 :
                            highlighted = 0
                    elif event.key == pg.K_RIGHT:
                        highlighted += 1
                        if highlighted >= len(tab) :
                            highlighted = len(tab)-1
                    elif event.key == pg.K_UP:
                        highlighted -= items_per_line * nChar
                        if highlighted < 0:
                            highlighted += items_per_line * nChar
                    elif event.key == pg.K_DOWN:
                        highlighted += items_per_line * nChar
                        if highlighted >= len(tab) :
                            highlighted -= items_per_line * nChar

                    #touches utilitaires
                    elif event.key == pg.K_RETURN:
                        total_time = pg.time.get_ticks()-start
                        return tab, total_time
                    elif event.key == pg.K_BACKSPACE:
                        highlighted -= 1
                        if highlighted < 0 :
                            highlighted = 0
                        else:
                            tab[highlighted]="-"
                    elif event.key == pg.K_INSERT:
                        if inser:
                            inser = False
                        else:
                            inser = True
                    elif event.key == pg.K_ESCAPE:
                        if self.debug:
                            raise Exception()
                        else:
                            pass

            if ((pg.time.get_ticks() - start)%(self.time_highlight*2))>self.time_highlight :
                on = True
            else:
                on = False
            self.write_instruction(self.make_text_from_tab(tab, nb_items, items_per_line, nChar, highlighted, on), self.font_stimuli)

    def recall_input_mouse(self, pics_list):
        assert self.has_collection()

        self.screen.fill(self.background_color)

##        test_pict = pics_list[0]
##        p_w = test_pict.get_width()
##        p_h = test_pict.get_height()
        ptest = pg.image.load(pics_list[0])
        start_h = 200
        h_dec = ptest.get_height()
        nb_pics_per_line = 13
        start_w = 20
        w_dec = ptest.get_width()

        focus = 0
        p = []
        for i in range(len(pics_list)):
            picture = pg.image.load(pics_list[i])
            pos_h = start_h + int(i/nb_pics_per_line)*h_dec
            pos_w = start_w + (i%nb_pics_per_line)*w_dec
            p.append(Pict(picture, pos_w, pos_h, i, False))

        start = pg.time.get_ticks()
        drag = False
        c = True
        mouse_last_pos = pg.mouse.get_pos()
        while c:
            self.save_proc()
            #display
            self.screen.fill(self.background_color)
            for P in p:
                self.screen.blit(P.pict, P.pos)
            pg.display.flip()

            for event in pg.event.get():
                if self.debug:
                    if event.type == pg.QUIT:
                        raise Exception()
                if event.type==pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        raise Exception()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        clicked = None
                        max_focus = 0
##                        for P in p:
##                            if P.is_clicked(#...:
##                                if P.order >
##                                clicked.append(P)
##                        if
##                            drag = True
##                            mouse_last_pos = pygame.mouse.get_pos()
##                            dragged = ...
                if event.type == pg.MOUSEBUTTONUP:
                    if event.button == 1:
                        drag = False

            if drag:
                mouse_pos = pg.mouse.get_pos()
                 #modifier dragged..
                 #Traitements
                mouse_last_pos = mouse_pos

    def count_errors(self, answers):
        assert self.has_collection()
        toLearn = self.collection.elements
        nb_char_per_item = len(toLearn[0])
        assert len(answers) == nb_char_per_item*len(toLearn)
        e = 0
        p = []
        for i in range(len(toLearn)):
            if self.make_str(answers[i*nb_char_per_item:(i+1)*nb_char_per_item])!=toLearn[i]:
                e+=1
                p.append(i)
        return e, p

    #__________A partir d'ici : EXPERIMENTATION_________________________

#_____trucs pour interagir avec des séquences
    def record(self):
        pass

    def run(self, sequence):
        for act in sequence:
            if act.isImmediate():
                act.execute()
                #pb : c'est à PygameExperiment d'exécuter les machins...
            else:
                start = pg.time.get_ticks()
                while pg.time.get_ticks() - start < act.duration:
                    self.save_proc()
#_________Autres classes________________________________________________________


class Sequence():
    #une sequence est une suite d'actions "pygame", chacune liée à un temps
    #pour gérer des suites de elif pygame.time.get_ticks() - start < _time_photo:...
    pass

class Action():
    #un des trucs faisable dans une séquence...
        #y'a des SeqAction qui attendent des inputs, d'autres qui ne font qu'afficher...
    def __init__(self, experiment, dur, act, data):

        #dur : durée
        #disp : qu'affiche-t-on à l'écran ?
        #act : quelles actions ? input de l'user
        # act <=> "keymap" ? une liste de dico "key <=> action atomique"
        self.duration = dur
        self.act = act #!! act doit être une fonction de PygameExperiment
        self.data = data

    def execute(self):
        pass
        #self.act(data)

    def isImmediate(self):
        return self.dur == 0

    def isContinuous(self):
        return self.dur == -1

class SeqAction():
    #un des trucs faisable dans une séquence...
        #y'a des SeqAction qui attendent des inputs, d'autres qui ne font qu'afficher...
    def __init__(self, e, dur):

        #dur : durée
        #disp : qu'affiche-t-on à l'écran ?
        #act : quelles actions ? input de l'user
        # act <=> "keymap" ? une liste de dico "key <=> action atomique"
        self.duration = dur
        self.experiment = e
        self.act = None
        self.disp = None

    def isReady(self):
        if (self.act == None) or (self.disp == None) :
            return False
        else:
            return True

    def set_disp(self, ):
        pass

    def goNext(self):
        pass
    def goPrec(self):
        pass


    def execute(self):
        pass
       # self.act(data)

    def isImmediate(self):
        return self.dur == 0

    def isContinuous(self):
        return self.dur == -1

class Act():
    pass
class Display(Act):
    pass

class Pict():
    def __init__(self, picture, pos_w, pos_h, order, placed):
        self.pict = picture
        self.w = picture.get_width()
        self.h = picture.get_height()
        self.x = pos_w
        self.y = pos_h
        self.pos = (self.x,self.y)
        self.order = order
        self.placed = placed

    def is_clicked(self,x, y):
        if x>self.x and y>self.y:
            if x<self.x+self.w and y<self.y+self.h:
                return True
        return False


#_______________________________________________________
##
##class Chrono():
##    def __init__(self, pos = (0,0), run = True, hide = True):
##        self.start = pg.time.get_ticks()
##        self.pos = pos
##        self.running = run
##        self.hide = hide
##        self.timeLog = []
##
##    def t(self):
##        return pg.time.get_ticks
##
##    def get_time(self):
##        return self.start - self.t() #ATTENTION PROBLEME
##    #AVEC LES STOP TIMES...
##
##    def display(self, ...):
##        text = "00:00:00"
##        return self.pos
##
##    def move(self, newPosition):
##        self.pos = newPosition
##
##    def stop(self):
##        self.stopTime = pg.time.get_ticks()
##        self.running = False
##



