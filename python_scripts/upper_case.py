import os
import glob
import conll


def tolower(file_path):
    trees= conll.conllFile2trees(file_path)       
    for tree in trees:
        for i, node in tree.items():
            if node['t'] != "PROPN": # if not proper noun
                node['t']=node['t'].lower() # make it lower
    # write the modified conll file to a new conll file
    conll.trees2conllFile(trees, os.path.join('sans_majuscules', os.path.basename(file_path)))
    return True


if __name__ == "__main__":
    files = glob.glob("../Paris_Stories/*")
    # make the directory
    if not os.path.isdir('sans_majuscules'):
            os.mkdir('sans_majuscules')  
    # treat the files
    for file in files:
        tolower(file)