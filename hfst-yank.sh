#!/bin/bash

#ok I would like a script that can download the giellalt and make the yankerino all in one

#TODO check if the directory already exists, not essential just avoids error msgs

#TODO the webpage says to get the deb files but the pkg seems to be in the debian/ubuntu repos if you just do sudo apt install hfst???? but it doesnt mention it?
#doing now - go through learn to use grep, find where these roman numeral dates are coming from
#make it check if hfst is installed
#I think this just needs to be done by user right bc i dont want a script to invoke sudo, or do i?
#testing pushing from laptop
if ! command -v hfst-lexc 2>/dev/null; then
    echo "must install hfst by doing xyz thing"
    exit 1
fi

if [ -z $1 ]
then
    echo "Error: Missing language code"
    echo "Usage: $0 <three letter GiellaLT language code>"
    exit 1
fi


#take in the argument and download the files off github
echo "path to github url/$1"; 
git clone "https://github.com/giellalt/lang-$1.git"

#how do I fill multiple files?
#i need to run the lines in martines thesis, and I need to like idk all of it should be pretty easy except basically globbing all the files that I need
declare -a lex_files
lex_files+=("lang-$1/src/fst/morphology/root.lexc")
echo "root file: lang-$1/src/fst/morphology/root.lexc"
for f in lang-$1/src/fst/morphology/*.lexc
do
    if [ "$f" = "lang-$1/src/fst/morphology/root.lexc" ] #|| [ "$f" = "lang-$1/src/fst/morphology/compounding.lexc" ]
    
    then
        echo ""
    else
        lex_files+=("$f")
        echo "lex file: $f"
    fi
done
#echo ${lex_files[*]}

for f in lang-$1/src/fst/morphology/stems/*.lexc
do
    #if [ "$f" = "lang-$1/src/fst/morphology/stems/numerals.lexc" ] || [ "$f" = "lang-$1/src/fst/morphology/stems/verbs.lexc" ] || [ "$f" = "lang-$1/src/fst/morphology/stems/abbreviations.lexc" ]
    #finnish seems only to break if it includes determiners lexc file, why is the determiners file broken???
    #german breaks on the verbs, gotta take out verbs for german for some reason, it repeats the same thing over and over
    if [ "$f" = "lang-$1/src/fst/morphology/stems/numerals.lexc" ] || [ "$f" = "lang-$1/src/fst/morphology/stems/abbreviations.lexc" ] || [ "$f" = "lang-$1/src/fst/morphology/stems/determiners.lexc" ] || [ "$f" = "lang-$1/src/fst/morphology/stems/digits.lexc" ] || [ "$f" = "lang-$1/src/fst/morphology/stems/verbs.lexc" ]
    then
        echo "not acceptable file! : $f"
    else
        lex_files+=("$f")
        echo "lex file: $f"
    fi
done

for f in lang-$1/src/fst/morphology/affixes/*.lexc
do
    if [ "$f" = "lang-$1/src/fst/morphology/affixes/numerals.lexc" ]
    
    then
        echo ""
    else
        lex_files+=("$f")
        echo "lex file: $f"
    fi
done

echo ${lex_files[*]}

#the error is here, it generates an empty lex.hfst transducer
#hfst-lexc ${lex_files[*]} -o lang-$1/src/fst/morphology/lex.hfst
hfst-lexc -v ${lex_files[*]} | hfst-fst2txt | hfst-txt2fst -o lang-$1/src/fst/morphology/lex.hfst

#hfst-edit-metadata -i lang-$1/src/fst/morphology/lex.hfst -o lang-$1/src/fst/morphology/lex-edit.hfst

hfst-twolc -v lang-$1/src/fst/morphology/phonology.twolc -o lang-$1/src/fst/morphology/twol.hfst

hfst-compose-intersect -v lang-$1/src/fst/morphology/lex.hfst lang-$1/src/fst/morphology/twol.hfst | hfst-fst2txt | hfst-txt2fst -o lang-$1/src/fst/morphology/$1.hfst

hfst-fst2strings -v lang-$1/src/fst/morphology/$1.hfst -o "$1-corpus.txt" -c 0
