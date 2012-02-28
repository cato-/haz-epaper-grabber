#!/bin/bash
# haz_epaper_grabber.sh 0.1
# Download the E-Paper for HAZ (Hannoversche Allgemeine Zeitung) with an account
# and merge everything into a single pdf.
#
# "THE BEER-WARE LICENSE" (Revision 42):
# <hazepaper -at- robertweidlich -dot- de> wrote this file. As long as you
# retain this notice you can do whatever you want with this stuff. If we meet 
# some day, and you think this stuff is worth it, you can buy me a beer in return.

USAGE="Usage: `basename $0` -u user -p password [-q] [-d dumpdir]"
QUIET=0
DATADIR="."

while getopts hu:p:d:q OPT; do
  case "$OPT" in
    h)
      echo $USAGE
      exit 0
      ;;
    u)
      USERNAME=$OPTARG
      ;;
    p)
      PASSWORD=$OPTARG
      ;;
    q)
      QUIET=1
      ;;
    d)
      DATADIR=$OPTARG
      ;;
    \?)
      echo $USAGE >&2
      exit 1
      ;;
  esac
done

[ $QUIET -eq 0 ] && ECHO=echo || ECHO=:

function check_result() {
    if [ $? -eq 0 ]; then
      [ $QUIET -eq 0 ] && echo "done."
    else
      echo "failed. Exiting."
      exit 2
    fi
}

YEAR="$(date +%y)"
MONTH="$(date +%m)"
DAY="$(date +%d)"

$ECHO "Getting todays ($DAY.$MONTH.$YEAR) newspaper for $USERNAME"

BASENAME=http://epaper12.niedersachsen.com/
LOGINURL=$BASENAME/epaper/index_HAZ_neu.html
DOWNLOADURL="${BASENAME}epaper/getfiles_complete.php?zeitung=HAZ&ekZeitung=&book=&Y=${YEAR}&M=${MONTH}&D=${DAY}"
COOKIEFILE=cookie.txt
ZIPFILE=file.zip

$ECHO -n "Fetching login cookie ... "
curl -sS --data-urlencode beilage="" \
         --data-urlencode username="$USERNAME" \
         --data-urlencode passwort="$PASSWORD" \
         --data-urlencode version="pdf" \
         --data-urlencode Ok="Ok" \
         --cookie-jar "$COOKIEFILE" "$LOGINURL" -o /dev/null
check_result

$ECHO -n "Getting e-paper ...       "
curl -sS -L -b "$COOKIEFILE" "$DOWNLOADURL" > "$ZIPFILE"
check_result

$ECHO -n "Unzipping e-paper ...     "
unzip -q "$ZIPFILE"
check_result

FOLDER=$(unzip -l "$ZIPFILE"|sed 's,^.* ,,;'|grep '/'|cut -d '/' -f1|sort|uniq)
RESULT="HAZ-$YEAR$MONTH$DAY.pdf"

$ECHO -n "Merging e-paper ...       "
pdfjam -q -o "$RESULT" "$FOLDER"/*.pdf
check_result

$ECHO -n "Archiving e-paper ...     "
if [ ! -e "$DATADIR" ]; then mkdir "$DATADIR"; fi
mv "$RESULT" "$DATADIR"
check_result

$ECHO -n "Cleaning up ...           "
rm -r "$FOLDER" "$ZIPFILE" "$COOKIEFILE"
check_result

