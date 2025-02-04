#!/bin/awk -f
# This program counts the number of IP interfaces in the switch
BEGIN { count = 0;};
$2 ~ /[0-9]+\./ {count++};
END {print "Number of IP Interface :", count;}

