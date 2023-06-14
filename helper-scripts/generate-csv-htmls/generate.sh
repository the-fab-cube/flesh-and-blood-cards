#!/bin/bash

if type pyenv > /dev/null 2>&1; then
    CMD="pyenv exec poetry run csvtotable"
else
    CMD="csvtotable"
fi

$CMD ../../csvs/english/ability.csv ../../web/csvs/english/ability.html -d $'\t' -q $'"' -o
$CMD ../../csvs/english/art-variation.csv ../../web/csvs/english/art-variation.html -d $'\t' -q $'"' -o
$CMD ../../csvs/english/artist.csv ../../web/csvs/english/artist.html -d $'\t' -q $'"' -o
$CMD ../../csvs/english/card.csv ../../web/csvs/english/card.html -d $'\t' -q $'"' -o
$CMD ../../csvs/english/card-printing.csv ../../web/csvs/english/card-printing.html -d $'\t' -q $'"' -o
$CMD ../../csvs/english/edition.csv ../../web/csvs/english/edition.html -d $'\t' -q $'"' -o
$CMD ../../csvs/english/foiling.csv ../../web/csvs/english/foiling.html -d $'\t' -q $'"' -o
$CMD ../../csvs/english/icon.csv ../../web/csvs/english/icon.html -d $'\t' -q $'"' -o
$CMD ../../csvs/english/keyword.csv ../../web/csvs/english/keyword.html -d $'\t' -q $'"' -o
$CMD ../../csvs/english/rarity.csv ../../web/csvs/english/rarity.html -d $'\t' -q $'"' -o
$CMD ../../csvs/english/set.csv ../../web/csvs/english/set.html -d $'\t' -q $'"' -o
$CMD ../../csvs/english/set-printing.csv ../../web/csvs/english/set-printing.html -d $'\t' -q $'"' -o
$CMD ../../csvs/english/type.csv ../../web/csvs/english/type.html -d $'\t' -q $'"' -o

$CMD ../../csvs/french/ability.csv ../../web/csvs/french/ability.html -d $'\t' -q $'"' -o
$CMD ../../csvs/french/artist.csv ../../web/csvs/french/artist.html -d $'\t' -q $'"' -o
$CMD ../../csvs/french/card.csv ../../web/csvs/french/card.html -d $'\t' -q $'"' -o
$CMD ../../csvs/french/card-printing.csv ../../web/csvs/french/card-printing.html -d $'\t' -q $'"' -o
$CMD ../../csvs/french/keyword.csv ../../web/csvs/french/keyword.html -d $'\t' -q $'"' -o
$CMD ../../csvs/french/set-printing.csv ../../web/csvs/french/set-printing.html -d $'\t' -q $'"' -o
$CMD ../../csvs/french/type.csv ../../web/csvs/french/type.html -d $'\t' -q $'"' -o

$CMD ../../csvs/german/ability.csv ../../web/csvs/german/ability.html -d $'\t' -q $'"' -o
$CMD ../../csvs/german/artist.csv ../../web/csvs/german/artist.html -d $'\t' -q $'"' -o
$CMD ../../csvs/german/card.csv ../../web/csvs/german/card.html -d $'\t' -q $'"' -o
$CMD ../../csvs/german/card-printing.csv ../../web/csvs/german/card-printing.html -d $'\t' -q $'"' -o
$CMD ../../csvs/german/keyword.csv ../../web/csvs/german/keyword.html -d $'\t' -q $'"' -o
$CMD ../../csvs/german/set-printing.csv ../../web/csvs/german/set-printing.html -d $'\t' -q $'"' -o
$CMD ../../csvs/german/type.csv ../../web/csvs/german/type.html -d $'\t' -q $'"' -o

$CMD ../../csvs/italian/ability.csv ../../web/csvs/italian/ability.html -d $'\t' -q $'"' -o
$CMD ../../csvs/italian/artist.csv ../../web/csvs/italian/artist.html -d $'\t' -q $'"' -o
$CMD ../../csvs/italian/card.csv ../../web/csvs/italian/card.html -d $'\t' -q $'"' -o
$CMD ../../csvs/italian/card-printing.csv ../../web/csvs/italian/card-printing.html -d $'\t' -q $'"' -o
$CMD ../../csvs/italian/keyword.csv ../../web/csvs/italian/keyword.html -d $'\t' -q $'"' -o
$CMD ../../csvs/italian/set-printing.csv ../../web/csvs/italian/set-printing.html -d $'\t' -q $'"' -o
$CMD ../../csvs/italian/type.csv ../../web/csvs/italian/type.html -d $'\t' -q $'"' -o

$CMD ../../csvs/spanish/ability.csv ../../web/csvs/spanish/ability.html -d $'\t' -q $'"' -o
$CMD ../../csvs/spanish/artist.csv ../../web/csvs/spanish/artist.html -d $'\t' -q $'"' -o
$CMD ../../csvs/spanish/card.csv ../../web/csvs/spanish/card.html -d $'\t' -q $'"' -o
$CMD ../../csvs/spanish/card-printing.csv ../../web/csvs/spanish/card-printing.html -d $'\t' -q $'"' -o
$CMD ../../csvs/spanish/keyword.csv ../../web/csvs/spanish/keyword.html -d $'\t' -q $'"' -o
$CMD ../../csvs/spanish/set-printing.csv ../../web/csvs/spanish/set-printing.html -d $'\t' -q $'"' -o
$CMD ../../csvs/spanish/type.csv ../../web/csvs/spanish/type.html -d $'\t' -q $'"' -o
