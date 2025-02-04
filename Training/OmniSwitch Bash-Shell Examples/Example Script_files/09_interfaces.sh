show interfaces status | awk '{print $1}'
arr=($(show interfaces status | grep [0-9] | awk '{print $1}'));
for i in ${arr[@]};do echo $i;show interfaces $i | grep MAC;done
