#!/usr/bin/env bash

FileName=$1
FolderName=./ro_data/split_dataset

# TODO:get data
if [[ (-n ${Filename}) ]]; then
    # split the dataset into smaller files containing 55 000 lines per file
    split -l 550000 -d --additional-suffix=.txt ${FileName} file > ${FolderName}
    # run the sentence segmentation step
    python ./src/preprocess_txt.py --input_folder ${FolderName}
    # merge the preprocessed files back into one dataset
    find . -name "file*_processed.txt" | sort -k1 | xargs cat > '{$FileName}_processed.txt'
    # remove the files created in the segmentation step
    rm -r ${FolderName}/*
else
    echo 'Error: argument is empty'
fi