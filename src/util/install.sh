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
elif [ "${OS}" = "Darwin" ] ; then
        OSSTR="${OS} OS X `defaults read loginwindow SystemVersionStampAsString`"
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
else
    OSSTR="NULL"
fi

echo "Determined distribution is: ${OSSTR}\n"

case $OSSTR in
    "NULL") echo Im not sure about that distro. Rather do it manually.
            exit 1;;
    *)      sudo mkdir /usr/bin/Detanglement &> /dev/null
            returnval=$?
            if [ "${returnval}" != "0" ] ; then
                echo "Cowardly exiting on failure." 
                echo "The program is likely already installed or there exists another directory called Detanglement in /usr/bin."
                exit 1
            fi
            sudo cp -r ../* /usr/bin/Detanglement
            returnval=$?
            if [ "${returnval}" != "0" ] ; then
                echo "Cowardly exiting on failure."
                exit 1
            fi
            [ ! -f ~/.bashrc ] || grep "tangle" ~/.bashrc > /dev/null || 
                echo "alias tangle=\"/usr/bin/Detanglement/src/Tangle.py\"" >> ~/.bashrc
            [ ! -f ~/.bash_profile ] || grep "tangle" ~/.bash_profile /dev/null || 
                echo "alias tangle=\"/usr/bin/Detanglement/src/Tangle.py\"" >> ~/.bash_profile
            returnval=$?
            if [ "${returnval}" != "0" ] ; then
                echo "Cowardly exiting on failure."
                exit 1
            fi
            echo "Everything seems to have worked fine, try it by opening a new terminal and typing 'tangle'."
            exit 0;;
esac
