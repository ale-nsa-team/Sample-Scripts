#!/bin/bash

#A Script to perform a factory reset on AOS 8.x switches
#Process mirrors ALE Tech Pub Article Number 000057824
#Summary AOS 8x switch can be factory reset with series of commands provided
#in Article Number 000057824 which was last modified 9/2/2021

echo "This tool will delete all configs, logs, users, etc. from the switch."
echo "Perform a FULL factory reset? (y/n)"
read answer

if [ "$answer" == "y" ]; then
  echo "Please Confirm the factory reset. This can not be undone. (y/n)"
  read confirm

  if [ "$confirm" == "y" ]; then
    echo "Waiting for 5 seconds. You can still cancel this script by typing Control C."
    sleep 5

    echo "Performing factory reset. Some file - directory not found warnings are normal and expected."
    aaa authentication default local
    cd /flash
    rm -f working/*.cfg
    rm -f certified/*.cfg
    rm -f working/*.conf
    rm -f certified/*.conf
    rm -f working/*.sav
    rm -f certified/*.sav
    rm -f working/*.md5
    rm -f certified/*.md5
    rm -f working/*.txt
    rm -f certified/*.txt
    rm -f working/*.cfg-ft
    rm -f certified/*.cfg-ft
    rm -f working/Udiag.img
    rm -f working/Urescue.img
    rm -f certified/Udiag.img
    rm -f certified/Urescue.img
    rm -f /flash/*.err
    rm -f /flash/*.cfg
    rm -f /flash/tech*
    rm -rf /flash/swlog*
    rm -f system/user*
    rm -f switch/cloud/*
    rm -f switch/dhcpd*
    rm -f switch/*.txt
    rm -f /flash/libcurl*
    rm -f /flash/agcmm*
    rm -rf working/pkg
    rm -r certified/pkg
    rm -r /flash/pmd
    swlog clear all
    echo "Factory reset complete."
    echo "You may now power down the switch or can reboot it using this command:"
    echo "reload from working no rollback-timeout"

  else
    echo "Factory reset cancelled."
  fi
else
  echo "Factory reset cancelled."
fi
