#!/usr/bin/python3
##############################################
#
# Name: mediaplayer.py
#
# Author: Peter Christen
#
# Version: 1.0
# 
# Date: 10.09.2017 - V1.0
#       01.02.2020 - V1.1 configparser ergänzt
#
# Purpose: Startet omxplayer
#
##############################################

import RPi.GPIO as gp
import time,os,threading,stat,argparse,configparser

#Argparse Eingabe prüfen 
parser = argparse.ArgumentParser(description='Mediaplayer')
parser.add_argument('-v', action='store_true', help="Gibt Statusmeldungen aus")
args = parser.parse_args()

#Config-File einlesen
config = configparser.ConfigParser()
config.read('/etc/mediaplayer.cfg')

#Config-Daten zuordnen
med1=config['MEDIEN']['med1']
med2=config['MEDIEN']['med2']
med3=config['MEDIEN']['med3']
med4=config['MEDIEN']['med4']

#Taster den Pins zuordnen
tred=26		# Pin 37 Roter Taster
tgreen=19	# Pin 35 Grüner Taster
tyellow=13	# Pin 31 Gelber Taster
tblue=6		# Pin 33 Blauer Taster
tblack=5	# Pin 29 Schwarzer Taster
playstatus=0	# Medium läuft nicht=0, Medium läuft=1
fifopath="/tmp/omxplaxer.fifo"
verbose=0

if args.v:
   verbose=1
 
#GPIO initialisieren
gp.setmode(gp.BCM)
gp.setwarnings(False)

#Ausgänge initialisieren
for pin in (tred,tgreen,tyellow,tblue,tblack):
   gp.setup(pin, gp.IN, pull_up_down=gp.PUD_DOWN)

#fifo erstellen
if not os.path.exists(fifopath):
   os.mkfifo(fifopath)

#Funktionen
def write_fifo(x):
   fifo=open(fifopath, "w")
   fifo.write(x)
   #print (x)
   fifo.close()
   time.sleep(0.5)

def play():
   kommando="omxplayer /home/pi/Videos/Video_Notepad.mp4 <"+fifopath
   #print(kommando)
   os.popen(kommando)
   
#Medium abfragen und starten
#pdb.set_trace()
if verbose==1: print ("Bitte die rote Taste")
while True:
   if gp.input(tred)==True and playstatus==0:
      playstatus=1
      if verbose==1: print ("Film ab")
      t = threading.Thread(target=play)
      t.start()
      time.sleep(0.5)
      write_fifo("p")
      write_fifo("p")
   elif gp.input(tred)==True and playstatus==1:
      write_fifo("i")
      if verbose==1: print("Von Anfang")
   elif gp.input(tgreen)==True and playstatus==1:
      write_fifo("+")
      if verbose==1: print("Lauter")
   elif gp.input(tyellow)==True and playstatus==1:
      write_fifo("-")
      if verbose==1: print("Leiser")
   elif gp.input(tblue)==True and playstatus==1:
      write_fifo("p")
      if verbose==1: print("Pause")
   elif gp.input(tblack)==True:
      if verbose==1: print("Ende")
      write_fifo("q")
      break

#Alles wieder aufräumen
gp.cleanup()
