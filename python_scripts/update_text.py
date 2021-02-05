#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os

"""
Ce scripte sert à mettre à jour le trait "# text =" des métadonnées. Il ne fait que coller les tokens comme ils apparaissent dans le conll.
Le scripte prend en compte le trait "SpaceAfter=No" de la colonne misc et les amalgammes sont écrits ocmme un mot (ex : 'au' et pas 'à le')
"""

def getTokens(content, i):
    text="# text = "
    while content[i] != "\n": # le saut à la ligne signifie la fin de la phrase, on s'arrête car on traite le corpus phrase par phrase
        # print(content[i])
        line=content[i].split("\t")
        if "-" in line[0]: # les amalgammes ont comme index deux chiffres, par exeple 3-4 où 3=à et 4=le, on prend la forme dans la 2e colonne (au)
            text+=line[1]+" "
            i+=2 # on saute les 2 lignes suivantes qui correspondent à l'analyse des deux composants (à et le)
        elif "SpaceAfter=No" in line[9]:
            text+=line[1] # pas d'espace ajouté
        else:
            text+=line[1]+" " # le cas normal = on écrit la forme et un espace
        i+=1
    return text[:-1]+"\n"


def updateText(pathFiles, outfile):
    """
    This function treats all conll files from a directory.
    It reads a conll file line by line and when it finds a "# text =" line, it takes the tokens that follow.
    The result is written in a directory - outfile. This directory must already exist!
    """
    file_list = os.listdir(pathFiles)
    for file in file_list:
        if file.endswith('.conllu'):
            print(file)
            newfile=outfile+file
            new=open(newfile, 'w', encoding='utf-8')
            with open(pathFiles+file, 'r', encoding='utf-8') as fic:
                content=fic.readlines()
                i=0
                for line in content:
                    if line.startswith("# text = "): # une fois arrivés à cette ligne, on va chercher les tokens pour les coller
                        # print('lets start')
                        text = getTokens(content,i+1)
                        new.write(text)
                    else: # si ce n'est pas la ligne # text, on l'écrit telle quelle
                        new.write(line)
                    i+=1
    fic.close()


if __name__ == "__main__":
    # premier argument = dossier avec les conll à modifier
    # deuxième argument = dossier où seront écrits les conll modifiés (il faut el créer avant de lancer)
    updateText("macro_corpus/", "text_updated/")