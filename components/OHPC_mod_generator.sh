#!/bin/bash
#-----------------------------------------------------------------------
# Uility to derive modules environment variable settings from shell
# script initializaion file.
#-----------------------------------------------------------------------

if [ $# -ne 1 ];then
    echo "Usage: $0 <shell-script-to-eval> args"
    exit 1
fi

# environment variables to ignore

ignoreVars="^SHLVL=|^INTEL_LICENSE_FILE=|^PWD=|^_="

inFile=$1
shift
remainArgs="$@"

if [ ! -s $inFile ];then
    echo "$inFile not available locally"
    exit 1
fi

TMPFILE=/tmp/mod_generator.$RANDOM
OUTFILE=$TMPFILE.out

cat <<EOF > $TMPFILE
#!/bin/bash
unset LD_LIBRARY_PATH
unset LIBRARY_PATH

MYPATH=\${PATH}

source $inFile "$remainArgs"

/usr/bin/printenv | sed s!:\${MYPATH}!!
EOF


chmod 700 $TMPFILE || exit 1

env -i $TMPFILE | egrep -v $ignoreVars > $OUTFILE

if [ ! -s $OUTFILE ];then
    echo "No environment variables detected"
    exit 1
fi

maxLen=0

# scan for max variable name length

for var in `cat $OUTFILE`; do 
    locLen=`echo $var | awk -F = '{print $1}'| wc -m` || exit 1

    if [ $locLen -gt $maxLen ];then
        maxLen=$locLen
    fi
done

echo " "
echo "# machine generated from $inFile"
echo " "
for var in `cat $OUTFILE`; do 
    varName=`echo $var | awk -F = '{print $1}'` || exit 1
    varDef=`echo $var | awk -F = '{print $2}'`  || exit 1

    echo $varName | grep -q PATH

    if [ $? -eq 0 ];then
        printf "%-13s %-${maxLen}s %s\n" "prepend_path" $varName $varDef
    else
        printf "%-13s %-${maxLen}s %s\n" "setenv" $varName $varDef
    fi
done

echo " "
echo "# end of machine generated"
echo " "

rm $TMPFILE
rm $OUTFILE
