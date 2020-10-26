import re
import numpy as np
import pandas as pd
from text_pre_processing.method.base_method import BaseMethod

class QA_M(BaseMethod):
    def generate_QA_M(self, val):
        result = []
        for aspect in self.aspect_categories:
            question = 'bạn nghĩ thế_nào về '+ self.aspect_categories[aspect] + ' ?'
            sentiment = self.labels_categories['none']
            labels = self.get_labels(val[2])
            for l in labels:
                if(l[0] == aspect):
                    sentiment = self.labels_categories[l[1]]
            result.append([val[0], sentiment ,question, val[1]])
        return result

    def generate_data_frame(self, dataframe):
        gen_data = []
        for item in dataframe.values:
            gen_data.append(self.generate_QA_M(item))
        
        gen_data_numpy_array = np.array(gen_data)
        gen_data_numpy_array = gen_data_numpy_array.reshape(gen_data_numpy_array.shape[0]*gen_data_numpy_array.shape[1]
                                                            , gen_data_numpy_array.shape[2])
        d = pd.DataFrame(gen_data_numpy_array, columns = ['id', 'sentiment', 'question', 'sentence'])
        return d