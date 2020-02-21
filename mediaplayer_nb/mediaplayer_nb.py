#!/usr/bin/python3
##############################################
#
# Name: mediaplayer_nb.py
#
# Author: Peter Christen
#
# Version: 1.0
# 
# Date: 14.02.2020 - V1.0
#
# Purpose: Startet Video auf Knopfdruck
#
##############################################

import mediaplayer_modul_nb as mmnb
import time,argparse,configparser

#Argparse Eingabe prüfen 
parser = argparse.ArgumentParser(description='Mediaplayer für Schweizerische Nationalbibliothek')
parser.add_argument('-v', action='store_true', help="Gibt Statusmeldungen aus")
parser.add_argument('-t', action='store_true', help="Macht nur ein Testlauf")
args = parser.parse_args()

#Variabeln
if args.v: 
   verbose=1
else: 
   verbose=0
if args.t: 
   dotest=1
   verbose=1
else: 
   dotest=0

#Main program
mmnb.runmedia(dotest,verbose)
