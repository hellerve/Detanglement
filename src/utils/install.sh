#!/bin/sh

OS=`uname -s`
REV=`uname -r`
MACH=`uname -m`

GetVersionFromFile()
{
        VERSION=`cat $1 | tr "\n" ' ' | sed s/.*VERSION.*=\ // `
}

if [ "${OS}" = "SunOS" ] ; then
        OS=Solaris
        ARCH=`uname -p`
        OSSTR="${OS} ${REV}(${ARCH} `uname -v`)"
elif [ "${OS}" = "AIX" ] ; then
        OSSTR="${OS} `oslevel` (`oslevel -r`)"
elif [ "${OS}" = "Linux" ] ; then
        KERNEL=`uname -r`
        if [ -f /etc/redhat-release ] ; then
                DIST='RedHat'
                PSUEDONAME=`cat /etc/redhat-release | sed s/.*\(// | sed s/\)//`
                REV=`cat /etc/redhat-release | sed s/.*release\ // | sed s/\ .*//`
        elif [ -f /etc/SuSE-release ] ; then
                DIST=`cat /etc/SuSE-release | tr "\n" ' '| sed s/VERSION.*//`
                REV=`cat /etc/SuSE-release | tr "\n" ' ' | sed s/.*=\ //`
        elif [ -f /etc/mandrake-release ] ; then
                DIST='Mandrake'
                PSUEDONAME=`cat /etc/mandrake-release | sed s/.*\(// | sed s/\)//`
                REV=`cat /etc/mandrake-release | sed s/.*release\ // | sed s/\ .*//`
        elif [ -f /etc/debian_version ] ; then
                DIST="Debian `cat /etc/debian_version`"
                REV=""

        fi
        if [ -f /etc/UnitedLinux-release ] ; then
                DIST="${DIST}[`cat /etc/UnitedLinux-release | tr "\n" ' ' | sed s/VERSION.*//`]"
        fi

        OSSTR="${OS} ${DIST} ${REV}(${PSUEDONAME} ${KERNEL} ${MACH})"

fi

case $OSSTR in
    *"ARCH"*) sudo mkdir /usr/bin/Entanglement
            returnval=$?
            if [ "${returnval}" != "0" ] ; then
                echo "Cowardly exiting on failure."
                exit 1
            fi
            sudo cp -r ../* /usr/bin/Entanglement
            returnval=$?
            if [ "${returnval}" != "0" ] ; then
                echo "Cowardly exiting on failure."
                exit 1
            fi
            echo "alias tangle=\"/usr/bin/Entanglement/Tangle.py\"" >> ~/.bashrc
            returnval=$?
            if [ "${returnval}" != "0" ] ; then
                echo "Cowardly exiting on failure."
                exit 1
            fi
            echo "Everything seems to have worked fine, try it by typing 'tangle'."
            exit 0;;
    *) echo Im not sure about that distro. Rather do it manually.
       exit 1;;
esac
