import argparse
import collections

import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.preprocessing import label_binarize
from sklearn.metrics import f1_score

def vlsp_2018_PRF(y_true, y_pred, domain):
    """
    Calculate "Micro P R F" of aspect detection task of VLSP-2018.
    """
    s_all=0
    g_all=0
    s_g_all=0
    
    total_available_aspects = 12 if domain == 'restaurant' else 34

    for i in range(len(y_pred)//total_available_aspects):
        s=set()
        g=set()
        for j in range(total_available_aspects):
            if y_pred[i*total_available_aspects+j]!=3:
                s.add(j)
            if y_true[i*total_available_aspects+j]!=3:
                g.add(j)
        if len(g)==0:continue
        #get all index != 3 (None) then intersection 2 list
        s_g=s.intersection(g)
        s_all+=len(s)
        g_all+=len(g)
        s_g_all+=len(s_g)

    p=s_g_all/s_all
    r=s_g_all/g_all
    f=2*p*r/(p+r)

    return p,r,f

def get_y_true(task_name, true_data_dir):
    """ 
    Read file to obtain y_true.
    All of five tasks of VLSP 2018 use the test set of task-BERT-pair-NLI-M to get true labels.
    """

    df = pd.read_csv(true_data_dir,sep='\t',header=None).values
    y_true=[]
    for i in range(len(df)):
        label = df[i][1]
        assert label in ['tích_cực', 'trung_lập', 'tiêu_cực', 'không_có'], "error!"
        if label == 'tích_cực':
            n = 0
        elif label == 'trung_lập':
            n = 1
        elif label == 'tiêu_cực':
            n = 2
        elif label == 'không_có':
            n = 3
        y_true.append(n)
    
    return y_true


def get_y_pred(task_name, pred_data_dir):
    """ 
    Read file to obtain y_pred and scores.
    """
    pred=[]
    score=[]
    if task_name in ["vlsp_2018_NLI_M", "vlsp_2018_QA_M"]:
        with open(pred_data_dir,"r",encoding="utf-8") as f:
            s=f.readline().strip().split()
            while s:
                pred.append(int(s[0]))
                score.append([float(s[1]), float(s[2]), float(s[3]), float(s[4])])
                s = f.readline().strip().split()
    elif task_name in ["vlsp_2018_NLI_B", "vlsp_2018_QA_B"]:
        count = 0
        tmp = []
        with open(pred_data_dir, "r", encoding="utf-8") as f:
            s = f.readline().strip().split()
            while s:
                tmp.append([float(s[2])])
                count += 1
                if count % 4 == 0:
                    tmp_sum = np.sum(tmp)
                    t = []
                    for i in range(4):
                        t.append(tmp[i] / tmp_sum)
                    score.append(t)
                    if t[0] >= t[1] and t[0] >= t[2] and t[0]>=t[3]:
                        pred.append(0)
                    elif t[1] >= t[0] and t[1] >= t[2] and t[1]>=t[3]:
                        pred.append(1)
                    elif t[2] >= t[0] and t[2] >= t[1] and t[2]>=t[3]:
                        pred.append(2)
                    else:
                        pred.append(3)
                    tmp = []
                s = f.readline().strip().split()
    else: 
        print('Has not implement for single choice method')

    return pred, score


def vlsp_2018_Acc(y_true, y_pred, score, classes=3):
    """
    Calculate "Acc" of sentiment classification task of VLSP 2018.
    """
    assert classes in [2, 3], "classes must be 2 or 3."

    if classes == 3:
        total=0
        total_right=0
        for i in range(len(y_true)):
            if y_true[i]==3:continue
            total+=1
            tmp=y_pred[i]
            if tmp>=3:
                if score[i][0]>=score[i][1] and score[i][0]>=score[i][2]:
                    tmp=0
                elif score[i][1]>=score[i][0] and score[i][1]>=score[i][2]:
                    tmp=1
                else:
                    tmp=2
            if y_true[i]==tmp:
                total_right+=1
        sentiment_Acc = total_right/total
    else:
        total=0
        total_right=0
        for i in range(len(y_true)):
            if y_true[i]>=3 or y_true[i]==1:continue
            total+=1
            tmp=y_pred[i]
            if tmp>=3 or tmp==1:
                if score[i][0]>=score[i][2]:
                    tmp=0
                else:
                    tmp=2
            if y_true[i]==tmp:
                total_right+=1
        sentiment_Acc = total_right/total

    return sentiment_Acc


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--task_name",
                        default=None,
                        type=str,
                        required=True,
                        choices=["vlsp_2018_single", \
                                "vlsp_2018_NLI_M", "vlsp_2018_QA_M", "vlsp_2018_NLI_B", "vlsp_2018_QA_B"],
                        help="The name of the task to evalution.")

    parser.add_argument("--true_data_dir",
                        default=None,
                        type=str,
                        required=True,
                        help="The pred data dir.")

    parser.add_argument("--pred_data_dir",
                        default=None,
                        type=str,
                        required=True,
                        help="The pred data dir.")

    parser.add_argument("--domain",
                        default=None,
                        type=str,
                        required=True,
                        choices=['restaurant', 'hotel'],
                        help="domain")                    
    args = parser.parse_args()


    result = collections.OrderedDict()

    y_true = get_y_true(args.task_name, args.true_data_dir)
    y_pred, score = get_y_pred(args.task_name, args.pred_data_dir)
    aspect_P, aspect_R, aspect_F = vlsp_2018_PRF(y_true, y_pred, args.domain)
    sentiment_Acc_3_classes = vlsp_2018_Acc(y_true, y_pred, score, 3)
    f1_micro = f1_score(y_true, y_pred, average='micro')
    f1_macro = f1_score(y_true, y_pred, average='macro')


    result = {
            'aspect_P': aspect_P,
            'aspect_R': aspect_R,
            'aspect_F': aspect_F,
            'sentiment_accuracy': sentiment_Acc_3_classes,
            'f1': f1_micro,
            'f1_macro': f1_macro
    }

    for key in result.keys():
        print(key, "=",str(result[key]))
    

if __name__ == "__main__":
    main()
