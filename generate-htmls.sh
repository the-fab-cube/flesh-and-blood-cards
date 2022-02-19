#!/bin/bash

pyenv exec csvtotable csvs/card.csv web/card.html -d $'\t' -q $'"' -o