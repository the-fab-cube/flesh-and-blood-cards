#!/bin/bash

pyenv exec poetry run csvtotable ../../csvs/english/ability.csv ../../web/csvs/ability.html -d $'\t' -q $'"' -o
pyenv exec poetry run csvtotable ../../csvs/english/artist.csv ../../web/csvs/artist.html -d $'\t' -q $'"' -o
pyenv exec poetry run csvtotable ../../csvs/english/card.csv ../../web/csvs/card.html -d $'\t' -q $'"' -o
pyenv exec poetry run csvtotable ../../csvs/english/edition.csv ../../web/csvs/edition.html -d $'\t' -q $'"' -o
pyenv exec poetry run csvtotable ../../csvs/english/foiling.csv ../../web/csvs/foiling.html -d $'\t' -q $'"' -o
pyenv exec poetry run csvtotable ../../csvs/english/icon.csv ../../web/csvs/icon.html -d $'\t' -q $'"' -o
pyenv exec poetry run csvtotable ../../csvs/english/keyword.csv ../../web/csvs/keyword.html -d $'\t' -q $'"' -o
pyenv exec poetry run csvtotable ../../csvs/english/rarity.csv ../../web/csvs/rarity.html -d $'\t' -q $'"' -o
pyenv exec poetry run csvtotable ../../csvs/english/set.csv ../../web/csvs/set.html -d $'\t' -q $'"' -o
pyenv exec poetry run csvtotable ../../csvs/english/type.csv ../../web/csvs/type.html -d $'\t' -q $'"' -o