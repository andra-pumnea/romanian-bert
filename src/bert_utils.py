from pathlib import Path
from tokenizers import BertWordPieceTokenizer
from tokenizers.processors import BertProcessing


def train_tokenizer():
    paths = [str(x) for x in Path("./ro_data/").glob("*_processed.txt")]

    # Initialize a tokenizer
    tokenizer = BertWordPieceTokenizer()

    # Customize training
    tokenizer.train(files=paths, vocab_size=30_522, min_frequency=2, special_tokens=[
        '[SEP]',
        '[CLS]',
        '[MASK]',
        '[PAD]',
        '[UNK]'
    ])

    # Save files to disk
    tokenizer.save("./ro_data/", "rombert")


def test_tokenizer():
    tokenizer = BertWordPieceTokenizer(
        "./ro_data/rombert-vocab.txt")

    tokenizer.enable_truncation(max_length=512)

    input_ids = tokenizer.encode('Eu sunt Andrada.')
    print(input_ids.tokens)


if __name__ == '__main__':
    train_tokenizer()
    test_tokenizer()
