##############################################
#
# Name: INSTALL_mediaplayer_nb.bash
#
# Author: Peter Christen
#
# Version: 1.0
# 
# Date: 14.02.2020 - V1.0
#
# Purpose: Installiert die Mediaplayer App für die Schweizerische Nationalbibliothek
#
# Info: Mit der Option -d kann der Mediaplayer wieder gelöscht werden
#
##############################################

#Variablen
system_dir="/etc/systemd/system"
bin_dir="/usr/local/bin"
etc_dir="/etc"
video_dir="/home/pi/Videos"
bild_dir="/home/pi/Bilder"

#Verzeichnisse prüfen
if [ -d $system_dir ]
then
   echo "Verzeichnis: $system_dir ist ok"
else
   echo "Fehler: Verzeichnis: $system_dir existiert nicht"
   echo "Verwendet dieses Linux systemctl?"
   exit 1
fi

for verzeichnis in $video_dir $bild_dir $bin_dir
do
   if [ -d $verzeichnis ]
   then
      echo "Verzeichnis: $verzeichnis ist ok"
   else
      mkdir -p $verzeichnis
      chown pi $verzeichnis
      echo "Verzeichnis: $verzeichnis wurde erstellt"
   fi
done

if [ $1 ]
then
   if [ $1 = "-d" ]
   then
      echo "Loesche Mediaplayer"
      rm $bin_dir/mediaplayer_nb.py
      rm $bin_dir/mediaplayer_modul_nb.so
      rm $etc_dir/mediaplayer_nb.cfg
      rm $system_dir/mediaplayer_nb.service
      echo "Mediaplayer gelöscht"
      exit
   fi
fi

#Kopiere die Files
echo "Kopiere Files an die richtige Stelle"
cp mediaplayer_nb.py $bin_dir
cp mediaplayer_modul_nb.so $bin_dir
cp mediaplayer_nb.cfg $etc_dir
cp mediaplayer_nb.service $system_dir
cp Testfilm_cssgmbh.mp4 $video_dir
cp StartBild1.jpeg $bild_dir
chmod 755 $bin_dir/mediaplayer_nb.py
chmod 755 $bin_dir/mediaplayer_modul_nb.so

#Setze Boot auf multi-user.target
echo "Setze Boot auf multi-user.target"
systemctl set-default multi-user.target
systemctl enable mediaplayer_nb

#omxplaxer und joystick installieren
echo "Installiere Packages"
apt-get -y install omxplayer joystick fbi sqlite3
if [ $? -eq 0 ]
then
   echo "Installation ist abgeschlossen. Zum Testen bitte Rebooten"
else
   echo "Fehler: Nicht alle Packages konnten installiert werden"
fi
