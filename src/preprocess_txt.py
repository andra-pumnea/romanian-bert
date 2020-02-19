import concurrent
import glob

from nltk.tokenize import sent_tokenize
import argparse


def format_data_for_bert(input_file):
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


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', help='Provide text file to be processed')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    # Create a pool of processes. By default, one is created for each CPU in your machine.
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Get a list of files to process
        input_files = glob.glob("*.txt")

        # Process the list of files, but split the work across the process pool to use all CPUs!
        for input_file, output_file in zip(input_files, executor.map(format_data_for_bert, input_files)):
            print(f"A preprocessing for {input_file} was saved as {output_file}")
    # format_data_for_bert(args.input_file, args.output_file)
