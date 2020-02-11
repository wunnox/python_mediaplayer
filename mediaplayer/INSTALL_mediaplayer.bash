##############################################
#
# Name: INSTALL_mediaplayer.bash
#
# Author: Peter Christen
#
# Version: 1.0
# 
# Date: 10.09.2017 - V1.0
#
# Purpose: Installiert die Mediaplayer App
#
##############################################

#Variablen
system_dir="/etc/systemd/system"
bin_dir="/usr/local/bin"
etc_dir="/etc"

#Verzeichnisse prüfen
if [ -d $system_dir ]
then
   echo "Verzeichnis: $system_dir ist ok"
else
   echo "Fehler: Verzeichnis: $system_dir existiert nicht"
   echo "Verwendet dieses Linux systemctl?"
   exit 1
fi

if [ -d $bin_dir ]
then
   echo "Verzeichnis: $bin_dir ist ok"
else
   echo "Fehler: Verzeichnis: $bin_dir existiert nicht"
   exit 1
fi

#Kopiere die Files
echo "Kopiere Files an richtige Stelle"
cp mediaplayer.py $bin_dir
cp mediaplayer.cfg $etc_dir
cp mediaplayer.service $system_dir
chmod 755 $bin_dir/mediaplayer.py

#omxplaxer installieren
echo "Installieren omxplayer"
apt-get install omxplayer
if [ $? -eq 0 ]
then
   echo "Installation ist abgeschlossen"
else
   echo "Fehler: omxplayer konnte nicht installiert werden"
fi
