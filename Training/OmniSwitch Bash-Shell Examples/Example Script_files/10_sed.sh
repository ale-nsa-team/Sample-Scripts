show vlan | sed 's/[[:blank:]]//g'
show vlan | sed 's/[[:blank:]]/-/g'
show vlan | awk '{print $1,$7}' | sed 's/^/@NewLine: /g' 

