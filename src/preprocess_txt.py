from nltk.tokenize import sent_tokenize
import argparse


def format_data_for_bert(input_file, output_file):
    with open(input_file, 'r') as ro_txt:
        for line in ro_txt:
            doc = sent_tokenize(line)
            for sent in doc:
                with open(output_file, 'a') as ro_processed:
                    ro_processed.write("%s\n" % sent)
                ro_processed.close()
    ro_txt.close()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', help='Provide text file to be processed')
    parser.add_argument('--output_file', help='Provide text file where the output will be found')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    format_data_for_bert(args.input_file, args.output_file)
