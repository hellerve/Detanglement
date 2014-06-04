#!/bin/sh
# Detects which OS and if it is Linux then it will detect which Linux Distribution.

OS=`uname -s`
REV=`uname -r`
MACH=`uname -m`

GetVersionFromFile(){
        VERSION=`cat $1 | tr "\n" ' ' | sed s/.*VERSION.*=\ // `
}

if [ "${OS}" = "SunOS" ] ; then
        OS=Solaris
        ARCH=`uname -p`
        OSSTR="${OS} ${REV}(${ARCH} `uname -v`)"
elif [ "${OS}" = "Darwin" ] ; then
        OS=Darwin
elif [ "${OS}" = "AIX" ] ; then
        OSSTR="${OS} `oslevel` (`oslevel -r`)"
elif [ "${OS}" = "Linux" ] ; then
        KERNEL=`uname -r`
        if [ -f /etc/redhat-release ] ; then
                DIST='RedHat'
                PSEUDONAME=`cat /etc/redhat-release | sed s/.*\(// | sed s/\)//`
                REV=`cat /etc/redhat-release | sed s/.*release\ // | sed s/\ .*//`
        elif [ -f /etc/SuSE-release ] ; then
                DIST=`cat /etc/SuSE-release | tr "\n" ' '| sed s/VERSION.*//`
                REV=`cat /etc/SuSE-release | tr "\n" ' ' | sed s/.*=\ //`
        elif [ -f /etc/mandrake-release ] ; then
                DIST='Mandrake'
                PSEUDONAME=`cat /etc/mandrake-release | sed s/.*\(// | sed s/\)//`
                REV=`cat /etc/mandrake-release | sed s/.*release\ // | sed s/\ .*//`
        elif [ -f /etc/debian_version ] ; then
                DIST="Debian `cat /etc/debian_version`"
                REV=""
        elif [ -f /etc/arch-release ]; then
                DIST="Arch" 
                REV=`cat /etc/arch-relese | tr "\n" ' ' | sed s/.*=//`
        elif [ -f /etc/alpine-release ]; then
                echo="Alpine"
                PSEUDONAME=`cat /etc/alpine-release | sed s/.*\(// | sed s/\)//`
                REV=`cat /etc/alpine-release | sed s/.*release\ // | sed s/\ .*//`
        fi
        if [ -f /etc/UnitedLinux-release ] ; then
                DIST="${DIST}[`cat /etc/UnitedLinux-release | tr "\n" ' ' | sed s/VERSION.*//`]"
        fi

        OSSTR="${OS} ${DIST} ${REV}(${PSEUDONAME} ${KERNEL} ${MACH})"

fi

echo "Determined OS: ${OSSTR}"

case $OSSTR in
    *"Arch"*) return1=sudo pacman -S python-pip python-pyqt5
              return2=sudo pip install pygeoip geopy twitterapi wbpy
    *"Debian"*)return1=sudo apt-get install python3-pip python3-qt5
               return2=sudo python3-pip install pygeoip geopy twitterapi wbpy
    *"Darwin"*)return1=brew install PyQt5 #Assuming pip is already there, as it is installed with homebrews python3 formula
               return2=sudo pip3 install pygeoip geopy twitterapi wbpy
    *) echo Im not sure about that distro. Rather do it manually.
       exit 1;;
esac
if [ ${return1} != 0 ] ; then
    echo "The installation of pip or pyqt5 failed with status ${return1}. Cowardly exiting."
    exit 1;;
elif [ ${return2} != 0 ] ; then
    echo "The installation of pip or pyqt5 failed with status ${return1}. Cowardly exiting."
    exit 1;;
else
    echo "The depednencies should work fine now."
    exit 0;;
fir
