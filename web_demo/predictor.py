import numpy as np
import torch
import torch.nn.functional as F
from processor import VLSP_2018_QA_M_Processor
import tokenization
from modeling import BertConfig, BertForSequenceClassification
from text_pre_processing.text_pre_processing import TextPreProcessing
from tqdm import tqdm, trange
import run_classifier_TABSA
from text_pre_processing.method.qam import QA_M
from processor import InputExample

class InputFeatures(object):
    def __init__(self, input_ids, input_mask, segment_ids):
        self.input_ids = input_ids
        self.input_mask = input_mask
        self.segment_ids = segment_ids

class Predictor(object):
    def __init__(self):
        torch.manual_seed(42)
        self.bert_config = BertConfig.from_json_file('/Users/vinhtruongtrong/Downloads/drive-download-20201015T092207Z-001/bert_config.json')
        self.processor = VLSP_2018_QA_M_Processor()
        self.label_list = self.processor.get_labels()
        self.tokenizer = tokenization.FullTokenizer(
            vocab_file='/Users/vinhtruongtrong/Downloads/drive-download-20201015T092207Z-001/vocab.txt', do_lower_case=False)
        self.device = torch.device("cuda" if torch.cuda.is_available() and not args.no_cuda else "cpu")
        self.model = BertForSequenceClassification(self.bert_config, len(self.label_list))
        self.model.load_state_dict(torch.load('/Users/vinhtruongtrong/Downloads/drive-download-20201015T092207Z-001/model.bin', map_location='cpu'))
        self.model.to(self.device)
        self.model.eval()
    
    def generate_QA_M(self, val, domain):
        result = []
        for aspect in QA_M(domain).aspect_categories:
            question = 'bạn nghĩ thế_nào về '+ QA_M(domain).aspect_categories[aspect] + ' ?'
            result.append([question, val])
        return result
    
    def create_examples(self, lines, set_type = 'test'):
        examples = []
        for (i, line) in enumerate(lines):
            guid = "%s-%s" % (set_type, i)
            text_a = tokenization.convert_to_unicode(str(line[1]))
            text_b = tokenization.convert_to_unicode(str(line[0]))
            if i%1000==0:
                print(i)
                print("guid=",guid)
                print("text_a=",text_a)
            examples.append(
                InputExample(guid=guid, text_a=text_a, text_b=text_b))
        return examples
    def convert_examples_to_features(self, examples, max_seq_length, tokenizer):
    
        features = []
        for (ex_index, example) in enumerate(tqdm(examples)):
            tokens_a = tokenizer.tokenize(example.text_a)

            tokens_b = None
            if example.text_b:
                tokens_b = tokenizer.tokenize(example.text_b)

            if tokens_b:
                self._truncate_seq_pair(tokens_a, tokens_b, max_seq_length - 3)
            else:
                if len(tokens_a) > max_seq_length - 2:
                    tokens_a = tokens_a[0:(max_seq_length - 2)]

            tokens = []
            segment_ids = []
            tokens.append("[CLS]")
            segment_ids.append(0)
            for token in tokens_a:
                tokens.append(token)
                segment_ids.append(0)
            tokens.append("[SEP]")
            segment_ids.append(0)

            if tokens_b:
                for token in tokens_b:
                    tokens.append(token)
                    segment_ids.append(1)
                tokens.append("[SEP]")
                segment_ids.append(1)

            input_ids = tokenizer.convert_tokens_to_ids(tokens)

            input_mask = [1] * len(input_ids)

            while len(input_ids) < max_seq_length:
                input_ids.append(0)
                input_mask.append(0)
                segment_ids.append(0)

            features.append(
                    InputFeatures(
                            input_ids=input_ids,
                            input_mask=input_mask,
                            segment_ids=segment_ids))
        return features


    def _truncate_seq_pair(self, tokens_a, tokens_b, max_length):
        while True:
            total_length = len(tokens_a) + len(tokens_b)
            if total_length <= max_length:
                break
            if len(tokens_a) > len(tokens_b):
                tokens_a.pop()
            else:
                tokens_b.pop()
    
    def create_sample(self, sentence, domain = 'restaurant', method = 'QA_M'):
        text_processing = TextPreProcessing()
        sentence = text_processing.sentence_pre_processing(sentence)
        auxilary_sentences = self.generate_QA_M(sentence, domain) if method == 'QA_M' else None

        test_examples = self.create_examples(auxilary_sentences)
        test_features = self.convert_examples_to_features(test_examples, 128, self.tokenizer)

        all_input_ids = torch.tensor([f.input_ids for f in test_features], dtype=torch.long)
        all_input_mask = torch.tensor([f.input_mask for f in test_features], dtype=torch.long)
        all_segment_ids = torch.tensor([f.segment_ids for f in test_features], dtype=torch.long)

        test_data = run_classifier_TABSA.TensorDataset(all_input_ids, all_input_mask, all_segment_ids)
        test_dataloader = run_classifier_TABSA.DataLoader(test_data,batch_size=len(test_features), shuffle=False)

        return test_dataloader
    
    def predict(self, sentence, domain = 'restaurant', method = 'QA_M'): 
        test_dataloader = self.create_sample(sentence, domain, method)
        self.model.eval()
        ouputs = None
        for input_ids, input_mask, segment_ids in test_dataloader:
            input_ids = input_ids.to(self.device)
            input_mask = input_mask.to(self.device)
            segment_ids = segment_ids.to(self.device)

            with torch.no_grad():
                logits = self.model(input_ids, segment_ids, input_mask)

            logits = F.softmax(logits, dim=-1)
            logits = logits.detach().cpu().numpy()
            outputs = np.argmax(logits, axis=1)

        return outputs
    
    def multiple_output_post_processing(self, outputs):
        result = {}
        aspect_categories = QA_M('restaurant').aspect_categories
        for (index, value) in enumerate(aspect_categories):
            if(outputs[index] != 3):
                result[aspect_categories[value]] = self.label_list[outputs[index]]
                # result.append([aspect_categories[value], self.label_list[outputs[index]]])
        return result