#!/bin/bash

# SMSD_PID=`pidof gammu-smsd`
SMSD_PID=$(sv s gammu-smsd-{{ gammu_phoneid }} |awk {'print $4+0'})
if [ -z "$SMSD_PID" ] ; then
  gammu -c /etc/gammu.d/gammu-{{ gammu_phoneid }}.conf $@
else
  tty=$(lsof |grep -E "gammu-sms\s+$SMSD_PID\s+.*/dev/tty*"|awk {'print $NF'})
  kill -SIGUSR1 $SMSD_PID
  while test "$(fuser $ttyfuser $tty 2> /dev/null|xargs)" = $SMSD_PID
  do
    sleep 1
  done
  sleep 1
  gammu -c /etc/gammu.d/gammu-{{ gammu_phoneid }}.conf $@
  kill -SIGUSR2 $SMSD_PID
  while test "$(fuser $ttyfuser $tty 2> /dev/null|xargs)" != $SMSD_PID
  do
    sleep 1
  done
  sleep 1
fi
