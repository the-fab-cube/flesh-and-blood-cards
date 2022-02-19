#!/bin/bash

pyenv exec csvtotable csvs/card.csv web/card.html -d $'\t' -q $'"' -o
pyenv exec csvtotable csvs/edition.csv web/edition.html -d $'\t' -q $'"' -o
pyenv exec csvtotable csvs/foiling.csv web/foiling.html -d $'\t' -q $'"' -o
pyenv exec csvtotable csvs/icon.csv web/icon.html -d $'\t' -q $'"' -o
pyenv exec csvtotable csvs/keyword.csv web/keyword.html -d $'\t' -q $'"' -o
pyenv exec csvtotable csvs/rarity.csv web/rarity.html -d $'\t' -q $'"' -o
pyenv exec csvtotable csvs/set.csv web/set.html -d $'\t' -q $'"' -o
pyenv exec csvtotable csvs/type.csv web/type.html -d $'\t' -q $'"' -o