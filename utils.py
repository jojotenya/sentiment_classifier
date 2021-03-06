import numpy as np
import keras
import argparse
GO_ID = 0
EOS_ID = 1
UNK_ID = 2
SPLIT_DIMS = [5,5,3]
MAX_LEN = SPLIT_DIMS[0]*SPLIT_DIMS[1]*SPLIT_DIMS[2]
batch_size = 128

parser = argparse.ArgumentParser()
parser.add_argument("--data_path", default=None, dest="d")
parser.add_argument("--mapping_path", default="data/char_mapping", dest="m", help="mapping path")
parser.add_argument("--model_path", default="saved_models/Model07", dest="s", help="trained models directory")
parser.add_argument("--log_path", dest="l", help="log path record mean score")
args = parser.parse_args()
print(args)


with open(args.m,"r") as f:
    vocab_dict = dict([(row.strip(),i) for i,row in enumerate(f.readlines())])

def text_to_sequence(row):
    row = [r for r in row]
    row = list(map(lambda x:vocab_dict.get(x,UNK_ID),row))
    row = [GO_ID] + row
    row.append(EOS_ID)
    return row

def texts_to_sequences(rows):
    return list(map(lambda row:text_to_sequence(row),rows))

def pad_sequence(tokens,maxlen):
    pad_num = maxlen - len(tokens)
    tokens += [EOS_ID]*pad_num
    return tokens

def pad_sequences(tokens_list,maxlen):
    return np.array(list(map(lambda tokens:pad_sequence(tokens,maxlen),tokens_list)))

def get_split_list(arr,dims): 
    arrs = []
    for i in range(arr.shape[0]):
        split1=np.split(np.array(arr[i]),dims[2])
        a=[]
        for j in range(dims[2]):
            s=np.split(split1[j],dims[1])
            a.append(s)
        arrs.append(a)
    return arrs

def cal_score(s):
    idx = np.argmax(s)
    return idx*s[idx]

def cal_scores(scores):
    return list(map(lambda x:cal_score(x),scores))
