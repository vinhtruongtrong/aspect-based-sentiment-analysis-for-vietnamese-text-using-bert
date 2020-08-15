import glob
import argparse
import pandas as pd
import re
import os
from text_pre_processing.text_pre_processing import TextPreProcessing
from text_pre_processing.auxiliary_sentence_maker import AuxiliarySentenceMaker


class GeneratorDataSet(object):    
    def __init__(self, data_path, output_path, domain):
        self.data_path = data_path
        self.output_path = output_path
        self.domain = domain

    def read_txt_file(self, files):
        data = []
        for file in files:
            with open(file,encoding='utf-8') as f:
                val = list(filter(None, [w.strip() for w in f.readlines()]))
                data.append(val)
        return data
    
    def txt_to_record(self, txt_data):
        output = []
        for data in txt_data:
            records = []
            for i in range(0, len(data),3):
                records.append([data[i], data[i+1], data[i+2]])
            output.append(records)
        return output

    def get_all_category_in_data_frame(self, targetLabels):
        categories = []
        for multiLabels in targetLabels:
            for label in multiLabels:
                if(label not in categories):
                    categories.append(label)
        return categories

    def records_to_data_frame(self, records):
        aspect = [item[2] for item in records]
        
        patern = r'\w*#\w*&*\w*\,\s*\w*'
        aspect = [re.findall(patern,item) for item in aspect]
        aspect = [[re.split(r', ',subItem) for subItem in item] for item in aspect]
        
        df = pd.DataFrame(records, columns =['Id', 'Review', 'Label'])
        df.Result = aspect
        
        df['Aspect'] = [[subItem[0] for subItem in item] for item in df.Result]
        df['Sentiment'] = [[subItem[1] for subItem in item] for item in df.Result]
            
        df['Review'] = df['Review']        
        return df

    def generate_data(self):
        print("starting...")

        files = glob.glob("{}/*.txt".format(self.data_path))
        print(str(files))

        txt_data = self.read_txt_file(files)
        records = self.txt_to_record(txt_data)

        df_list = []
        for record in records:
            df_list.append(self.records_to_data_frame(record))
        
        directory = "{}/clean_data/{}".format(self.output_path, self.domain)
        if not os.path.exists(directory):
            os.makedirs(directory)
        

        qa_m_directory = "{}/{}/qa_m".format(directory, self.domain)
        if not os.path.exists(qa_m_directory):
            os.makedirs(qa_m_directory)

        qa_b_directory = "{}/{}/qa_b".format(directory, self.domain)
        if not os.path.exists(qa_b_directory):
            os.makedirs(qa_b_directory)

        nli_m_directory = "{}/{}/nli_m".format(directory, self.domain)
        if not os.path.exists(nli_m_directory):
            os.makedirs(nli_m_directory)

        nli_b_directory = "{}/{}/nli_b".format(directory, self.domain)
        if not os.path.exists(nli_b_directory):
            os.makedirs(nli_b_directory)

        text_processing = TextPreProcessing()
        auxiliary_maker = AuxiliarySentenceMaker(self.domain)
        
        clean_data = text_processing.start_pre_processing(df_list)
        for i in range(len(clean_data)):
            clean_data[i].to_csv(str('{}/{}.csv'.format(directory, os.path.basename(files[i]))), index=False, encoding="utf-8-sig")
            generated_data = auxiliary_maker.make_auxiliary_sentences(clean_data[i], os.path.basename(files[i]))
            generated_data['qa_m'].to_csv(str('{}/{}.csv'.format(qa_m_directory, os.path.basename(files[i]))), index=False, encoding="utf-8-sig")
            generated_data['qa_b'].to_csv(str('{}/{}.csv'.format(qa_b_directory, os.path.basename(files[i]))), index=False, encoding="utf-8-sig")
            generated_data['nli_m'].to_csv(str('{}/{}.csv'.format(nli_m_directory, os.path.basename(files[i]))), index=False, encoding="utf-8-sig")
            generated_data['nli_b'].to_csv(str('{}/{}.csv'.format(nli_b_directory, os.path.basename(files[i]))), index=False, encoding="utf-8-sig")

        print("completed")     
        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path",
                        default=None,
                        type=str,
                        required=True,
                        help="raw data folder path")
    parser.add_argument("--output_path",
                        default=None,
                        type=str,
                        required=True,
                        help="output folder path")
    parser.add_argument("--domain",
                        default=None,
                        type=str,
                        required=True,
                        help="domain",
                        choices=["restaurant","hotel"])

    args = parser.parse_args()
    generator = GeneratorDataSet(args.data_path, args.output_path, args.domain)
    generator.generate_data()

if __name__ == "__main__":
    main()