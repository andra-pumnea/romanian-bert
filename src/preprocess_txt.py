from nltk.tokenize import sent_tokenize
import argparse


def format_data_for_bert(ro_data):
    with open(ro_data, 'r') as ro_txt:
        for line in ro_txt:
            doc = sent_tokenize(line)
            for sent in doc:
                with open('ro_data/ro_dedup_processed.txt', 'a') as ro_processed:
                    ro_processed.write("%s\n" % sent)
                ro_processed.close()
    ro_txt.close()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', help='Provide text file to be processed')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    format_data_for_bert(args.input_file)
