#!/bin/bash

#ok I would like a script that can download the giellalt and make the yankerino all in one

#make it check if hfst is installed


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
    if [ "$f" = "lang-$1/src/fst/morphology/root.lexc" ]
    
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
    if [ "$f" = "lang-$1/src/fst/morphology/stems/numerals.lexc" ] | [ "$f" = "lang-$1/src/fst/morphology/stems/verbs.lexc" ] | [ "$f" = "lang-$1/src/fst/morphology/stems/abbreviations.lexc" ]
    
    then
        echo ""
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


hfst-lexc ${lex_files[*]} -o lang-$1/src/fst/morphology/lex.hfst

hfst-twolc lang-$1/src/fst/morphology/phonology.twolc -o lang-$1/src/fst/morphology/twol.hfst

hfst-compose-intersect lang-$1/src/fst/morphology/lex.hfst lang-$1/src/fst/morphology/twol.hfst -o lang-$1/src/fst/morphology/$1.hfst

hfst-fst2strings lang-$1/src/fst/morphology/$1.hfst -o "$1-corpus.txt" -c 1