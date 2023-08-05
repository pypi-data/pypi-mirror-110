#!/usr/bin/env python3
# -*- coding: utf-8 -*
from tkinter import *
import os
veri = Tk()
veri.title('Kyak2-systemd-installer')
veri.geometry('400x225')
veri.configure(bg='#252726')
veri.maxsize(400,225)
veri.minsize(400,225)

Label(text="Welcome to my app it needs Xterm terminal software\nand sudo permission to copy files needed locations\nTwo times password is asked for Menu Launcher\nOne time for Terminal Shortcut\nEnter password wait 5 sec and close.",fg='#00FA9A',bg='#252726').place(x=0,y=0)


def deger1():
    os.system("xterm -hold -e sudo cp Kyak2-systemd.py /usr/share/applications/")
    os.system("xterm -hold -e sudo cp Kyak2-systemd.desktop /usr/share/applications/")
def deger2():
    os.system("xterm -hold -e sudo cp Kyak2-systemd.py /usr/bin/")
def deger3():
    os.system("xterm -hold -e sudo rm /usr/share/applications/Kyak2-systemd.py")
    os.system("xterm -hold -e sudo rm /usr/share/applications/Kyak2-systemd.desktop")
def deger4():
    os.system("xterm -hold -e sudo rm /usr/bin/Kyak2-systemd.py")
    	
buton = Button(veri,text='Menu Launcher',fg='crimson',bg='#252726',command=deger1)
buton.place(x=30, y=100)
buton2 = Button(veri,text='Terminal Shortcut',fg='crimson',bg='#252726',command=deger2)
buton2.place(x=175, y=100)
buton3 = Button(veri,text='Launcher Uninstaller',fg='crimson',bg='#252726',command=deger3)
buton3.place(x=30, y=160)
buton4 = Button(veri,text='Shortcut Uninstaller',fg='crimson',bg='#252726',command=deger4)
buton4.place(x=175, y=160)




veri.mainloop()