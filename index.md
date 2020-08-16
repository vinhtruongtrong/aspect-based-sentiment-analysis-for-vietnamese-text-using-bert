# Aspect based sentiment analysis for Vietnamese text using BERT

You can download **VLSP 2018 dataset** [following this page](https://vlsp.org.vn/resources-vlsp2018).  
**BERT base pre-train model** [following this page](https://github.com/google-research/bert). 
**Pho-BERT pre-train model** [following this page](https://github.com/VinAIResearch/PhoBERT). 

This project is run on Google Colab environment. 

Before run project you must install some ensential packages by run this script:
```
pip install -r requirements.txt
```
## Generate data
```
python generator.py --data_path [raw data path] --output_path [output path] --domain [domain]
```
- **[raw data path]**: directory of your VLSP 2018 dataset (file *.txt)
- **[output path]**: directory when save data that use to train phase (file *.csv)
- **[domain]**: restaurant or hotel, to generate auxiliary sentences base on number of corresponding aspect

## Training
### Prepare dataset path
Before training we copy dataset ([train], [test], [dev]) into one folder and rename it following this rule:  
```
[name]_[method].csv
```
with:  
- **[name]** is train, test or dev
- **[method]** is QA_M, QA,B, NLI_M, NLI_B
for example you want train with method QA_M, your dataset file with look like
```
dataset
  train_QA_M.csv
  dev_QA_M.csv
  test_QA_M.csv
```
### Train phase
run this script to train with BERT base pre-train model
```
python run_classifier_TABSA.py \
--task_name [task name] \
--data_dir [directory of data] \
--vocab_file [vocab.txt file of pre-train model] \
--bert_config_file [bert_config.json file] \
--init_checkpoint [init check point] \
--do_save_model \
--eval_test \
--do_lower_case \
--max_seq_length [max sequence length] \
--train_batch_size [bath size] \
--learning_rate 2e-5 \
--num_train_epochs [epochs] \
--output_dir [directory of result] \
--seed 42
```
run this script to train with Pho-BERT pre-train model
```
python run_classifier_RoBERTa_TABSA.py \
--task_name [task name] \
--data_dir [directory of data] \
--vocab_file [vocab.txt file of pre-train model] \
--bert_config_file [bert_config.json file] \
--init_checkpoint [init check point] \
--do_save_model \
--eval_test \
--do_lower_case \
--max_seq_length [max sequence length] \
--train_batch_size [bath size] \
--learning_rate 2e-5 \
--num_train_epochs [epochs] \
--output_dir [directory of result] \
--seed 42
```
_Train phase may throw exception if the result directory was exist_

## Evaluation
While train phase it will create result file (*.txt) after each epoch. 
Run this script to evaluate result
```
python evaluation.py \
--task_name [task name] --true_data_dir [true label directory] \
--pred_data_dir [predict label file *.txt] \
--domain [domain]
```
## Contact

Having trouble with project? Post it on issues or contact this email: vinh.truongtrong@gmail.com and i’ll help you sort it out.
