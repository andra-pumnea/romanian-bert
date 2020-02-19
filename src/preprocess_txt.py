import concurrent.futures
import glob
import time

from nltk.tokenize import sent_tokenize
import argparse


def segment_sentences(input_file):
    with open(input_file, 'r') as ro_txt:
        output_file = input_file + '_processed'
        for line in ro_txt:
            doc = sent_tokenize(line)
            for sent in doc:
                with open(output_file, 'a') as ro_processed:
                    ro_processed.write("%s\n" % sent)
                ro_processed.close()
    ro_txt.close()
    return output_file


def run_segmentation_in_parallel(input_folder):
    # Create a pool of processes. By default, one is created for each CPU in your machine.
    #split -l 5000 -d --additional-suffix=.txt $FileName file
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Get a list of files to process
        input_files = glob.glob(input_folder)

        start = time.clock()

        # Process the list of files, but split the work across the process pool to use all CPUs!
        for input_file, output_file in zip(input_files, executor.map(segment_sentences, input_files)):
            print(f"A preprocessing for {input_file} was saved as {output_file}")

        elapsed = time.clock()
        print("Time spent in current batch is: ", elapsed - start)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_folder', help='Provide the folder where the text data needs to be processed')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    start = time.clock()
    run_segmentation_in_parallel(args.input_folder)
    elapsed = time.clock()
    print("Time spent in run_segmentation_in_parallel is: ", elapsed - start)