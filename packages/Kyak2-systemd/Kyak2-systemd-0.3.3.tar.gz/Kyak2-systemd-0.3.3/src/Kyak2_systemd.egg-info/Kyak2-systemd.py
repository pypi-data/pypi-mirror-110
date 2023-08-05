#!/usr/bin/env python3
# -*- coding: utf-8 -*
from tkinter import *
import os
veri = Tk()
veri.title('Kyak2-systemd')
veri.geometry('85x230')
veri.configure(bg='#252726')
veri.maxsize(85,230)
veri.minsize(85,230)


def deger1():
    os.system("systemctl suspend")
    os.system("xscreensaver-command -l")
def deger2():
	os.system("xscreensaver-command -l")
def deger3():
	os.system("systemctl reboot")
def deger4():
	os.system("systemctl poweroff")
def deger5():
    os.system("openbox --exit")	
buton = Button(veri,text='Suspend',fg='#F0E68C',bg='#252726',command=deger1)
buton.place(x=0, y=50)
buton2 = Button(veri,text='Lock',fg='#C0C0C0',bg='#252726',command=deger2)
buton2.place(x=0, y=0)
buton3 = Button(veri,text='Reboot',fg='#00FA9A',bg='#252726',command=deger3)
buton3.place(x=0, y=100)
buton4 = Button(veri,text='Poweroff',fg='#B22222',bg='#252726',command=deger4)
buton4.place(x=0, y=150)
buton5 = Button(veri,text='Log-Out',fg='crimson',bg='#252726',command=deger5)
buton5.place(x=0, y=200)



veri.mainloop()
