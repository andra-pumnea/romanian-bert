#!/usr/bin/env bash

FileName=./ro_data/ro_dedup.txt
FolderName=./ro_data/split_dataset

# TODO:get data
# split the dataset into smaller files containing 55 000 lines per file
split -l 550000 -d --additional-suffix=.txt $FileName file > ${FolderName}
# run the sentence segmentation step
python ./src/preprocess_txt.py --input_folder ${FolderName}
# merge the preprocessed files back into one dataset
find . -name "file*_processed.txt" | sort -k1 | xargs cat > ./ro_data/ro_dedup_processed.txt