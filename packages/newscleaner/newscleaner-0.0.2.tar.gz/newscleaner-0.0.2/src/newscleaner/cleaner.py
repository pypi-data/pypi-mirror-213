import re
import json
import html
import unicodedata
import pkg_resources


def clean(text):
    
    with open("tags.json", encoding="utf8") as file:
        tags = json.load(file)
    
    with open("regex.json", encoding="utf8") as file:
        regex = json.load(file)
    
    def replace_all(text, dic):
        for i, j in dic.items():
            text = text.replace(i, j)
        return text

    def replace_all1(text, dic):
        for i, j in dic.items():
            text = text.replace(j, i)
        return text

    text = replace_all(text,tags)
    text = re.sub(r'<[^<>]*>', ' ',text) 
    
    #rulesList = rulesFile
    for rule in regex:
        rules = regex.get(rule)
        if rule == 'suffix': 
            for substring in rules:
                pattern = re.compile(re.escape(substring)+'.*')
                text = pattern.sub('', text)
        elif rule == 'perfect_match':
            for substring in rules:
                pattern = re.compile(re.escape(substring))
                text = pattern.sub('',text)
        elif rule == 'prefix':
            for substring in rules:
                pattern = re.compile('.*'+re.escape(substring))
                text = pattern.sub('', text)
                
     
    text = html.unescape(text) #decoding unicode entities using html parser
    text = replace_all1(text,tags) 
                
     # cleaning emoji
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                           "]+", flags=re.UNICODE)
    
    clean_text = emoji_pattern.sub(r'', text)
    clean_text = re.sub("\n",'',clean_text)
    clean_text = unicodedata.normalize("NFKD",clean_text) #decoding utf-8 unicode data which is producing spacing
    
    # storing words in list with no extra spaces
    clean_text= [j for j in clean_text.strip().split(" ") if j !=""]
    
    
    return " ".join(clean_text)