#/bin/sh
while true;
do
  count=`ps -fe|grep python|grep nsfw`
  if [ "$?" != "0" ]; then
    python nsfw.py
  fi
  sleep 2
done
