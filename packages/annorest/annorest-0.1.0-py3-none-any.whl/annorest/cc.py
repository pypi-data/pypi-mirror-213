import opencc
converter = opencc.OpenCC('t2s.json')
def convert_to_traditional_chinese_bio(data):
    if not isinstance(data, list):
        data = [data]
    for single_doc in data:
        single_doc['text'] = converter.convert(single_doc['text'])

            
    return data