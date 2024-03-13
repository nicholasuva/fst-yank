#! /usr/bin/env python

"""
this will basically show which morph features are in which langs in the GiellaLT tools
"""

import glob
import subprocess
import matplotlib
import matplotlib.pyplot as plt
import re
import numpy as np


def dl_lang(lang_code):
    subprocess.run(["git", "clone", "https://github.com/giellalt/lang-"+lang_code+".git"])
    return

def find_lexc_files(lang_code):
    lexc_files = glob.glob("lang-"+lang_code+"/src/fst/morphology/**/*.lexc", recursive=True)
    print(lexc_files)
    truncated_files = []
    for file in lexc_files:
        valid_file = re.search(r'^lang-.*/src/fst/morphology/(.*\.lexc)$', file)
        truncated_files.append(valid_file.group(1))
    return lexc_files, truncated_files


def file_numlines(filepath):
    with open(filepath, 'r') as source:
        numlines = len(source.readlines())
    return numlines

def all_files_numlines(filepath_list, trunc_file_list):
    file_dict = {}
    for filepath, trunc in zip(filepath_list, trunc_file_list):
        #file_tuple = (file, file_numlines(file))
        #file_tuples.append(file_tuple)
        file_dict[trunc] = file_numlines(filepath)
    return file_dict


    
def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw=None, cbarlabel="", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (M, N).
    row_labels
        A list or array of length M with the labels for the rows.
    col_labels
        A list or array of length N with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if ax is None:
        ax = plt.gca()

    if cbar_kw is None:
        cbar_kw = {}

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    # Show all ticks and label them with the respective list entries.
    ax.set_xticks(np.arange(data.shape[1]), labels=col_labels)
    ax.set_yticks(np.arange(data.shape[0]), labels=row_labels)

    #this is nick trying to change the scale
    #ax.set_ylim([0,5])
    #that doesnt seem to work


    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
             rotation_mode="anchor")

    # Turn spines off and create white grid.
    ax.spines[:].set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar


def annotate_heatmap(im, data=None, valfmt="{x:.2f}",
                     textcolors=("black", "white"),
                     threshold=None, **textkw):
    """
    A function to annotate a heatmap.

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A pair of colors.  The first is used for values below a threshold,
        the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts

def format_all_data(list_of_lang_codes):
    """
    I need to change the output to a dict from a list of tuples, for each lang
    """
    all_lang_dict = {}
    for lang_code in list_of_lang_codes:
        dl_lang(lang_code)
        this_lexc_list, trunc_list = find_lexc_files(lang_code)
        this_lexc_heat_dict = all_files_numlines(this_lexc_list, trunc_list)
        all_lang_dict[lang_code] = this_lexc_heat_dict
    
    #find all filenames for all types of morph
    morph_file_set = set()
    for lang in all_lang_dict:
        for filename in all_lang_dict[lang]:
            #valid_file = re.search(r'^lang-.*/src/fst/morphology/(.*\.lexc)$', filename)
            #print(valid_file.group(1))
            #all_lang_dict[lang]
            #name = valid_file.group(1)
            if filename not in morph_file_set:
                morph_file_set.add(filename)
            #print(filename)
                
    y_label = list_of_lang_codes
    x_label = list(morph_file_set)


    #making the data into a numpy array
    #we want the rows to be per language, ok
    dimensions = (len(y_label), len(x_label))
    data = np.zeros(dimensions)
    #data[1,3] = 5
    for i in range(len(y_label)):
        for j in range(len(x_label)):
            #check if that morph file is in that lang
            if x_label[j] in all_lang_dict[y_label[i]]:
                data[i,j] = all_lang_dict[y_label[i]][x_label[j]]
    print(data)

    return x_label, y_label, data



all_giellalt_langs = [('aka', 'Akan'),
                      ('ale', 'Aleut'),
                      ('amh', 'Amharic'),
                      ('apu', 'Apurinã'),
                      ('ara', 'Arabic'),
                      ('aym', 'Aymara'),
                      ('bak', 'Bashkir'),
                      ('bla', 'Siksika'),
                      ('bul', 'Bulgarian'),
                      ('bxr', 'Russia Buriat'),
                      ('ces', 'Czech'),
                      ('cho', 'Choctaw'),
                      ('chp', 'Chipewyan'),
                      ('chr', 'Cherokee'),
                      ('ciw', 'Chippewa'),
                      ('ckt', 'Chukot'),
                      ('cor', 'Cornish'),
                      ('crj', 'Southern East Cree'),
                      ('crk', 'Plains Cree'),
                      ('cwd', 'Woods Cree'),
                      ('dag', 'Dagbani'),
                      ('deu', 'German'),
                      ('dgr', 'Dogrib'),
                      ('dsb', 'Lower Sorbian'),
                      ('eng', 'English'),
                      ('epo', 'Esperanto'),
                      ('ess', 'Central Siberian Yupik'),
                      ('est-x-plamk', 'Estonian (plamk)'),
                      ('est-x-utee', 'Estonian (utee)'),
                      ('esu', 'Central Alaskan Yup\'ik'),
                      ('eus', 'Basque'),
                      ('evn', 'Evenki'),
                      ('fao', 'Faroese'),
                      ('fin', 'Finnish'),
                      ('fit', 'Meänkieli (Tornedalen Finnish)'),
                      ('fkv', 'Kven Finnish'),
                      ('fro', 'Old French (842-ca. 1400)'),
                      ('gle', 'Irish'),
                      ('got', 'Gothic'),
                      ('grn', 'Guarani'),
                      ('gur', 'Farefare'),
                      ('hdn', 'Northern Haida'),
                      ('hil', 'Hiligaynon'),
                      ('hin', 'Hindi'),
                      ('hun', 'Hungarian'),
                      ('iku', 'Inuktitut'),
                      ('inp', 'Iñapari'),
                      ('ipk', 'Inupiaq'),
                      ('izh', 'Ingrian'),
                      ('kal', 'Kalaallisut'),
                      ('kca', 'Khanty'),
                      ('kek', 'Qʼeqchiʼ'),
                      ('khk', 'Bulgarian'),
                      ('kio', 'Siksika'),
                      ('kjh', 'Bulgarian'),
                      ('kmr', 'Siksika'),
                      ('koi', 'Bulgarian'),
                      ('kpv', 'Siksika'),
                      ('krl', 'Bulgarian'),
                      ('lav', 'Siksika'),
                      ('lit', 'Bulgarian'),
                      ('liv', 'Siksika'),
                      ('luo', 'Bulgarian'),
                      ('lut', 'Siksika'),
                      ('mdf', 'Bulgarian'),
                      ('mhr', 'Siksika'),
                      ('mns', 'Bulgarian'),
                      ('moh', 'Siksika'),
                      ('mpj', 'Bulgarian'),
                      ('mrj', 'Siksika'),
                      ('mya', 'Bulgarian'),
                      ('myv', 'Siksika'),
                      ('ndl', 'Bulgarian'),
                      ('nds', 'Siksika'),
                      ('nio', 'Bulgarian'),
                      ('nno', 'Siksika'),
                      ('nno-x-ext-apertium', 'Bulgarian'),
                      ('nob', 'Siksika'),
                      ('non', 'Bulgarian'),
                      ('nso', 'Siksika'),
                      ('oji', 'Bulgarian'),
                      ('olo', 'Siksika'),
                      ('pma', 'Bulgarian'),
                      ('quc-x-ext-apertium', 'Siksika'),
                      ('qya', 'Bulgarian'),
                      ('rmf', 'Siksika'),
                      ('rmg', 'Bulgarian'),
                      ('rmu-x-testing', 'Siksika'),
                      ('rmy', 'Bulgarian'),
                      ('ron', 'Siksika'),
                      ('rue', 'Bulgarian'),
                      ('rup', 'Siksika'),
                      ('rus', 'Bulgarian'),
                      ('sel', 'Siksika'),
                      ('sjd', 'Bulgarian'),
                      ('sje', 'Siksika'),
                      ('sjt', 'Bulgarian'),
                      ('sju-x-sydlapsk', 'Siksika'),
                      ('skf', 'Bulgarian'),
                      ('sma', 'Siksika'),
                      ('sme', 'Bulgarian'),
                      ('smj', 'Siksika'),
                      ('smn', 'Bulgarian'),
                      ('sms', 'Siksika'),
                      ('som', 'Bulgarian'),
                      ('spa-x-ext-apertium', 'Siksika'),
                      ('sqi', 'Bulgarian'),
                      ('srs', 'Siksika'),
                      ('sto', 'Bulgarian'),
                      ('swe', 'Siksika'),
                      ('tat', 'Bulgarian'),
                      ('tau', 'Siksika'),
                      ('tel', 'Bulgarian'),
                      ('tgl', 'Siksika'),
                      ('tha', 'Bulgarian'),
                      ('tir', 'Siksika'),
                      ('tku', 'Bulgarian'),
                      ('tlh', 'Siksika'),
                      ('tqn', 'Bulgarian'),
                      ('tur-x-ext-trmorph', 'Siksika'),
                      ('tuv', 'Bulgarian'),
                      ('tyv', 'Siksika'),
                      ('udm', 'Bulgarian'),
                      ('vep', 'Siksika'),
                      ('vot', 'Bulgarian'),
                      ('vot-x-ext-kkankain', 'Siksika'),
                      ('vro', 'Bulgarian'),
                      ('xak', 'Siksika'),
                      ('xal', 'Bulgarian'),
                      ('xin-x-qda', 'Guazacapán'),
                      ('xwo', 'Written Oirat'),
                      ('yrk', 'Nenets'),
                      ('zul-x-exp', 'Zulu'),
                      ('zxx', 'No linguistic content')
                      ]

def main():
    #lang_code = "eng"
    #dl_lang(lang_code)
    #test_list = find_lexc_files(lang_code)
    #this_list = all_files_numlines(test_list)
    #print(this_list)
    x_label, y_label, data = format_all_data(['eng', 'rus', 'deu', 'spa'])

    fig, ax = plt.subplots()
    im, cbar = heatmap(data, y_label, x_label, ax=ax, cmap='YlGn', cbarlabel='test', norm='log')
    #texts = annotate_heatmap(im, valfmt="{x:.1f}")
    fig.tight_layout()
    plt.show()
    plt.savefig('test.png')

    return

main()