import re
import numpy as np
import pandas as pd
from text_pre_processing.method.qam import QA_M
from text_pre_processing.method.qab import QA_B
from text_pre_processing.method.nlim import NLI_M
from text_pre_processing.method.nlib import NLI_B
import progressbar


class AuxiliarySentenceMaker(object):
    def __init__(self, domain):
        self.domain = domain
        print("---auxiliarySentenceMaker initialized---")

    def make_auxiliary_sentences(self, dataframe, filename):
        qa_m_generator = QA_M(self.domain)
        qa_b_generator = QA_B(self.domain)
        nli_m_generator = NLI_M(self.domain)
        nli_b_generator = NLI_B(self.domain)

        bar = progressbar.ProgressBar(maxval=100, \
            widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        bar.start()

        qa_m = qa_m_generator.generate_data_frame(dataframe)
        bar.update(25)

        qa_b = qa_b_generator.generate_data_frame(dataframe)
        bar.update(50)

        nli_m = nli_m_generator.generate_data_frame(dataframe)
        bar.update(75)

        nli_b = nli_b_generator.generate_data_frame(dataframe)
        bar.update(100)

        print(filename)

        return {
            'qa_m' : qa_m,
            'qa_b' : qa_b,
            'nli_m' : nli_m,
            'nli_b' : nli_b,
        }