#!/bin/sh
i=0
while [ $i -ne 30 ]
do
    GPSMODE="`/usr/bin/gpspipe -w 2>/dev/null | /usr/bin/head -10 | /bin/grep TPV | /bin/sed -r 's/.*"mode":(.).*/\1/' | /usr/bin/head -1 `"
    GPSDATE="`/usr/bin/gpspipe -w 2>/dev/null | /usr/bin/head -10  | /bin/grep TPV | /bin/sed -r 's/.*"time":"([^"]*)".*/\1/' | /usr/bin/head -1`"
    TPV="`/usr/bin/gpspipe -w 2>/dev/null | /usr/bin/head -10 | /bin/grep TPV | /usr/bin/head -1 `"
    echo $GPSMODE,$GPSDATE

    if [ $GPSMODE -eq 3 -a -n "$GPSDATE" ] ; then
        break
    fi
    echo "GPS NONE ${i}"
    sleep 10
    i=`expr $i + 1`
done

sudo /bin/date -s "$GPSDATE"
