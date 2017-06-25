BEWARE: UNMAINTAINED PROJECT
============================

Since I am no longer subscribed to HAZ, there will be no updates to this. Since 19th of July 2017 the script does not work anymore due to changes of the ePaper section.

Madsack E-Paper Grabber
=======================

Small script intended to run from cron to fetch todays newspaper. The current
version is a rewrite in python as the epaper website changed. It was designed
to download the HAZ (Hannoversche Allgemeine Zeitung), but might be used for
fetching other newspapers from Madsack (Aller-Zeitung, Dresdner Neueste Nachrichten,
Gelnhäuser Neue Zeitung, Göttinger Tageblatt/ Eichsfelder Tageblatt, Leipziger Volks­zeitung
Lübecker Nachrichten, Märkische Allgemeine Zeitung, Naumburger Tageblatt, Neue Presse,
Ostsee-Zeitung, Peiner Allgemeine Zeitung, Schaum­burger Nachrichte, Wolfsburger Allgemeine Zeitung)
as well, you might have to change ``baseurl`` in the python script. Please report 
which newspapers work.

Installation
------------

    mkdir madsack madsack/zeitung
    cd madsack
    git clone https://github.com/cato-/haz-epaper-grabber.git
    cd haz-epaper-grabber
    ./madsack-epaper-grabber.sh -u [user] -p [password] -a

Select the code (first word on each line) for the newspaper you would like to fetch and add something like the following
to your crontab:

    00 01 * * 1-6 $PATHTOYOURDIR/madsack/haz-epaper-grabber/madsack_epaper_grabber.sh -u [user] -p [password] -d $PATHTOYOURDIR/madsack/zeitung -i [code] [code2]

Licence
-------

"THE BEER-WARE LICENSE" (Revision 42):

<hazepaper -at- robertweidlich -dot- de> wrote this file. As long as you
retain this notice you can do whatever you want with this stuff. If we meet
some day, and you think this stuff is worth it, you can buy me a beer in
return.

