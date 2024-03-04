#! /usr/bin/env python

#this is going to be a script which will essentially take the morphological parse dictionary which was 
#yanked from the hfst files from giellalt, and take a corpus, and return a morphological info corpus
#I need to go back to my notes but I think kyle suggested a three column format either from Unimorph or UD

"""
what i need to do
read in a corpus and tokenize it
ok in another file probably, I need to convert the morph dicts i got from hfst into unimorph format
i guess right?
not sure why
I guess I could like also try unimorph morph dicts
and see how their performance compares
ok so i read in the corpus, then i tokenize it, then I find the morph tag, then I 
then I write it to the file
the thing is some fricking tokens will have multiple lemmas or multiple morph parses
so like uh
how do i choose
I think I will default to choosing the first one probably
unfortunately
let's see
i can store them as dicts and pickle them for ease of use
key is the surface form, value is a set of lemma and parse pairs

"""
