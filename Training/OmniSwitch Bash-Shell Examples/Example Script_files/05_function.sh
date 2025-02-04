function createipinterface () 
{ for ((i=100;i<=130;i++)) ;
do ip interface "VL$i" address 10.10.$(($i-100)).1/24 vlan $i;
echo "ip interface VL$i created.";
done; }

function removeipinterface () 
{ for ((i=100;i<=130;i++)) ;
do no ip interface "VL$i";
echo "ip interface VL$i removed.";
done; }

taguplink () 
{ 
    arr=($(show vlan | grep [0-9] | awk '{print $1}'));
    for i in ${arr[@]};
    do
        vlan $i members port $1 tagged;
    done
}


