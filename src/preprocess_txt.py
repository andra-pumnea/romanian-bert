from nltk.tokenize import sent_tokenize


def format_data_for_bert(ro_data):
    with open(ro_data, 'r') as ro_txt:
        for line in ro_txt:
            doc = sent_tokenize(line)
            for sent in doc:
                with open('../data/ro_dedup_processed.txt', 'a') as ro_processed:
                    ro_processed.write("%s\n" % sent)
                ro_processed.close()
    ro_txt.close()


if __name__ == '__main__':
    format_data_for_bert('../data/ro_dedup100.txt')
