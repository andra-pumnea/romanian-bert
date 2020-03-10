from pathlib import Path
from tokenizers import WordPiece
from tokenizers.processors import BertProcessing


def train_tokenizer():
    paths = [str(x) for x in Path("./ro_data/").glob("*_processed.txt")]

    # Initialize a tokenizer
    tokenizer = WordPiece()

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
    tokenizer = WordPiece(
        "./ro_data/rombert-vocab.json",
        "./ro_data/rombert-merges.txt", )

    tokenizer._tokenizer.post_processor = BertProcessing(
        ("[SEP]", tokenizer.token_to_id("[SEP]")) )

    tokenizer.enable_truncation(max_length=512)

    input_ids = tokenizer.encode('Eu sunt Andrada.')
    print(input_ids.tokens)


if __name__ == '__main__':
    train_tokenizer()
    test_tokenizer()
