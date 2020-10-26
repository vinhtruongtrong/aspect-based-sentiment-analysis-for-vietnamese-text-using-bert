import re
import numpy as np
import pandas as pd
from text_pre_processing.method.base_method import BaseMethod

class NLI_B(BaseMethod):
    def generate_NLI_B(self, val):
        result = []
        labels = self.get_labels(val[2])
        aspects = {}
        for i in labels:
            aspects[i[0]]=i[1]
            
        for aspect in self.aspect_categories:
            item = []
            if(aspect in aspects):
                label_of_match_aspect = aspects[aspect]
                for l in self.labels_categories:
                    w = '0'
                    pair = '{} - {}'.format(self.labels_categories[l], self.aspect_categories[aspect])
                    if(l == label_of_match_aspect):
                        w = '1'
                    item.append([val[0], w, pair, val[1]])
            else:
                for l in self.labels_categories:
                    w = '0'
                    pair = '{} - {}'.format(self.labels_categories[l], self.aspect_categories[aspect])
                    if(l == 'none'):
                        w = '1'
                    item.append([val[0], w, pair, val[1]])
            result.append(item)
        return result
    
    def generate_data_frame(self, dataframe):
        gen_data = []
        for item in dataframe.values:
            gen_data.append(self.generate_NLI_B(item))
            
        gen_data_numpy_array = np.array(gen_data)
        gen_data_numpy_array = gen_data_numpy_array.reshape(gen_data_numpy_array.shape[0]*gen_data_numpy_array.shape[1]*gen_data_numpy_array.shape[2]
                                                            , gen_data_numpy_array.shape[3])
        d = pd.DataFrame(gen_data_numpy_array, columns = ['id', 'label', 'aspect', 'sentence'])
        return d