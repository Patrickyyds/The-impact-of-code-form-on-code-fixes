# The-impact-of-code-form-on-code-fixes
An Extension experiment on the CURE project.[CURE: Code-Aware Neural Machine Translation for Automatic Program Repair](https://www.cs.purdue.edu/homes/lintan/publications/cure-icse21.pdf)

# This project made some modifications on the basis of the CURE project, including adding the code representations of AST and CFG, and studying the influence of different representations on the effectiveness of code repair.

## File Structure
* **results**: This folder contains all the QuixBugs benchmarks that CURE fixed. Each file contains the buggy line, CURE's patch and the developer's patch
* **candidate_patches**: This folder contains all the candidate patches CURE generated for bugs in each benchmark
* **data**: This folder contains the vocabulary file, subword tokenizer, some training data examples, and the GPT PL model pre-trained on code.
  * **vocabulary**
    * subword.txt: the subword tokenizer model needed by subword-nmt
    * vocabulary.txt: the vocabulary file used in CURE's paper
  * **models**: This folder is used to save the models
    * code_gpt.pt: the save GPT PL model trained on code:https://zenodo.org/record/7030145#.YwvXfFvMI5l
  * **patches**: This folder is used to save the generated patches
  * **data**: This folder is used to save the training data and validation data
    * CURE uses the source code training data shared by previous work [CoCoNuT](https://github.com/lin-tan/CoCoNut-Artifact)
* **src**: This folder includes the source code for CURE's APR model

## Dependency
* Python 3.8
* PyTorch 1.4.0  (details:[torch-1.4.0-cp38-cp38-linux_x86_64.whl])
* gensim 4.3.0
* NumPy 1.18.1
* Huggingface transformers 2.10.0
* subword-nmt

## My additional content
**Python file that changes the form of code**
  * data/data/prepare_training_data.py
  * data/data/prepare_training_data_ast.py
  * data/data/prepare_training_data_cfg.py
**Python file that converts code into vectors**
  * src/dataloader/change_forms.py
  * src/dataloader/tokenization.py
  * src/dataloader/word_dataloader.py

## Usage
**To change code forms**,run `data/data/prepare_training_data.py`,`data/data/prepare_training_data_ast.py`
Some settings you may need to change:
  * training_src.txt : the source training data needed by the model
  * validation_src.txt : test set data required by the model.

**To train a GPT-CoNuT model**, run `src/trainer/gpt_conut_trainer.py`
Some settings you may need to change:
  * vocab_file: the path to the vocabulary file used by the model
  * train_file: the path to the training data
  * valid_file: the path to the validation data
  * gpt_file: the path to the saved GPT PL model
  * hyper_parameter: the hyper-parameter of the model (including the number of encoder/decoder layers, dropout rate, etc.)
  * save_dir: the directory to save the model, default: data/models/

**To train a GPT-FConv model**, run `src/trainer/gpt_fconv_trainer.py`
Some settings you may need to change:
  * CURE's trained models: https://zenodo.org/record/7030145#.YwvXfFvMI5l
  * vocab_file: the path to the vocabulary file used by the model
  * train_file: the path to the training data
  * valid_file: the path to the validation data
  * gpt_file: the path to the saved GPT PL model
  * hyper_parameter: the hyper-parameter of the model (including the number of encoder/decoder layers, dropout rate, etc.)
  * save_dir: the directory to save the model, default: data/models/

**To prepare input for new test data**, check `data/data/prepare_testing_data.py`, make sure you check the readme file and follow the three steps to prepare the test input.

**To generate patches**, run `src/tester/generator.py`
Some settings you may need to change:
  * CURE's trained models: https://zenodo.org/record/7030145#.YwvXfFvMI5l
  * run 'src/dataloader/word_dataloader.py' and 'src/dataloader/tokenization.py' to change the code to vectors
  * vocab_file: the path to the vocabulary file used by the model
  * input_file: the input data to the model for generating patches, with each line referring to a bug in the following format: `buggy line <CTX> surrounding function`. see `candidate_patches/QuixBugs/quixbugs_bpe.txt` for reference. 
  * identifier_txt_file: the valid identifiers for each bug, with each line being a list of valid identifiers, identifiers are split by space. see `candidate_patches/QuixBugs/identifier.txt` for reference
  * identifier_token_file: the tokenized identifiers for each bug, with each line being a list of valid identifiers tokenized by camel letter, underscore, and subword. identifiers are split by `\t`. see `candidate_patches/QuixBugs/identifier.tokens` for reference
  * output_file: the path to the output result
  * beam_size: the number of candidate patches generated by each model
  * model_file: the path to the saved APR model

**To validate the candidate patches generated by models**, run `src/validation/rerank.py`, which will rerank the patches generated by all the models and the result will be dumped into `data/patches/reranked_patches.json`
