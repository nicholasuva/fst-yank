#! /usr/bin/env python3

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


3/4/24 what do i want to do, get corpora annotated and in a unimorph format
"""

import re
import pickle
from nltk.tokenize import word_tokenize


def hfst_entry_parse(line):
    #split surface form from lemma+parse

    sep = line.rstrip('\n').split(':')
    surface_form = sep[-1]
    lemma_and_parse = sep[0]
    sep2 = lemma_and_parse.split('+')
    lemma = sep2[0]
    parse_tags = sep2[1:]
    entry_dict = {
        'lemma': lemma,
        'surface_form': surface_form,
        'parse_tags': parse_tags
    }
    return entry_dict

def hfst_lex2dict(lex_filename):
    morph_dict = {}
    with open(lex_filename, 'r') as source:
        for line in source:
            line_dict = hfst_entry_parse(line)
            #print(line)
            #print(line_dict)
            this_surface_form = line_dict['surface_form']
            if this_surface_form in morph_dict:
                morph_dict[this_surface_form].append(line_dict)
            else:
                morph_dict[this_surface_form] = [line_dict]
    return morph_dict

def pickle_dict(dict, pickle_filename):
    with open(pickle_filename, 'wb') as handle:
        pickle.dump(dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print(pickle_filename + ' successfully pickled.')
    return

def load_pickle(pickle_filename):
    print('loading pickle:\t' + pickle_filename)
    with open(pickle_filename, 'rb') as handle:
        dict = pickle.load(handle)
    print('pickle loaded:\t' + pickle_filename)
    return dict

def display_parses_unimorph_str(parses):
    #I may need to standardize the abbreviations for the parses
    parse_string = ';'.join([parse for parse in parses])
    return parse_string


def sentence_annotate(sentence, morph_lex_dict):
    #annotate the sentence with unimorph format
    tokens = word_tokenize(sentence)
    #tokens = tokens.lower() may need to reimplement this??
    annotated_tokens = []
    for token in tokens:
        if token in morph_lex_dict:
            this_ann_tok = [morph_lex_dict[token][0]['lemma'], token, display_parses_unimorph_str(morph_lex_dict[token][0]['parse_tags'])]
            annotated_tokens.append(this_ann_tok)
        else:
            this_ann_tok = ['-', token, '-']
            annotated_tokens.append(this_ann_tok)
    return annotated_tokens

def raw_corpus_annotate(corpus_filename, out_filename, morph_lex_dict):
    with open(corpus_filename,'r') as source:
        for count, line in enumerate(source):
            pass
    num_sents = count + 1
    line_counter = 0
    with open(corpus_filename,'r') as source:
        with open(out_filename,'w') as sink:
            for line in source:
                line_counter += 1
                annotated_line = sentence_annotate(line.rstrip('\n'), morph_lex_dict)
                for token in annotated_line:
                    sink.write('\t'.join([elem for elem in token]) + '\n')
                sink.write('\n')
                print("Annotating corpus:\t" + corpus_filename + "\t. Progress:\t{:.1f}%".format(line_counter/num_sents*100),end='\r')
    print("Corpus annotated:\t" + corpus_filename +"\tdestination:\t" + out_filename, end='\n')
    return



def main():
    """
    eng_dict = hfst_lex2dict('eng-corpus.txt')
    pickle_dict(eng_dict, 'eng-dict.pickle')
    deu_dict = hfst_lex2dict('deu-corpus.txt')
    pickle_dict(deu_dict, 'deu-dict.pickle')
    """
    deu_corp_dict = load_pickle('deu-dict.pickle')
    test_sent_de = "Hallo, das ist mein unwirklisch Tintenfisch, und ich liebe dich."
    #ann_test = sentence_annotate(test_sent_de, deu_corp_dict)
    #print(ann_test)
    #raw_corpus_annotate('de-corpus-test-file.txt', 'de-test-annotated.txt', deu_corp_dict)
    raw_corpus_annotate('../Corpora/OpenSubtitles/en-de/OpenSubtitles.de-en.de', '../Corpora/OpenSubtitles/en-de/OpenSubtitles.de-en.de-hfst-morph-annotated', deu_corp_dict)



    return

main()
