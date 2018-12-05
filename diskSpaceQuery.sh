server=
port=
disk=`df -hP {disk} | awk '{print $5}' |tail -1|sed 's/%$//g'`
cluster=

echo "disks.$cluster.$(cat /etc/hostname) $disk `date +%s`"

echo "disks.$cluster.$(cat /etc/hostname) $disk `date +%s`" | nc $server $port
