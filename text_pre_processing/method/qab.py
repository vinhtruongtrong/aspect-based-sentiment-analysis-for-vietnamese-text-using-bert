import re
import numpy as np
import pandas as pd
from text_pre_processing.method.base_method import BaseMethod

class QA_B(BaseMethod):
    # def __init__(self):
    #     self.aspect_categories = {
    #             'FOOD#STYLE&OPTIONS': 'phong_cách đồ_ăn', 
    #             'FOOD#QUALITY': 'chất_lượng đồ_ăn', 
    #             'AMBIENCE#GENERAL' : 'cảnh_quan',
    #             'RESTAURANT#GENERAL' : 'tổng_thể', 
    #             'SERVICE#GENERAL' : 'dịch_vụ', 
    #             'FOOD#PRICES' : 'giá thức_ăn',
    #             'RESTAURANT#PRICES' : 'giá tổng_thể', 
    #             'LOCATION#GENERAL' : 'vị_trí', 
    #             'RESTAURANT#MISCELLANEOUS' : 'khác',
    #             'DRINKS#STYLE&OPTIONS' : 'phong_cách nước', 
    #             'DRINKS#PRICES' : 'giá nước', 
    #             'DRINKS#QUALITY' : 'chất_lượng nước'
    #         }
    #     self.labels_categories = {
    #             'positive' : 'tích_cực',
    #             'negative': 'tiêu_cực',
    #             'neutral' : 'trung_lập',
    #             'none' : 'không_có'
    #         }
    
    def generate_QM_B(self, val):
        result = []
        labels = self.get_labels(val[2])
        aspects = [i[0] for i in labels]
        for aspect in self.aspect_categories:
            item = []
            if(aspect in aspects):
                for label in self.labels_categories:
                    question = 'khía_cạnh {} là {} .'.format(self.aspect_categories[aspect], self.labels_categories[label])
                    sentiment = '0'
                    for l in labels:
                        if(l[0] == aspect and l[1] == label):
                            sentiment = '1'
                    item.append([val[0], sentiment ,question, val[1]])
            else:
                for label in self.labels_categories:
                    question = 'khía_cạnh {} là {} .'.format(self.aspect_categories[aspect], self.labels_categories[label])
                    sentiment = '1' if label == 'none' else '0'
                    item.append([val[0], sentiment ,question, val[1]])
            result.append(item)
        return result
    
    def generate_data_frame(self, dataframe):
        gen_data = []
        for item in dataframe.values:
            gen_data.append(self.generate_QM_B(item))
            
        gen_data_numpy_array = np.array(gen_data)
        gen_data_numpy_array = gen_data_numpy_array.reshape(gen_data_numpy_array.shape[0]*gen_data_numpy_array.shape[1]*gen_data_numpy_array.shape[2]
                                                            , gen_data_numpy_array.shape[3])
        d = pd.DataFrame(gen_data_numpy_array, columns = ['id', 'sentiment', 'question', 'sentence'])
        return d
        