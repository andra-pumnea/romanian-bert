#!/usr/bin/env bash

FileName=$1
mkdir ./ro_data/split_dataset

# TODO:get data
if [[ (-n ${FileName}) ]]; then
    # split the dataset into smaller files containing 55 000 lines per file
    split -l 550000 -d --additional-suffix=.txt ${FileName} file > ./ro_data/split_dataset
    # run the sentence segmentation step
    python ./src/preprocess_txt.py --input_folder ./ro_data/split_dataset
    # merge the preprocessed files back into one dataset
    ${output_file}=${FileName%.txt}_processed.txt
    find . -name "file*_processed.txt" | sort -k1 | xargs cat > $output_file
    # remove the files created in the segmentation step
    # rm -r ./ro_data/split_dataset
else
    echo 'Error: argument is empty'
fi