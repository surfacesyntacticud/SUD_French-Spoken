# -*- coding: utf-8 -*-
# Mariam Nakhlé


import conll, os

"""
Ce scripte sert à deux choses :
1. extraire le lexique d'un corpus existent
	- on crée un fichier tsv avec la forme, le lemma, le upos, les traits morphologiques et le nombre d'occurrences
2. ajouter l'information sur les traits morphologiques dans un corpus qui ne contient pas de traits morphologiques
	- en nous basant sur le lexique qu'on vient d'extraire
"""


def wrapper(pathFiles, outFileName):
	"""
	Wrapper fonction for the get_lexicon() fonction as defined below
	"""
	dic={}
	file_list = os.listdir(pathFiles)
	f = open(outFileName, "w", encoding="utf-8")
	for file in file_list:
		if file.endswith('.conllu'):
			print(file)
			trees=conll.conllFile2trees(pathFiles+'/'+file)
			dic = get_lexicon(trees, dic)

	for x, y in sorted(dic.items()) :
		line = "\t".join(x) +"\t"+ str(y)+"\n"
		f.write(line)
	f.close()

def get_lexicon(trees,dic) :
	"""
	This fonction takes as input a corpus made of conll files and makes a lexique table out of it.
	The lexique contains the token (its form), the lemma, the corresponding part-of-speech, the moprhological attributes and the frequency of each word.
	"""
	compteur=1
	# nous nous intéresseront pas aux traits mentionnés en bas puisque ce sont des traits qui relèvent du contexte et donc ne sont pas pertinents pour le lexique
	sauf=["AlignBegin","AlignEnd" ,"Gloss","levenshtein", "MotNouveau", "aSupprimer", "Lang","Typo", "Shared"] 
	for bloc in trees :
		for num in bloc :
			trait=[]
			for key in list(bloc[num].keys()):
				if key == 'id' :
					break
				elif key not in sauf :
					trait.append(key+"="+bloc[num][key])
			if trait :
				token = (bloc[num]['t'], bloc[num]['lemma'], bloc[num]['tag'], "|".join(trait),"_")
				if 'Gloss' in bloc[num].keys():
					token = (bloc[num]['t'], bloc[num]['lemma'], bloc[num]['tag'],  "|".join(trait),bloc[num]['Gloss'])
			else :
				token = (bloc[num]['t'], bloc[num]['lemma'], bloc[num]['tag'], "_" ,"_")
				if 'Gloss' in bloc[num].keys():
					token = (bloc[num]['t'], bloc[num]['lemma'], bloc[num]['tag'], "_",bloc[num]['Gloss'])

			if token in dic :
				dic[token]=dic[token]+1
			else :
				dic[token]=compteur
	return dic


def updateFeats(pathFiles1, pathFiles2, lexique):
	"""
	This function browses a corpus of conll files and checks whether the lexicon that we are using contains a morphological analysis for the tokens of the corpus.
	If the token is not present in the lexicon, we write it into the file 'inconnu'. If the word is present in the lexicon and it has exactly one possible
	analysis, the morphological feature is updated in the conll file. However, if the token has more than one possible morphological analysis, the feature is not
	updated and it is written in the 'ambigu' file.
	All the updated conll files are created in the folder './updated_feats'.
	"""
	# ambig_file = open("ambigu_"+os.path.basename(pathFiles)+".tsv", 'w', encoding='utf-8')
	# inconnu_file = open("inconnu_"+os.path.basename(pathFiles)+".tsv", 'w', encoding='utf-8')

	ambig_file = open("ambigu_Stories-Spoken.tsv", 'w', encoding='utf-8')
	inconnu_file = open("inconnu_Stories-Spoken.tsv", 'w', encoding='utf-8')


	# ok_file = open('okay_'+os.path.basename(pathFiles)+".tsv", 'w', encoding='utf-8')
	INC={}
	AMB={}
	lexi = open(lexique , 'r', encoding='utf-8')
	lexContenu=lexi.readlines()
	lex=[]
	for line in lexContenu:
		line=line.split('\t')
		lex.append((line[0], line[1], line[2], line[3]))
	# files = all the conll files (the ones where we want to insert the features)
	files1 = os.listdir(pathFiles1)
	files2 = os.listdir(pathFiles2)
	files1.extend(files2)
	files=files1
	nonamb=0
	amb=0
	unkn=0
	for fic in files:
		if fic.endswith('.conllu'):
			print(fic)
			try :
				trees= conll.conllFile2trees(os.path.join(pathFiles1, fic))
			except :
				trees= conll.conllFile2trees(os.path.join(pathFiles2, fic))
			for tree in trees:
				for i, node in tree.items():
					toCheck = (node['t'], node['lemma'], node['tag'])
					# let's search for the token-lemma-pos combination in the lexicon
					# we will count how many times this combination appears
					searching=0
					for token in lex:
						if token[:3] == toCheck:
							searching+=1
							remember=token
					# searching=1, c'est-à-dire une seule analyse possible
					if searching == 1:
						nonamb+=1
						if remember[3] != "_" and remember[3] != '' and remember[3] != ' ':
							if "|" in remember[3]:
								features = remember[3].split('|')
								for feature in features:
									pair=feature.split('=')
									node[pair[0]] = pair[1]
							else:
								pair=remember[3].split('=')
								node[pair[0]] = pair[1]

					if searching == 0:
						# traitement des ponctuations, le lemma doit être comme la forme
						# en Spoken, le lemme était _
						if toCheck[2] == "PUNCT":
							node['lemma']=node['t']

						else:
							# Traitement des cas spécifiques, à modifier selon les besoins

							# Correction du lemme du pronom je -> lemma = il
							if toCheck[0] == 'je' or toCheck[0] == 'Je' or toCheck[0] == "j'" or toCheck[0] == "J'":
								node['lemma']='il'
								toAdd='Number=Sing|Person=1|PronType=Prs'
								features = toAdd.split('|')
								for feature in features:
									pair=feature.split('=')
									node[pair[0]] = pair[1]
							# Correction du lemme du pronom tu -> lemma = il
							elif toCheck[0] == 'tu' or toCheck[0] == 'Tu':
								node['lemma']='il'
								toAdd='Number=Sing|Person=2|PronType=Prs'
								features = toAdd.split('|')
								for feature in features:
									pair=feature.split('=')
									node[pair[0]] = pair[1]
							# Correction du upos de mais -> upos = CCONJ
							elif toCheck[0]=='mais' and toCheck[1]=='mais' and toCheck[2]=='ADV':
								node['tag']= 'CCONJ' 
							elif toCheck[0]=='Mais' and toCheck[1]=='mais' and toCheck[2]=='ADV':
								node['tag']= 'CCONJ' 

							# On saute les noms propres, de toute façon, ils n'ont pas de traits morphologiques
							elif toCheck[2] != "PROPN":
								# liste des mots inconnus
								if toCheck in INC:
									INC[toCheck]=INC[toCheck]+1
								else:
									INC[toCheck]=1
								unkn+=1
					if searching > 1: # si searching>1, alors il y avait plus qu'une analyse possible - c'est ambigu
					# liste des mots ambigus
						if toCheck in AMB:
							AMB[toCheck] = AMB[toCheck]+1
						else:
							AMB[toCheck]=1
						amb+=1

			# writing the final updated conll files (the full corpus) into the ./updated_feats folder
			conll.trees2conllFile(trees, os.path.join('updated_feats', fic))
	
	
	print(nonamb, 'non ambigous words')
	print(amb, 'ambigous words')
	print(unkn, 'unknown words')


	# writing into the information files
	for x, y in sorted(AMB.items(), key=lambda x:x[1], reverse=True ) :
		lineAMB="\t".join(x)+"\t"+str(y)+' \n'
		ambig_file.write(lineAMB)
	
	for x, y in sorted(INC.items(), key=lambda x:x[1], reverse=True ) :
		lineINC="\t".join(x)+"\t"+str(y)+' \n'
		inconnu_file.write(lineINC)

	inconnu_file.close()
	ambig_file.close() 


if __name__ == "__main__":
	# paths
	lexicon = 'lexique_GSD.tsv'
	GSD_corpus = '../../git/SUD_French-GSD'
	Spoken_corpus = "../../git/SUD_French-Spoken/SUD_French-Paris-Stories"
	Stories_corpus = "../../git/SUD_French-Spoken/SUD_French-Spoken"


	wrapper(GSD_corpus, lexicon)
	# updateFeats(Spoken_corpus, Stories_corpus, lexicon)