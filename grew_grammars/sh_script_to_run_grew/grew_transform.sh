#!usr/bin/bash

# le corpus contenant les fichiers à traiter
corpus=spoken

# le fichier contenant les règles grew
rules=$1
echo $rules
# la sortie, le dossier doit déjà exister !
output=output


for filename in $(ls $corpus)
	do
	# echo $filename
	grew transform -i $corpus/$filename -o $output/$filename -grs $rules
	done