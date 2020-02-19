from pathlib import Path
from tokenizers import ByteLevelBPETokenizer
from tokenizers.processors import BertProcessing


def train_tokenizer():
    paths = [str(x) for x in Path("./ro_data/").glob("**/*.txt")]

    # Initialize a tokenizer
    tokenizer = ByteLevelBPETokenizer()

    # Customize training
    tokenizer.train(files=paths, vocab_size=52_000, min_frequency=2, special_tokens=[
        "<s>",
        "<pad>",
        "</s>",
        "<unk>",
        "<mask>",
    ])

    # Save files to disk
    tokenizer.save("./ro_data/", "rombert")


def test_tokenizer():
    tokenizer = ByteLevelBPETokenizer(
        "./ro_data/rombert-vocab.json",
        "./ro_data/rombert-merges.txt", )

    tokenizer._tokenizer.post_processor = BertProcessing(
        ("</s>", tokenizer.token_to_id("</s>")),
        ("<s>", tokenizer.token_to_id("<s>")), )

    tokenizer.enable_truncation(max_length=512)

    input_ids = tokenizer.encode('Eu sunt Andrada.')
    print(input_ids.tokens)

if __name__ == '__main__':
    train_tokenizer()
    test_tokenizer()
