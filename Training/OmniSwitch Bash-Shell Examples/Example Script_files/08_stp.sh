show vlan | grep [0-9] | awk '{print $1}'
arr=($(show vlan | grep [0-9] | awk '{print $1}'));
for i in ${arr[@]};do show spantree vlan $i | grep age;done

