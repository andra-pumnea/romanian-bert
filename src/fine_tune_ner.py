import logging
from pathlib import Path

from farm.data_handler.data_silo import DataSilo
from farm.data_handler.processor import NERProcessor
from farm.modeling.optimization import initialize_optimizer
from farm.infer import Inferencer
from farm.modeling.adaptive_model import AdaptiveModel
from farm.modeling.language_model import LanguageModel
from farm.modeling.prediction_head import TokenClassificationHead
from farm.modeling.tokenization import Tokenizer
from farm.train import Trainer
from farm.utils import set_all_seeds, MLFlowLogger, initialize_device_settings

def ner():
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=logging.INFO,
    )

    ml_logger = MLFlowLogger(tracking_uri="https://public-mlflow.deepset.ai/")
    ml_logger.init_experiment(experiment_name="Public_FARM", run_name="Run_ner_ronec")

    ##########################
    ########## Settings
    ##########################
    set_all_seeds(seed=42)
    device, n_gpu = initialize_device_settings(use_cuda=True)
    n_epochs = 4
    batch_size = 16
    evaluate_every = 200
    lang_model =  "xlm-roberta-large"
    do_lower_case = False

    # 1.Create a tokenizer
    tokenizer = Tokenizer.load(
        pretrained_model_name_or_path=lang_model, do_lower_case=do_lower_case
    )

    # 2. Create a DataProcessor that handles all the conversion from raw text into a pytorch Dataset
    ner_labels = ["[PAD]", 'X','O', 'I-ORDINAL', 'I-ORGANIZATION', 'I-NUMERIC_VALUE', 'I-DATETIME', 'I-PRODUCT', 'I-PERSON', 'I-GPE', 'I-NAT_REL_POL',
                   'I-FACILITY', 'I-QUANTITY', 'I-LOC', 'I-MONEY', 'I-EVENT', 'I-PERIOD', 'I-WORK_OF_ART', 'I-LANGUAGE',
                   'B-ORDINAL', 'B-ORGANIZATION', 'B-NUMERIC_VALUE', 'B-DATETIME', 'B-PRODUCT', 'B-PERSON', 'B-GPE', 'B-NAT_REL_POL',
                   'B-FACILITY', 'B-QUANTITY', 'B-LOC', 'B-MONEY', 'B-EVENT', 'B-PERIOD', 'B-WORK_OF_ART', 'B-LANGUAGE']

    processor = NERProcessor(
        tokenizer=tokenizer, max_seq_len=128, data_dir=Path("../downstream-tasks/ner"), train_filename="train.txt", dev_filename=None, dev_split=0.1, test_filename=None, delimiter="\t", metric="seq_f1", label_list=ner_labels
    )

    # 3. Create a DataSilo that loads several datasets (train/dev/test), provides DataLoaders for them and calculates a few descriptive statistics of our datasets
    data_silo = DataSilo(processor=processor, batch_size=batch_size)

    # 4. Create an AdaptiveModel
    # a) which consists of a pretrained language model as a basis
    language_model = LanguageModel.load(lang_model, language='romanian')
    # b) and a prediction head on top that is suited for our task => NER
    prediction_head = TokenClassificationHead(num_labels=len(ner_labels))

    model = AdaptiveModel(
        language_model=language_model,
        prediction_heads=[prediction_head],
        embeds_dropout_prob=0.1,
        lm_output_types=["per_token"],
        device=device,
    )

    # 5. Create an optimizer
    model, optimizer, lr_schedule = initialize_optimizer(
        model=model,
        learning_rate=1e-5,
        n_batches=len(data_silo.loaders["train"]),
        n_epochs=n_epochs,
        device=device,
    )

    # 6. Feed everything to the Trainer, which keeps care of growing our model into powerful plant and evaluates it from time to time
    trainer = Trainer(
        model=model,
        optimizer=optimizer,
        data_silo=data_silo,
        epochs=n_epochs,
        n_gpu=n_gpu,
        lr_schedule=lr_schedule,
        evaluate_every=evaluate_every,
        device=device,
    )

    # 7. Let it grow
    trainer.train()

    # 8. Hooray! You have a model. Store it:
    save_dir = "saved_models/bert-romanian-ner"
    model.save(save_dir)
    processor.save(save_dir)


    # 9. Load it & harvest your fruits (Inference)
    basic_texts = [
        {"text": "Popescu Ion merge la Cluj"},
        {"text": "Andrada s-a mutat in Berlin de 2 ani"},
    ]
    model = Inferencer.load(save_dir)
    result = model.inference_from_dicts(dicts=basic_texts)
    print(result)


if __name__ == "__main__":
    ner()