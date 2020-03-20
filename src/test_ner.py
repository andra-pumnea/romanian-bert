from farm.infer import Inferencer

def test_model():

    save_dir = "saved_models/bert-romanian-ner"

    # Load it & harvest your fruits (Inference)
    basic_texts = [
        {"text": "Popescu Ion merge la Cluj"},
        {"text": "Andrada s-a mutat in Berlin de 2 ani"},
    ]
    model = Inferencer.load(save_dir)
    result = model.inference_from_dicts(dicts=basic_texts)
    print(result)
    
if __name__ == "__main__":
    test_model()