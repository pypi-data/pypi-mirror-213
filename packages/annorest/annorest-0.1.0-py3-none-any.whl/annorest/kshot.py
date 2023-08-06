import json
import os
import pandas as pd

"""
This script is used to generate k-shot data for Inverse
"""
# Arguments
RANDOM_SEED = 42
# REPLACE = True # Whether to sample with replacement True：取出的樣本可以再放回去，False：取出的樣本不能再放回去

# 進階設定
BIO_PREFIX = ['B-', 'I-', 'S-']

def flatten(l):
    return [item for sublist in l for item in sublist]


def remove_BIO_prefix(label_list):
    """
    Remove BIO prefix from label list
    Input: ['B-ORG', 'I-ORG','I-ORG','I-ORG']
    Output: ['ORG', 'ORG','ORG','ORG']
    """
    label = []
    for single_label in label_list:
        if single_label[:2] in BIO_PREFIX:
            label.append(single_label[2:])
        else:
            label.append(single_label)
    return label
    
def get_unique_label_list(data, remove_bio_prefix=True):
    label_list = []
    for single_doc in data:
        if(remove_bio_prefix):
            label_list.append(remove_BIO_prefix(single_doc['label']))
        else:
            label_list.append(single_doc['label'])
    label_list = list(dict.fromkeys((flatten(label_list))))
    if 'O' in label_list:
        label_list.remove('O')
    return label_list

def get_support_df(data_converted, unique_label_list):
    label_docs = []
    for doc in data_converted:
        d_label_set = set(remove_BIO_prefix(doc['label']))
        label_docs.append([1 if x in d_label_set else 0 for x in unique_label_list])
    label_df = pd.DataFrame(label_docs, columns=unique_label_list)
    return label_df

def get_k_shot_idx(k_shot, support_df, replace=True):
        sampled_ind = []
        for l in unique_label_list:
            try:
                sampled_ind+=support_df[support_df[l]==1].sample(k_shot, random_state=RANDOM_SEED, replace=replace).index.to_list()
            except Exception as e:
                # print("error when sampling k_shot: " + str(k_shot))
                # print(l)
                # print(e.args)
                raise
        sampled_ind = list(set(sampled_ind))
        len(sampled_ind)
        return sampled_ind

def caculate_test_statistic(test_data, unique_label_list, shot_count):
    test_label_docs = []
    for doc in test_data:
        d_label_set = set(remove_BIO_prefix(doc['label']))
        # print(d_label_set)
        test_label_docs.append([1 if x in d_label_set else 0 for x in unique_label_list])
        # print([x for x in unique_label_list])
        # break
    test_label_df = pd.DataFrame(test_label_docs, columns=unique_label_list)
    return test_label_df

def main(data_converted, k=5, custom_unique_label_list=None, print_log=True, replace=True):
    """
    Input format:
        data_converted = [
            {
                'text': ['比','亚','迪','半','导','体'],
                'label': ['B-ORG', 'I-ORG','I-ORG','I-ORG','I-ORG','I-ORG']
            },
        ]
        k: k-shot
        custom_unique_label_list: if you want to use custom unique label list, you can pass it in
    
    Output format:
        k_shot_data = [
            {
                'text': ['比','亚','迪','半','导','体'],
                'label': ['B-ORG', 'I-ORG','I-ORG','I-ORG','I-ORG','I-ORG']
            },
        ]
        test_data = [
            {
                'text': ['比','亚','迪','半','导','体'],
                'label': ['B-ORG', 'I-ORG','I-ORG','I-ORG','I-ORG','I-ORG']
            },
        ]
    """
    global unique_label_list
    if custom_unique_label_list is not None:
        unique_label_list = custom_unique_label_list
    else:
        unique_label_list = get_unique_label_list(data_converted)
    
    support_df = get_support_df(data_converted, unique_label_list)
    sampled_ind = get_k_shot_idx(k, support_df, replace)

    k_shot_data = [data for idx, data in enumerate(data_converted) if idx in sampled_ind]
    test_data = [data for idx, data in enumerate(data_converted) if idx not in sampled_ind]

    assert len(k_shot_data) == len(sampled_ind)
    assert len(test_data) == len(data_converted) - len(sampled_ind)
    if print_log:
        print("=====", k, " shots setting =====")
        print(str(k) + ' shot design size: ' + str(k * len(unique_label_list)))
        print(str(k) + ' shot data size: ' + str(len(k_shot_data)))
        print(str(k) + ' test data size: ' + str(len(test_data)))
        
    return k_shot_data, test_data

if __name__ == "__main__":
    pass
    # main(data_converted)