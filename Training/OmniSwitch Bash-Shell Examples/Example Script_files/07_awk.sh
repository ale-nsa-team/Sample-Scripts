show vlan | awk '{print $1,$7}'
show vlan | awk '$6 < 1600 {print $1,$7}'
show vlan | awk '$1 ~ /1[[:digit:]]{2}/ {print "VLAN ID between 100-199: ", $1,"Name:", $7}'
show vlan | awk '$3 = "Ena" && $6 > 1400 {print "Enabled VLANs with MTU greater than 1400:", $7}'
show vlan | awk '$6 == "1500" && $7 == "OSPF"'
show ip interface | awk '$2 ~ /10\.[[:digit:]]{2}\./ {print $1,$2}'
show vlan | awk 'BEGIN{OFS=";";ORS="\n"}{print $1,$2,$3,$4,$5,$6}'
show log swlog | awk '$4>"17:34:00" && $4<"17:38:00" {print $0}'

