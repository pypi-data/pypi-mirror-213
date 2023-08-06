import re
def flatten(l):
    """
    input: [[1,2,3],[4,5,6]]
    output: [1,2,3,4,5,6]
    """
    return [item for sublist in l for item in sublist]


def remove_BIO_prefix(label_list, custom_prefix=["B-", "I-", "S-"]):
    """
    input: ['B-LOC', 'I-LOC', 'O', 'B-PER', 'I-PER', 'O']
    output: ['LOC', 'LOC', 'O', 'PER', 'PER', 'O']
    """
    label = []
    for single_label in label_list:
        if single_label.startswith(tuple(custom_prefix)):
            label.append(single_label[2:])
        else:
            label.append(single_label)
    return label


def get_unique_label_list(data, remove_bio_prefix=True):
    """
    input: [{'label': ['B-LOC', 'I-LOC', 'O', 'B-PER', 'I-PER', 'O']}]
    output: ['LOC', 'PER']
    """
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


def get_unique_label_list_from_fastnlp(data, remove_bio_prefix=True, remove_O=True):
    """
    input: [{'target': ['B-LOC', 'I-LOC', 'O', 'B-PER', 'I-PER', 'O']}]
    output: ['LOC', 'PER']
    """
    all_label_list=flatten([i["target"] for i in data])
    if remove_bio_prefix:
        all_label_list=remove_BIO_prefix(all_label_list)
    # 轉換為unique list
    all_label_list = list(dict.fromkeys(all_label_list))
    if remove_O:
        if "O" in all_label_list:
            all_label_list.remove("O")

    return all_label_list



# keep separator and do not put separator as new element.
# def split_string_by_delimiter(str, pattern= ";,.\-\%。，\n\t", keep_delimiter = True, separate = False):
# s= "自從電動-車大廠特斯拉（Tesla）旗下的Model 3車款，於2018年導入以碳化矽（SiC）生產的功率元件——金屬氧化物半導體場效電晶體（MOSFET），使得功率轉換效率大增，也間接延長了電池續航力，不但帶動碳化矽這項材料重新受到業界關注，各種應用也持續發酵。\n「碳化矽的特性適合運用在功率2,000W（瓦）以上的高階電源應用，這一定是未來趨勢，只是看它（碳化矽市場）爆發得有多快。」強茂營運長陳佐銘表示。\n強茂為臺灣最大整流元件製造商，市佔全球第6。目前高達99％的營收是由一般矽材料產品所貢獻，在矽製程的二極體產品面，可以從晶片設計、晶圓製造，到封裝測試、市場行銷一手包辦，共擁有2座晶圓廠（位於中國山東和高雄永安）與3個封裝廠區（位於高雄岡山、江蘇徐州、江蘇無錫）。\n小辭典\n【二極體】Diode，如同控制電流的閥門，半導體的二極體大多使用矽基材生產，例如整流二極體，可將交流電轉變為直流電。  【功率元件】電子裝置的電能轉換與電路控制的核心；主要用途包括變頻、整流、變壓、功率放大等，應用於通訊、消費電子、新能源交通等。  【MOSFET】金屬氧化物半導體場效電晶體，為功率半導體元件，利用閘極電壓控制輸出電流的大小，以供應終端電子設備，常用於手機、筆電、行動電源等。\n強茂營運長_陳佐銘 圖/蔡仁譯攝影\n攜手上游材料商，以高CP服務助客戶升級\n根據法國市場研究機構Yole Développement預測，受到汽車電動化趨勢的帶動，碳化矽功率半導體市場2020年～2026年將以36％年複合成長率（CAGR）成長，屆時產值可望達45億美元。\n看好功率元件採用碳化矽的前景，成立超過30年的強茂，已於2019年起向國際大廠招攬人才，研發團隊裡也有約20％的人力，專注於開發碳化矽產品。2020年，強茂已量產第1代碳化矽二極管，主要針對工業電源、消費性電源、太陽能逆變器及能源轉換系統等非車規的應用領域；2021年預計營收可達1.25億元，並計畫於2022年量產第2代產品。\n「Gen 2（第2代）效率可提升15％，成本節省20％。」陳佐銘指出，當強茂的產品效能足以媲美國際大廠，也看好未來材料成本逐漸下降，「這樣成本就不會是我們吃虧的地方，高CP值加服務，就是我們的路線。」\n陳佐銘分析，目前碳化矽產品價格依然是矽基產品的7～8倍，但是「2025年之後，EV（純電動車）比例會非常高，到時候我們的產品成熟了，應用端也夠多元，預期（碳化矽元件）價格會往下走，⋯⋯如果能走到一半的價錢，甜蜜點就出現了。」\n到時候，強茂碳化矽產品的營收佔比，估計可以從目前的1％提升至5～8％。\n談到碳化矽未來的產品線規畫，陳佐銘說，「要打國際戰，車用就是主戰場！」強茂也訂於2023年1月之前，推出旗下第1代碳化矽金屬氧化物半導體場效電晶體（SiC MOSFET），鎖定電動車市場需求，「我們已經做好打這個仗的準備！」\n強茂_第一代碳化矽二極管 圖/蔡仁譯攝影\n在碳化矽的IC設計業務中，一邊要與上游材料供應商對接，另一頭則是相關應用的功率電源供應器廠商。要做到碳化矽功率元件的產業垂直整合，陳佐銘認為，挑戰來自於上游原料供應。「主要的變異數在最前面，要找到很整齊的Substrate（基板）加上Epitaxy（磊晶）不容易，也是決定後面良率很大的因素。」\n至於功率電源供應器客戶的掌握，強茂非常有信心，「通路、服務，是我們優於其他大廠的地方。」由於目前的客戶都已合作超過30年，將來想進化導入碳化矽元件，強茂依然會是他們首選的合作夥伴。\n臺灣如何打國際戰？強茂：團結的狼纔有機會\n談起臺灣在第3類半導體的發展，陳佐銘認為，儘管臺灣在第1類半導體材料（矽）和先進製程已積累多年基礎，成熟的產業聚落甚至讓臺積電有「護國神山」之稱，「但是第3類半導體完全不一樣，主要玩家都不在這裡（臺灣）。」\n以矽材料為基礎的第1類半導體，由於已發展60多年，產業架構成熟，供應鏈的上、中、下游廠商專業分工，也獨立運作得非常健全。相較之下，碳化矽材料雖然也已經發展30多年，卻是近年來才開始受到產業關注，國際大廠也多以垂直整合製造商（IDM）為主。\n「IDM山頭都是老虎，我們只是一隻狼，靠一隻狼去打老虎是不可能的，但是團結的狼就有機會。」陳佐銘比喻。因此，臺灣要發展第3類半導體，產業還不夠完整，也需要更多垂直整合，才能在國際上站穩腳步。\n關於另一項備受關注、市場也更成熟的第3類半導體材料：氮化鎵（GaN），強茂是否考慮投入？\n陳佐明坦言，氮化鎵的技術門檻不高，投入的同業也多，市場競爭相較於碳化矽更為激烈，因此公司仍處於觀望狀態，不過「我們希望可以補足在第3類半導體的拼圖，所以會再評估。」\n強茂營運長_陳佐銘 圖/蔡仁譯攝影\n強茂\n成立：1986年 董事長：方敏清 近期財報：2021年前3季累計合併營收104.34億元，年增39.26％；累計前3季每股稅後純益（EPS）4.45元。 關鍵技術：臺灣少數具備碳化矽MOSFET（金屬氧化物半導體場效電晶體）與二極體設計能力的廠商。 目標：預期2025～2026年，碳化矽產品營收佔比由目前的1％提升至5～8％；2022年，車用IC營收佔比，從目前的13％提升至超過15％。\n責任編輯：吳佩臻\n更多報導目標打造「SiC走廊」！無懼對手虎視電動車大餅，Wolfspeed如何穩居碳化矽基板之王？總主筆專欄》成就馬斯克霸業的第三代半導體，也能帶臺灣業者高飛？"
# 要注意斷的符號不可以讓詞切成兩半，e.g. "I'm" -> "I" "m" 這樣會造成B-PERSON, I-PERSON, O, O被切成[B-PERSON], [I-PERSON, O]，第二個子句沒有B-PERSON，會出錯 
def split_string_by_delimiter(str, pattern= "。\n\t", keep_delimiter = True, separate = False):
    if keep_delimiter:
        res = re.split('([' + pattern + '])', str)
        # delimiter保留在文字中或是分開
        if separate:
            return res
        else:
            return [i+j for i,j in zip(res[::2], res[1::2])]
    else:
        # 保留delimiter或刪除
        res = re.split('[' + pattern + ']', str)
        return res

def indexLebel_to_BIO(text, label):
    """[
      {
        "end": 149,
        "text": "兩",
        "start": 148,
        "labels": [
          "CARDINAL"
        ]
      }
    ]
    """
    instance_label=['O'] * len(text)
    for label in label:
        start_index = label['start']
        end_index = label['end']

        # 可輸入多個label或是單一label，但僅處理第一個label
        if "labels" in label and isinstance(label['labels'], list):
            label = label['labels'][0]
        elif "label" in label and isinstance(label['label'], str):
            label = label['label']
        
        for i in range(start_index, end_index):
            if i == start_index:
                instance_label[i] = "B-" + str(label)
            else:
                instance_label[i] = "I-" + str(label)
        # print(label)
    assert len(instance_label) == len(text)
    return instance_label


# label: BIO format
def split_doc_to_sentance(text, label, mode='BIO'):
    # split text
    text_splited = split_string_by_delimiter(text)
    
    if mode=='BIO':
        # split label
        label_splited = []
        start = 0
        for sub_sentence in text_splited:
            end = start + len(sub_sentence)
            label_splited.append(label[start:end])
            start = end

    return text_splited, label_splited

def convert_label_list_to_BIO(data):
    instance_label=['O'] * len(data['text'])
    for label in data['label']:
        start_index = label['start']
        end_index = label['end']
        label = label['labels'][0]
        for i in range(start_index, end_index):
            if i == start_index:
                instance_label[i] = "B-" + str(label)
            else:
                instance_label[i] = "I-" + str(label)
        # print(label)
    return instance_label

def convert_to_BIO(data):
    data_converted = []
    for single_doc in data:
        single_doc_convert_result = {
            'text': single_doc['text'],
            'label': convert_label_list_to_BIO(single_doc)
        }
        assert len(single_doc_convert_result['text']) == len(single_doc_convert_result['label'])
        data_converted.append(single_doc_convert_result)
    return data_converted

def split_to_sentence(data):
    result = []
    for single_doc in data:
        text_splited = split_string_by_delimiter(single_doc['text'])
        label_splited = []
        index = 0
        for sentence in text_splited:
            label_splited = single_doc['label'][index:index+len(sentence)]
            index = index + len(sentence)
        
            concat = {
                'text': list(sentence),
                'label': label_splited
            }
            result.append(concat)
    return result

"""
標準交換格式
[
    {
        'text': '我是一個人',
        'labels': [
            {
                'start': 0,
                'end': 1,
                'label': 'PERSON'
            }
        ]
    }
]


"""

## 轉換為標準交換格式的範例函數
def load_xx(data, keep_all_information=False):
    def text_to_unified(text):
        # 實作此程式
        return text
    def label_to_unified(labels, text=None):
        # 實作此程式
        return labels
    # 轉換
    db = []
    for single_doc in data:
        if keep_all_information==False:
            db.append({
                'text': text_to_unified(single_doc['text']),
                'labels': label_to_unified(single_doc['labels'])
            })
    return db


def load_db(data, keep_all_information=False):
    def text_to_unified(text):
        return text
    def label_to_unified(labels, text=None):
        unified_label = []
        for label in labels:
            unified_label.append({
                'start': label[0],
                'end': label[1],
                'label': label[2]
            })
        return unified_label
    # 載入資料庫
    db = []
    for single_doc in data:
        if keep_all_information==False:
            db.append({
                'text': text_to_unified(single_doc['article_content']),
                'labels': label_to_unified(single_doc['result']['2'])
            })
    return db

def export_bio(data):
    def unified_to_bio_text(text):
        # 實作此程式
        return text
    def unified_to_bio_label(labels, text=None):
        # 實作此程式
        instance_label=['O'] * len(text) #先全部填寫O
        for label in labels:
            start_index = label['start']
            end_index = label['end']
            label = label['label']
            for i in range(start_index, end_index):
                if i == start_index:
                    instance_label[i] = "B-" + str(label)
                else:
                    instance_label[i] = "I-" + str(label)
        return instance_label
    result = []
    for single_doc in data:
        result_single_doc = {}
        result_single_doc['text'] = unified_to_bio_text(single_doc['text'])
        result_single_doc['labels'] = unified_to_bio_label(single_doc['labels'], single_doc['text'])
        assert len(result_single_doc['text']) == len(result_single_doc['labels'])
        result.append(result_single_doc)
   
    return result


# 可輸入單筆資料或多筆資料
# 單筆資料格式不限
# 多筆資料為單筆資料的list
def convert(data, input = "DATABASE", output='BIO'):
    if not isinstance(data, list):
        data = [data]
    # 輸入層
    if input == "DATABASE":
        formated_data = load_db(data)
    
    # 輸出層
    if output == "UNIFIED":
        output_data = formated_data
    elif output == "BIO":
        output_data = export_bio(formated_data)
    return output_data

# 
"""

    {
        'text': '我是一個人',
        'labels': [
            {
                'start': 0,
                'end': 1,
                'label': 'PERSON'
            }
        ]
    }

"""

def split_doc_to_sentance_bio(data):
    
    # keep separator and do not put separator as new element.
    # def split_string_by_delimiter(str, pattern= ";,.\-\%。，\n\t", keep_delimiter = True, separate = False):
    # s= "自從電動-車大廠特斯拉（Tesla）旗下的Model 3車款，於2018年導入以碳化矽（SiC）生產的功率元件——金屬氧化物半導體場效電晶體（MOSFET），使得功率轉換效率大增，也間接延長了電池續航力，不但帶動碳化矽這項材料重新受到業界關注，各種應用也持續發酵。\n「碳化矽的特性適合運用在功率2,000W（瓦）以上的高階電源應用，這一定是未來趨勢，只是看它（碳化矽市場）爆發得有多快。」強茂營運長陳佐銘表示。\n強茂為臺灣最大整流元件製造商，市佔全球第6。目前高達99％的營收是由一般矽材料產品所貢獻，在矽製程的二極體產品面，可以從晶片設計、晶圓製造，到封裝測試、市場行銷一手包辦，共擁有2座晶圓廠（位於中國山東和高雄永安）與3個封裝廠區（位於高雄岡山、江蘇徐州、江蘇無錫）。\n小辭典\n【二極體】Diode，如同控制電流的閥門，半導體的二極體大多使用矽基材生產，例如整流二極體，可將交流電轉變為直流電。  【功率元件】電子裝置的電能轉換與電路控制的核心；主要用途包括變頻、整流、變壓、功率放大等，應用於通訊、消費電子、新能源交通等。  【MOSFET】金屬氧化物半導體場效電晶體，為功率半導體元件，利用閘極電壓控制輸出電流的大小，以供應終端電子設備，常用於手機、筆電、行動電源等。\n強茂營運長_陳佐銘 圖/蔡仁譯攝影\n攜手上游材料商，以高CP服務助客戶升級\n根據法國市場研究機構Yole Développement預測，受到汽車電動化趨勢的帶動，碳化矽功率半導體市場2020年～2026年將以36％年複合成長率（CAGR）成長，屆時產值可望達45億美元。\n看好功率元件採用碳化矽的前景，成立超過30年的強茂，已於2019年起向國際大廠招攬人才，研發團隊裡也有約20％的人力，專注於開發碳化矽產品。2020年，強茂已量產第1代碳化矽二極管，主要針對工業電源、消費性電源、太陽能逆變器及能源轉換系統等非車規的應用領域；2021年預計營收可達1.25億元，並計畫於2022年量產第2代產品。\n「Gen 2（第2代）效率可提升15％，成本節省20％。」陳佐銘指出，當強茂的產品效能足以媲美國際大廠，也看好未來材料成本逐漸下降，「這樣成本就不會是我們吃虧的地方，高CP值加服務，就是我們的路線。」\n陳佐銘分析，目前碳化矽產品價格依然是矽基產品的7～8倍，但是「2025年之後，EV（純電動車）比例會非常高，到時候我們的產品成熟了，應用端也夠多元，預期（碳化矽元件）價格會往下走，⋯⋯如果能走到一半的價錢，甜蜜點就出現了。」\n到時候，強茂碳化矽產品的營收佔比，估計可以從目前的1％提升至5～8％。\n談到碳化矽未來的產品線規畫，陳佐銘說，「要打國際戰，車用就是主戰場！」強茂也訂於2023年1月之前，推出旗下第1代碳化矽金屬氧化物半導體場效電晶體（SiC MOSFET），鎖定電動車市場需求，「我們已經做好打這個仗的準備！」\n強茂_第一代碳化矽二極管 圖/蔡仁譯攝影\n在碳化矽的IC設計業務中，一邊要與上游材料供應商對接，另一頭則是相關應用的功率電源供應器廠商。要做到碳化矽功率元件的產業垂直整合，陳佐銘認為，挑戰來自於上游原料供應。「主要的變異數在最前面，要找到很整齊的Substrate（基板）加上Epitaxy（磊晶）不容易，也是決定後面良率很大的因素。」\n至於功率電源供應器客戶的掌握，強茂非常有信心，「通路、服務，是我們優於其他大廠的地方。」由於目前的客戶都已合作超過30年，將來想進化導入碳化矽元件，強茂依然會是他們首選的合作夥伴。\n臺灣如何打國際戰？強茂：團結的狼纔有機會\n談起臺灣在第3類半導體的發展，陳佐銘認為，儘管臺灣在第1類半導體材料（矽）和先進製程已積累多年基礎，成熟的產業聚落甚至讓臺積電有「護國神山」之稱，「但是第3類半導體完全不一樣，主要玩家都不在這裡（臺灣）。」\n以矽材料為基礎的第1類半導體，由於已發展60多年，產業架構成熟，供應鏈的上、中、下游廠商專業分工，也獨立運作得非常健全。相較之下，碳化矽材料雖然也已經發展30多年，卻是近年來才開始受到產業關注，國際大廠也多以垂直整合製造商（IDM）為主。\n「IDM山頭都是老虎，我們只是一隻狼，靠一隻狼去打老虎是不可能的，但是團結的狼就有機會。」陳佐銘比喻。因此，臺灣要發展第3類半導體，產業還不夠完整，也需要更多垂直整合，才能在國際上站穩腳步。\n關於另一項備受關注、市場也更成熟的第3類半導體材料：氮化鎵（GaN），強茂是否考慮投入？\n陳佐明坦言，氮化鎵的技術門檻不高，投入的同業也多，市場競爭相較於碳化矽更為激烈，因此公司仍處於觀望狀態，不過「我們希望可以補足在第3類半導體的拼圖，所以會再評估。」\n強茂營運長_陳佐銘 圖/蔡仁譯攝影\n強茂\n成立：1986年 董事長：方敏清 近期財報：2021年前3季累計合併營收104.34億元，年增39.26％；累計前3季每股稅後純益（EPS）4.45元。 關鍵技術：臺灣少數具備碳化矽MOSFET（金屬氧化物半導體場效電晶體）與二極體設計能力的廠商。 目標：預期2025～2026年，碳化矽產品營收佔比由目前的1％提升至5～8％；2022年，車用IC營收佔比，從目前的13％提升至超過15％。\n責任編輯：吳佩臻\n更多報導目標打造「SiC走廊」！無懼對手虎視電動車大餅，Wolfspeed如何穩居碳化矽基板之王？總主筆專欄》成就馬斯克霸業的第三代半導體，也能帶臺灣業者高飛？"
    # 要注意斷的符號不可以讓詞切成兩半，e.g. "I'm" -> "I" "m" 這樣會造成B-PERSON, I-PERSON, O, O被切成[B-PERSON], [I-PERSON, O]，第二個子句沒有B-PERSON，會出錯 
    # def split_string_by_delimiter(str, pattern= "。\n\t", keep_delimiter = True, separate = False):
    def split_string_by_delimiter(str, pattern= "。", keep_delimiter = True, separate = False):
        if keep_delimiter:
            res = re.split('([' + pattern + '])', str)
            # delimiter保留在文字中或是分開
            if separate:
                return res
            else:
                return [i+j for i,j in zip(res[::2], res[1::2])]
        else:
            # 保留delimiter或刪除
            res = re.split('[' + pattern + ']', str)
            return res

    def split_label_by_delimiter(labels, sentence_list=None):
        # split label
        label_splited = []
        start = 0
        for sub_sentence in sentence_list:
            end = start + len(sub_sentence)
            label_splited.append(labels[start : end])
            start = end
        return label_splited

    if not isinstance(data, list):
        data = [data]

    result = []
    for single_doc in data:
        text= split_string_by_delimiter(single_doc['text'])
        labels= split_label_by_delimiter(single_doc['labels'], text)
        splited_doc = {
            'text': text,
            'labels': labels
        }
        # print(splited_doc)
        for i in range(len(splited_doc['text'])):
            # print(len(splited_doc['text'][i]))
            # print(len(splited_doc['labels'][i]))
            assert len(splited_doc['text'][i]) == len(splited_doc['labels'][i])
        result.append(splited_doc)


    return result

def validate_bio(data):
    if not isinstance(data, list):
        data = [data]

    result = []
    for single_doc in data:
        # print(single_doc)
        removed_index = []
        for i in range(len(single_doc['text'])):
            if single_doc['labels'][i][0].startswith('I-'):
                removed_index.append(i)
                # raise ValueError('I- must be preceded by B-')

        for i in removed_index[::-1]:
            del single_doc['text'][i]
            del single_doc['labels'][i]
        result.append(single_doc)
    return result
    ## 以下是自動生成的，以後可以參考
    # for single_doc in data:
    #     for i in range(len(single_doc['labels'])):
    #         for j in range(len(single_doc['labels'][i])):
    #             if single_doc['labels'][i][j] == 'O':
    #                 continue
    #             elif single_doc['labels'][i][j].startswith('B-'):
    #                 if j+1 < len(single_doc['labels'][i]) and single_doc['labels'][i][j+1].startswith('I-'):
    #                     continue
    #                 else:
    #                     print(single_doc['text'][i])
    #                     print(single_doc['labels'][i])
    #                     raise ValueError('B- must be followed by I-')
    #             elif single_doc['labels'][i][j].startswith('I-'):
    #                 if j-1 >= 0 and single_doc['labels'][i][j-1].startswith('I-'):
    #                     continue
    #                 else:
    #                     print(single_doc['text'][i])
    #                     print(single_doc['labels'][i])
    #                     raise ValueError('I- must be preceded by I- or B-')
    #             else:
    #                 raise ValueError('Invalid label: ' + single_doc['labels'][i][j])

    return data

def convert_bio_to_conll(data):
    """
    test = [{
        "text":["自從電動車大廠特斯拉", "測試"],
        "labels":[["O", "O", "B-P", "I-P", "I-P", "O", "O", "B-O", "I-O", "I-O"], ["O", "O"]]
    },
    {
        "text":["自從電動車大廠特斯拉", "測試"],
        "labels":[["O", "O", "B-P", "I-P", "I-P", "O", "O", "B-O", "I-O", "I-O"], ["O", "O"]]
    }]  

    out = [[[('自', 'O'),
    ('從', 'O'),
    ('電', 'B-P'),
    ('動', 'I-P'),
    ('車', 'I-P'),
    ('大', 'O'),
    ('廠', 'O'),
    ('特', 'B-O'),
    ('斯', 'I-O'),
    ('拉', 'I-O')],
    [('測', 'O'), ('試', 'O')]],
    [[('自', 'O'),
    ('從', 'O'),
    ('電', 'B-P'),
    ('動', 'I-P'),
    ('車', 'I-P'),
    ('大', 'O'),
    ('廠', 'O'),
    ('特', 'B-O'),
    ('斯', 'I-O'),
    ('拉', 'I-O')],
    [('測', 'O'), ('試', 'O')]]]
    """
    if not isinstance(data, list):
        data = [data]
    result = []
    for single_doc in data:
        doc = []
        for sentence_idx in range(len(single_doc['text'])):
            removed_index = []
            token_list = list(single_doc['text'][sentence_idx])
            label_list = single_doc['labels'][sentence_idx]
            
            # 移除token為空白(暫時不要移除好了，這樣以後才可以對應到DB資料並寫回DB)
            # for i in range(len(token_list)):
            #     if token_list[i] == ' ':
            #         removed_index.append(i)
            # for i in removed_index[::-1]:
            #     del token_list[i]
            #     del label_list[i]
            # 移除完成

            zip_data = list(zip(token_list, label_list))
            doc.append(zip_data)
        result.append(doc)
    return result
import os
def store_conll_to_file(data, path, new_line_for_doc=True):
    if not isinstance(data, list):
        data = [data]
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        for single_doc in data:
            for idx, sentence in enumerate(single_doc):
                for token in sentence:
                    # 為了印出像是\n這樣的字元，所進行的各種嘗試
                    # encoded_str = str(token[0] + " " + token[1]).encode('unicode-escape')
                    encoded_str = str(token[0] + " " + token[1])
                    # f.write(fr"{encoded_str}")
                    # if '\n' in encoded_str:
                    #     print("%r" % encoded_str)

                    # 最後只有這種成功(若沒有replace，出來的string會包含左右引號'')
                    f.write(("%r" % encoded_str).replace('\'', ''))
                    # f.write("換行")
                    f.write("\n")
                    # f.write(encoded_str + r'\r\n\ '[:-1])
                    # f.write("\n")
                if new_line_for_doc and idx != len(single_doc)-1:
                    f.write("\n")

# import opencc
# converter = opencc.OpenCC('t2s.json')
# def convert_to_traditional_chinese_bio(data):
#     if not isinstance(data, list):
#         data = [data]
#     for single_doc in data:
#         single_doc['text'] = converter.convert(single_doc['text'])

            
#     return data

def filter_out_label_bio(data, removed_labels):
    if not isinstance(data, list):
        data = [data]
    result = []
    for single_doc in data:
        for label_idx in range(len(single_doc['labels'])):
            if single_doc['labels'][label_idx].startswith("B-") or single_doc['labels'][label_idx].startswith("I-"):
                if single_doc['labels'][label_idx][2:] in removed_labels:
                    single_doc['labels'][label_idx] = 'O'
        result.append(single_doc)
    return result

def change_label_name_bio(data, old_label, new_label):
    if not isinstance(data, list):
        data = [data]
    for single_doc in data:
        for label_idx in range(len(single_doc['labels'])):
            if single_doc['labels'][label_idx].startswith("B-") or single_doc['labels'][label_idx].startswith("I-"):
                if single_doc['labels'][label_idx][2:] == old_label:
                    single_doc['labels'][label_idx] = single_doc['labels'][label_idx][0] + "-" + new_label
    return data