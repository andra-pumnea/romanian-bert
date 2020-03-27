# Training Romanian Bert from scratch

In this experiment we have fine-tuned several language models with [FARM](https://github.com/deepset-ai/FARM) on the [Ronec dataset](https://github.com/dumitrescustefan/ronec), which provides a NER Romanian task. The authors of the dataset report **0.82 F1** score when training a Spacy model, where 0.1 of the dataset is used for testing. The same test set ratio was used in our experiments. The results are reported in the tabel below:


| Spacy         | Roberta-XLM   | mBert   | Distill mBert|
| ------------- |:-------------:| :-----: | ------------:|
| 0.82 F1       | 0.84 F1       | 0.80 F1 | 0.78 F1      |


The dataset is also discussed in the following paper: 
_Dumitrescu, Stefan Daniel, and Andrei-Marius Avram. "Introducing RONEC--the Romanian Named Entity Corpus." arXiv preprint arXiv:1909.01247 (2019)._
