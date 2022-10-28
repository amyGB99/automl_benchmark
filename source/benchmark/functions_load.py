
######################## Text #################################


def load_paws(self,format = "pandas", in_x_y = True ,samples =  2, encoding = "utf-8"):
    import pandas as pd 
    import os 
    path = self.download()

    train = os.path.join(path,'train.txt')
    test =  os.path.join(path,'test.txt')
    all = os.path.join(path,'all.txt')
    
    dftr = pd.read_csv(train,sep="\t",encoding=encoding)
    dfte = pd.read_csv(test,sep="\t",encoding=encoding)
    dfall = pd.concat([dftr,dfte],axis=0).reset_index(drop = True)
    
    
    #dfall = pd.read_csv(all,sep="\t",encoding=encoding)
    if in_x_y == False:
        if samples == 1:
            return dfall.drop(['id'],axis=1)
        elif samples ==2:
            return dftr.drop(['id'],axis=1),dfte.drop(['id'],axis=1)
        else:
            print("Incorrect params") 
    else:
        dummy_tr = dftr.filter(regex='(sentence1|sentence2)') 
        y_tr = dftr.filter(regex='label')

        dummy_te = dfte.filter(regex='(sentence1|sentence2)') 
        y_te = dfte.filter(regex='label') 
        
        if samples== 1:
            dummy_all = dfall.filter(regex='(sentence1|sentence2)') 
            y = dfall.filter(regex='label')
            if format == "pandas":
                return dummy_all,y
            else:
                X = dummy_all.to_numpy().tolist()
                return X,list(y['label']) 
        elif samples ==2:
            if format == "pandas":
                return dummy_tr,y_tr,dummy_te,y_te 
            else:
                #X_tr = list()
                #for i in range(len(dummy_tr.axes[0])):
                    #X_tr.append((dummy_tr.iloc[i,0],dummy_tr.iloc[i,1])) 
                X_tr = dummy_tr.to_numpy().tolist()
                #X_te = list()
                #for i in range(len(dummy_te.axes[0])):
                 #   X_te.append((dummy_te.iloc[i,0],dummy_te.iloc[i,1])) 
                X_te = dummy_te.to_numpy().tolist()
                return X_tr, list(y_tr['label']),X_te, list(y_te['label'])  
        else:
            print("Incorrect params")    
    
def load_wnli(self,format = "pandas",in_x_y = True ,samples =  2,encoding='utf-8'):
    import pandas as pd 
    import os 
    path = self.download()
    
    #path = os.path.dirname(os.path.realpath(__file__))
    ptrain = os.path.join(path,'wnli-train-es.tsv')
    ptest =  os.path.join(path,'wnli-dev-es.tsv') 
    
    dftr = pd.read_csv(ptrain,sep='\t',encoding= encoding)  
    dfte = pd.read_csv(ptest,sep='\t',encoding= encoding)  
    
    dfte = dfte[dfte["label"].notna()]
    dfte["label"] = dfte["label"].astype("int")
    dfall = pd.concat([dftr,dfte],axis=0).reset_index(drop = True)
    
    if in_x_y == False:
        if samples == 1:
            return dfall.drop(['index'],axis=1)
        elif samples ==2:
            return dftr.drop(['index'],axis=1),dfte.drop(['index'],axis=1)
        else:
            print("Incorrect params") 
    else:
        dummy_tr = dftr.filter(regex='(sentence1|sentence2)') 
        y_tr = dftr.filter(regex='label')

        dummy_te = dfte.filter(regex='(sentence1|sentence2)') 
        y_te = dfte.filter(regex='label') 
        
        if samples== 1:
            dummy_all = dfall.filter(regex='(sentence1|sentence2)') 
            y = dfall.filter(regex='label')
            if format == "pandas":
                return dummy_all,y
            else:
                X = dummy_all.to_numpy().tolist()
                return X,list(y['label']) 
        elif samples ==2:
            if format == "pandas":
                return dummy_tr,y_tr,dummy_te,y_te 
            else:
                #X_tr = list()
                #for i in range(len(dummy_tr.axes[0])):
                    #X_tr.append((dummy_tr.iloc[i,0],dummy_tr.iloc[i,1])) 
                X_tr = dummy_tr.to_numpy().tolist()
                #X_te = list()
                #for i in range(len(dummy_te.axes[0])):
                 #   X_te.append((dummy_te.iloc[i,0],dummy_te.iloc[i,1])) 
                X_te = dummy_te.to_numpy().tolist()
                return X_tr, list(y_tr['label']),X_te, list(y_te['label'])  
        else:
            print("Incorrect params")
    
def load_wikiann(self, format = "pandas", samples =3):#falta
    '''
    Return :
     dict:   {
        'tokens': ["rick", "and", "morty", "are", "cool", "."],
        'ner_tags': ["B-PER", "O" , "B-PER", "O", "O", "O"],
        'langs': ["en", "en", "en", "en", "en", "en"]
        'spans': ["PER: rick", "PER: morty"]
        }
    '''
    import pandas as pd 
    import os 
    import json
    
    path = self.download()
    train = os.path.join(path,'train.json')
    dev =  os.path.join(path,'dev.json')
    test =  os.path.join(path,'test.json')
    
    def generate_examples(filepath):
        
        with open(filepath, encoding="utf-8") as f:
            wikiann_es = json.load(f)
            for id_, data in enumerate(wikiann_es["data"]):
                tokens = data["tokens"]
                ner_tags = data["ner_tags"]
                spans = data["spans"]
                langs = data["langs"]
                yield {"langs":langs,"tokens": tokens,"ner_tags":ner_tags,"spans":spans}
    
    Xtr = []
    ytr = []
    
    Xte = []
    yte = []
    yde = []
    Xde = []
    
    for item in generate_examples(train):
        Xtr.append(item['tokens'])
        ytr.append(item['ner_tags'])
    for item in generate_examples(dev):
        Xde.append(item['tokens'])
        yde.append(item['ner_tags'])
    for item in generate_examples(test):
        Xte.append(item['tokens'])
        yte.append(item['ner_tags'])       
    return Xtr,ytr, Xde, yde, Xte,yte  

def load_sst_en(self,  format = "pandas", in_x_y= True, samples= 2, encoding= 'utf-8'):
    import pandas as pd
    import os 
    path = self.download()
    ptrain = os.path.join(path,'sst_train.txt')
    ptest = os.path.join(path,'sst_test.txt')
    
    dftr = pd.read_csv(ptrain,sep="\t",header=None,names=['label','text'],encoding=encoding)
    dftr['label'] = dftr['label'].str.replace("__label__","").astype('int')
    
    dfte = pd.read_csv(ptest,sep="\t",header=None,names=['label','text'],encoding=encoding)
    dfte['label'] = dfte['label'].str.replace("__label__","").astype('int')
    
    all_ = pd.concat([dftr,dfte],axis=0).reset_index(drop = True)
    if in_x_y == False:
        if samples == 1:
            return all_
        elif samples ==2:
            return dftr,dfte
        else:
            print("Incorrect params") 
    else:
        dummy_tr = dftr.filter(regex='text') 
        y_tr = dftr.filter(regex='label')

        dummy_te = dfte.filter(regex='text') 
        y_te = dfte.filter(regex='label') 
        
        if samples == 1:
            dummy_all = all_.filter(regex='text') 
            y = all_.filter(regex='label')
            if format == "pandas":
                return dummy_all,y
            else:
                X = list(dummy_all["text"])
                return X,list(y['label']) 
        elif samples ==2:
            if format == "pandas":
                return dummy_tr,y_tr,dummy_te,y_te 
            else:
                X_tr = list(dftr['text'])
                X_te = list(dfte['text'])
                return X_tr, list(y_tr['label']),X_te, list(y_te['label'])  
        else:
             print("Incorrect params") 

def load_wikicat(self, format = "pandas",in_x_y = True, samples = 2,encoding = 'utf-8'):
    import pandas as pd 
    import os 
    import numpy as np
    path = self.download()
    ptrain = os.path.join(path,'train.tsv')
    ptest =  os.path.join(path,'test.tsv')
    # ptrain = os.path.join(path,'train.txt')
    # pdev = os.path.join(path,'dev.txt')
    # ptest = os.path.join(path,'test.txt')
    
    dftr = pd.read_csv(ptrain,sep="\t", encoding = encoding)
    dfte = pd.read_csv(ptest,sep="\t",encoding = encoding)
    
    dftr['label'] = dftr['label'].astype('category')
    dfte['label'] = dfte['label'].astype('category')
    dfall = pd.concat([dftr,dfte],axis=0).reset_index(drop = True)
    
    if in_x_y == False:
        if samples == 1:
            return dfall
        elif samples ==2:
            return dftr,dfte
        else:
            print("Incorrect params") 
    else:
        X_tr = dftr.filter(regex='text') 
        y_tr = dftr.filter(regex='label')

        X_te = dfte.filter(regex='text') 
        y_te = dfte.filter(regex='label') 
        
        if samples== 1:
            X_all = dfall.filter(regex='text') 
            y = dfall.filter(regex='label')
            if format == "pandas":
                return X_all,y
            else:
                return list(X_all['text']),list(y['label']) 
        elif samples ==2:
            if format == "pandas":
                return X_tr,y_tr,X_te,y_te 
            else:
               
                return list(X_tr['text']), list(y_tr['label']),list(X_te['text']), list(y_te['label'])  
        else:
            print("Incorrect params")

def load_stsb(self,  format = "pandas", in_x_y= True, samples= 2, encoding= 'utf-8'):
    import pandas as pd
    import os 
    path = self.download()
    
    train = os.path.join(path,'train.csv')
    dev =  os.path.join(path,'dev.csv')
    test =  os.path.join(path,'test.csv')
    
    dftr1 = pd.read_csv(train, names=['sentence1','sentence2','score'],encoding= encoding)
    dftr2 = pd.read_csv(dev, names=['sentence1','sentence2','score'],encoding= encoding)
    dfte = pd.read_csv(test ,names=['sentence1','sentence2','score'],encoding= encoding)
    dftr = pd.concat([dftr1,dftr2],axis=0).reset_index(drop = True)
    dfall = pd.concat([dftr,dfte],axis=0).reset_index(drop = True)
    
    # dfte = dfte[dfte["label"].notna()]
    # dfte["label"] = dfte["label"].astype("int")
    if in_x_y == False:
        if samples == 1:
            return dfall
        elif samples ==2:
            return dftr,dfte
        else:
            print("Incorrect params") 
    else:
        dummy_tr = dftr.filter(regex='(sentence1|sentence2)') 
        y_tr = dftr.filter(regex='score')

        dummy_te = dfte.filter(regex='(sentence1|sentence2)') 
        y_te = dfte.filter(regex='score') 
        
        if samples== 1:
            dummy_all = dfall.filter(regex='(sentence1|sentence2)') 
            y = dfall.filter(regex='score')
            if format == "pandas":
                return dummy_all,y
            else:
                X = dummy_all.to_numpy().tolist()
                return X, list(y['score']) 
        elif samples ==2:
            if format == "pandas":
                return dummy_tr,y_tr,dummy_te,y_te 
            else:
                #X_tr = list()
                #for i in range(len(dummy_tr.axes[0])):
                    #X_tr.append((dummy_tr.iloc[i,0],dummy_tr.iloc[i,1])) 
                X_tr = dummy_tr.to_numpy().tolist()
                #X_te = list()
                #for i in range(len(dummy_te.axes[0])):
                 #   X_te.append((dummy_te.iloc[i,0],dummy_te.iloc[i,1])) 
                X_te = dummy_te.to_numpy().tolist()
                return X_tr, list(y_tr['score']),X_te, list(y_te['score'])  
        else:
            print("Incorrect params")
    
def load_haha(self,  format = "pandas", in_x_y= True, samples= 2, encoding= 'utf-8',target= 'is_humor' ):
    
    import pandas as pd 
    import os 
    import numpy as np
    path = self.download()
    ptrain = os.path.join(path,'haha_2019_train.csv')
    ptest =  os.path.join(path,'haha_2019_test_gold.csv')

    dftr = pd.read_csv(ptrain, encoding = encoding)
    dfte = pd.read_csv(ptest,encoding = encoding)
    dfall = pd.concat([dftr,dfte],axis=0).reset_index(drop = True)
    
    if in_x_y == False:
        if samples == 1:
            return dfall
        elif samples ==2:
            return dftr,dfte
        else:
            print("Incorrect params") 
    else:
        X_tr = dftr.filter(regex='text') 
        y_tr = dftr.filter(regex=target)

        X_te = dfte.filter(regex='text') 
        y_te = dfte.filter(regex=target) 
        
        if samples== 1:
            X_all = dfall.filter(regex='text') 
            y = dfall.filter(regex= target)
            if format == "pandas":
                return X_all,y
            else:
                return list(X_all['text']),list(y[target]) 
        elif samples ==2:
            if format == "pandas":
                return X_tr,y_tr,X_te,y_te 
            else:
               
                return list(X_tr['text']), list(y_tr[target]),list(X_te['text']), list(y_te[target])  
        else:
            print("Incorrect params")

def load_meddocan(self,  format = "pandas", in_x_y= True, samples= 2, encoding= 'utf-8'):
    
    
    def parse_text_and_tags(file_name=None):
        """
        Given a file representing an annotated text in Brat format
        returns the `text` and `tags` annotated.
        """
        text = ""
        phi = []

        if file_name is not None:
            text = open(os.path.splitext(file_name)[0] + ".txt", "r").read()

            for row in open(file_name, "r"):
                line = row.strip()
                if line.startswith("T"):  # Lines is a Brat TAG
                    try:
                        label = line.split("\t")[1].split()
                        tag = label[0]
                        start = int(label[1])
                        end = int(label[2])
                        value = text[start:end]
                        phi.append((tag, start, end, value))
                    except IndexError:
                        print(
                            "ERROR! Index error while splitting sentence '"
                            + line
                            + "' in document '"
                            + file_name
                            + "'!"
                        )
                else:  # Line is a Brat comment
                    print("\tSkipping line (comment):\t" + line)
        return (text, phi)

    def get_tagged_tokens(text, tags):
        """
        convert a given text and annotations in brat format to IOB tag format

        Parameters:
        - text: raw text
        - tags: tags annotated on `text` with brat format

        output:
        tuple of identified tags in brat format from text and list of tokens tagged in IOB format
        """
        tags.sort(key=lambda x: x[1])
        offset = 0
        tagged_tokens = []

        current_tag = ""
        current_tag_end = 0
        current_tag_init = 0
        processing_token = False

        token = ""
        tag = ""

        itag = 0
        next_tag_init = tags[itag][1]

        sentences = [[]]

        for char in text:
            if processing_token and current_tag_end == offset:
                tagged_tokens.append((current_tag, current_tag_init, offset, token))

                tokens = token.split()
                if len(tokens) > 1:
                    sentences[-1].append((tokens[0], tag))
                    for tok in tokens[1:]:
                        sentences[-1].append((tok, "I-" + current_tag))
                else:
                    sentences[-1].append((token, tag))

                token = ""
                current_tag = ""
                processing_token = False

            if not processing_token and char in [
                "\n",
                " ",
                ",",
                ".",
                ";",
                ":",
                "!",
                "?",
                "(",
                ")",
            ]:
                if token:
                    sentences[-1].append((token, tag))

                if char in ["\n", ".", "!", " ?"] and len(sentences[-1]) > 1:
                    sentences.append([])

                token = ""
                offset += 1
                continue

            if offset == next_tag_init:
                if token:
                    if char in ["\n", " ", ",", ".", ";", ":", "!", "?", "(", ")"]:
                        sentences[-1].append((token, tag))
                    else:
                        token += char
                        sentences[-1].append((token, tag))
                    token = ""

                current_tag = tags[itag][0]
                current_tag_init = tags[itag][1]
                current_tag_end = tags[itag][2]
                processing_token = True

                itag += 1
                next_tag_init = tags[itag][1] if itag < len(tags) else -1

            if processing_token and current_tag:
                if not token:
                    tag = "B-" + current_tag
            else:
                tag = "O"
            token += char
            offset += 1

        raw_sentences = [
            [word for word, _ in sentence] for sentence in sentences if sentence
        ]
        raw_tags = [[tag for _, tag in sentence] for sentence in sentences if sentence]
        return tagged_tokens, raw_sentences, raw_tags

    def compare_tags(tag_list, other_tag_list):
        """
        compare two tags lists with the same tag format:

        (`tag_name`, `start_offset`, `end_offset`, `value`)
        """
        tags_amount = len(tag_list)

        if tags_amount != len(other_tag_list):
            print(
                "missmatch of amount of tags %d vs %d" % (tags_amount, len(other_tag_list))
            )
            return False

        tag_list.sort(key=lambda x: x[1])
        other_tag_list.sort(key=lambda x: x[1])
        for i in range(tags_amount):
            if len(tag_list[i]) != len(other_tag_list[i]):
                print("missmatch of tags format")
                return False

            for j in range(len(tag_list[i])):
                if tag_list[i][j] != other_tag_list[i][j]:
                    print(
                        "missmatch of tags %s vs %s"
                        % (tag_list[i][j], other_tag_list[i][j])
                    )
                    return False

        return True
    
    import os 
    """
    Loads train and test datasets from [MEDDOCAN iberleaf 2018](https://github.com/PlanTL-SANIDAD/SPACCC_MEDDOCAN).

    ##### Examples

    ```python
    >>> X_train, y_train, X_valid, y_valid = load()
    >>> len(X_train), len(X_valid)
    (25622, 8432)
    >>> len(y_train), len(y_valid)
    (25622, 8432)

    ```
    """
    import pandas as pd 
    import os 
    import numpy as np
    path = self.download()
    ptrain = os.path.join(path,'train')
    pdev =  os.path.join(path,'dev')
    ptest =  os.path.join(path,'test')

    train_path = os.path.join(ptrain,'brat')
    dev_path = os.path.join(pdev,'brat')
    test_path = os.path.join(ptest,'brat')

    X_train = []
    X_test = []
    y_train = []
    y_test = []

    total = 0
    success = 0
    failed = 0

    for file in os.scandir(train_path):
        if file.name.split(".")[1] == "ann":
            text, phi = parse_text_and_tags(file.path)
            brat_corpora, text, ibo_corpora = get_tagged_tokens(text, phi)
            if compare_tags(brat_corpora, phi):
                X_train.extend(text)
                y_train.extend(ibo_corpora)

    for file in os.scandir(dev_path):
        if file.name.split(".")[1] == "ann":
            text, phi = parse_text_and_tags(file.path)
            brat_corpora, text, ibo_corpora = get_tagged_tokens(text, phi)
            if compare_tags(brat_corpora, phi):
                X_train.extend(text)
                y_train.extend(ibo_corpora)

    for file in os.scandir(test_path):
        if file.name.split(".")[1] == "ann":
            text, phi = parse_text_and_tags(file.path)
            brat_corpora, text, ibo_corpora = get_tagged_tokens(text, phi)
            if compare_tags(brat_corpora, phi):
                X_test.extend(text)
                y_test.extend(ibo_corpora)

    # if max_examples is not None:
    #     X_train = X_train[:max_examples]
    #     X_test = X_test[:max_examples]
    #     y_train = y_train[:max_examples]
    #     y_test = y_test[:max_examples]
    print(len(X_train))
    print(len(X_test))
    
    return X_train, y_train, X_test, y_test

def load_vaccine(self,  format = "pandas", in_x_y= True, samples= 2, encoding= 'utf-8',target = "label"):
    import pandas as pd 
    import os 
    import numpy as np
    path = self.download()
    ptrain = os.path.join(path,'train.csv')
    ptest =  os.path.join(path,'test.csv')

    dftr = pd.read_csv(ptrain, encoding = encoding).drop(['tweet_id','user_id'],axis= 1)
    dfte = pd.read_csv(ptest,encoding = encoding).drop(['tweet_id','user_id'],axis =1)
    dfall = pd.concat([dftr,dfte],axis=0).reset_index(drop = True)
    
    if in_x_y == False:
        if samples == 1:
            return dfall
        elif samples ==2:
            return dftr,dfte
        else:
            print("Incorrect params") 
    else:
        X_tr = dftr.filter(regex='text') 
        y_tr = dftr.filter(regex=target)

        X_te = dfte.filter(regex='text') 
        y_te = dfte.filter(regex=target) 
        
        if samples== 1:
            X_all = dfall.filter(regex='text') 
            y = dfall.filter(regex= target)
            if format == "pandas":
                return X_all,y
            else:
                return list(X_all['text']),list(y[target]) 
        elif samples ==2:
            if format == "pandas":
                return X_tr,y_tr,X_te,y_te 
            else:
               
                return list(X_tr['text']), list(y_tr[target]),list(X_te['text']), list(y_te[target])  
        else:
            print("Incorrect params")

def load_sentiment(self,  format = "pandas", in_x_y= True, samples= 2, encoding= 'utf-8',target = "label"):
    import pandas as pd 
    import os 
    path = self.download()
    plabel1 = os.path.join(path,'positive_words_es.txt')
    plabel2 =  os.path.join(path,'negative_words_es.txt') 
    positive = []
    negative = []
    with open(plabel1,'r') as fp1:    
        content = fp1.read()
        positive = content.split('\n')
    with open(plabel2,'r') as fp1:    
        content = fp1.read()
        negative = content.split('\n')    
    positive.pop(-1) 
    negative.pop(-1) 
    dftr = pd.DataFrame(columns=['word','label'])
    dfte = pd.DataFrame(columns=['word','label'])
    
    lptrain = 1455 *[1]
    lptest = 100 *[1]
    
    wptrain = positive[0:1455]
    wptest = positive[1455:]
    wntrain = negative[0:2620]
    wntest = negative[2620:]
    lntrain = 2620 *[0]
    lntest = 100 *[0]
    
    wptrain.extend(wntrain)
    wptest.extend(wntest)
    lptrain.extend(lntrain)
    lptest.extend(lntest)
    dftr['word'] = wptrain
    dftr['label'] = lptrain
    dfte['word'] = wptest
    dfte['label'] = lptest
    dfall = pd.concat([dftr,dfte],axis=0).reset_index(drop = True)
    
    if in_x_y == False:
        if samples == 1:
            return dfall
        elif samples ==2:
            return dftr,dfte
        else:
            print("Incorrect params") 
    else:
        X_tr = dftr.filter(regex='word') 
        y_tr = dftr.filter(regex=target)

        X_te = dfte.filter(regex='word') 
        y_te = dfte.filter(regex=target) 
        
        if samples== 1:
            X_all = dfall.filter(regex='word') 
            y = dfall.filter(regex= target)
            if format == "pandas":
                return X_all,y
            else:
                return list(X_all['word']),list(y[target]) 
        elif samples ==2:
            if format == "pandas":
                return X_tr,y_tr,X_te,y_te 
            else:
               
                return list(X_tr['word']), list(y_tr[target]),list(X_te['word']), list(y_te[target])  
        else:
            print("Incorrect params")

def load_wikineural():
    pass 

def load_language(self,  format = "pandas", in_x_y= True, samples= 2, encoding= 'utf-8',target = "labels"):
   
    import pandas as pd 
    import os 
    import numpy as np
    path = self.download()
    ptrain = os.path.join(path,'train.csv')
    pdev =  os.path.join(path,'valid.csv')
    ptest =  os.path.join(path,'test.csv')

    dftr1 = pd.read_csv(ptrain, encoding = encoding)
    dfde = pd.read_csv(pdev,encoding = encoding)
    dfte = pd.read_csv(ptest,encoding = encoding)
    
    dfall = pd.concat([dftr1,dfde,dfte],axis=0).reset_index(drop= True)
    dftr = pd.concat([dftr1,dfde],axis=0).reset_index(drop= True)
    if in_x_y == False:
        if samples == 1:
            return dfall
        elif samples ==2:
            return dftr,dfte
        else:
            print("Incorrect params") 
    else:
        X_tr = dftr.filter(regex='text') 
        y_tr = dftr.filter(regex=target)

        X_te = dfte.filter(regex='text') 
        y_te = dfte.filter(regex=target) 
        
        if samples== 1:
            X_all = dfall.filter(regex='text') 
            y = dfall.filter(regex= target)
            if format == "pandas":
                return X_all,y
            else:
                return list(X_all['text']),list(y[target]) 
        elif samples ==2:
            if format == "pandas":
                return X_tr,y_tr,X_te,y_te 
            else:
               
                return list(X_tr['text']), list(y_tr[target]),list(X_te['text']), list(y_te[target])  
        else:
            print("Incorrect params")


################## Multimodales  ###########################

def load_twiteer_human(self,  format = "pandas", in_x_y= True, samples= 2, encoding= 'utf-8', target = 'account_type'):
    import pandas as pd 
    import os 
    path = self.download()
    pall  = os.path.join(path,'twitter_human_bots_dataset.csv')
  
    
    dfall = pd.read_csv(pall,encoding= 'utf-8').drop(['id','Unnamed: 0'],axis=1)
    dfall['account_type'] = dfall['account_type'].astype('category')
    dfall['created_at'] =  pd.to_datetime(dfall['created_at'],infer_datetime_format=True)
    dftr = dfall.iloc[0:29950].reset_index()
    dfte = dfall.iloc[29950:].reset_index(drop = True)

    if in_x_y == False:
        if samples == 1:
            return dfall
        elif samples ==2:
            return dftr,dfte
        else:
            print("Incorrect params") 
    else:
        y_tr = dftr.filter(regex=target)
        dummy_tr = dftr.drop([target],axis=1)

        y_te = dfte.filter(regex=target) 
        dummy_te = dfte.drop([target],axis=1) 
        if samples== 1:
            y = dfall.filter(regex=target)
            dummy_all = dfall.drop([target],axis=1) 
        
            if format == "pandas":
                return dummy_all,y
            else:
                X = dummy_all.to_numpy().tolist()
                return X,list(y[target]) 
        elif samples ==2:
            if format == "pandas":
                return dummy_tr,y_tr,dummy_te,y_te 
            else:
                #X_tr = list()
                #for i in range(len(dummy_tr.axes[0])):
                    #X_tr.append((dummy_tr.iloc[i,0],dummy_tr.iloc[i,1])) 
                X_tr = dummy_tr.to_numpy().tolist()
                #X_te = list()
                #for i in range(len(dummy_te.axes[0])):
                 #   X_te.append((dummy_te.iloc[i,0],dummy_te.iloc[i,1])) 
                X_te = dummy_te.to_numpy().tolist()
                return X_tr, list(y_tr[target]),X_te, list(y_te[target])  
        else:
            print("Incorrect params")  

def load_google_guest(self,  format = "pandas", in_x_y= True, samples= 2, encoding= 'utf-8',target = "question_well_written"):
   
    import pandas as pd 
    import os 
    path = self.download()
    ptrain = os.path.join(path,'train.csv')
    ptest = os.path.join(path,'test.csv')
    pplabel = os.path.join(path,'sample_submission.csv')
    
    dftr = pd.read_csv(ptrain,encoding= 'utf-8').drop(['qa_id'],axis=1)
    dfte1 = pd.read_csv(ptest,encoding= 'utf-8').drop(['qa_id'],axis=1)
    dfte2 = pd.read_csv(pplabel,encoding= 'utf-8').drop(['qa_id'],axis=1)
    
    dftr['category'] = dftr['category'].astype('category')
    dfte = pd.concat([dfte1,dfte2],axis=1)
    dfte['category'] = dfte['category'].astype('category')
    dfall = pd.concat([dftr,dfte],axis=0).reset_index(drop = True)
  
    if in_x_y == False:
        if samples == 1:
            return dfall
        elif samples ==2:
            return dftr,dfte
        else:
            print("Incorrect params") 
    else:
        y_tr = dftr.filter(regex=target)
        dummy_tr = dftr.drop([target],axis=1)

        y_te = dfte.filter(regex=target) 
        dummy_te = dfte.drop([target],axis=1) 
        if samples== 1:
            y = dfall.filter(regex=target)
            dummy_all = dfall.drop([target],axis=1) 
        
            if format == "pandas":
                return dummy_all,y
            else:
                X = dummy_all.to_numpy().tolist()
                return X,list(y[target]) 
        elif samples ==2:
            if format == "pandas":
                return dummy_tr,y_tr,dummy_te,y_te 
            else:
                #X_tr = list()
                #for i in range(len(dummy_tr.axes[0])):
                    #X_tr.append((dummy_tr.iloc[i,0],dummy_tr.iloc[i,1])) 
                X_tr = dummy_tr.to_numpy().tolist()
                #X_te = list()
                #for i in range(len(dummy_te.axes[0])):
                 #   X_te.append((dummy_te.iloc[i,0],dummy_te.iloc[i,1])) 
                X_te = dummy_te.to_numpy().tolist()
                return X_tr, list(y_tr[target]),X_te, list(y_te[target])  
        else:
            print("Incorrect params") 
     
def load_inferes(self,  format = "pandas", in_x_y= True, samples= 2, encoding= 'utf-8'):
    import pandas as pd
    import os 
    path = self.download()
    train = os.path.join(path,'train_.csv')
    dev =  os.path.join(path,'dev.csv')
    test =  os.path.join(path,'test.csv')
    dftr1 = pd.read_csv(train)
    dfte = pd.read_csv(test)
    dfde1 = pd.read_csv(dev)
    dftr = pd.concat([dftr1,dfde1],axis = 0).reset_index(drop = True)
    dfall = pd.concat([dftr,dfte],axis = 0).reset_index(drop = True)
    dfall['Label'] = dfall['Label'].astype('category')
    dftr['Label'] = dftr['Label'].astype('category')
    dfte['Label'] = dfte['Label'].astype('category')
    
    if in_x_y == False:
            if samples == 1:
                return dfall.drop(['ID'],axis=1)
            elif samples ==2:
                return dftr.drop(['ID'],axis=1),dfte.drop(['ID'],axis=1)
            else:
                print("Incorrect params") 
    else:
        y_tr = dftr.filter(regex='Label')
        dummy_tr = dftr.drop(['Label','ID'],axis=1)

        y_te = dfte.filter(regex='Label') 
        dummy_te = dfte.drop(['Label','ID'],axis=1) 
        if samples== 1:
            y = dfall.filter(regex='Label')
            dummy_all = dfall.drop(['Label','ID'],axis=1) 
        
            if format == "pandas":
                return dummy_all,y
            else:
                X = dummy_all.to_numpy().tolist()
                return X,list(y['Label']) 
        elif samples ==2:
            if format == "pandas":
                return dummy_tr,y_tr,dummy_te,y_te 
            else:
                #X_tr = list()
                #for i in range(len(dummy_tr.axes[0])):
                    #X_tr.append((dummy_tr.iloc[i,0],dummy_tr.iloc[i,1])) 
                X_tr = dummy_tr.to_numpy().tolist()
                #X_te = list()
                #for i in range(len(dummy_te.axes[0])):
                #   X_te.append((dummy_te.iloc[i,0],dummy_te.iloc[i,1])) 
                X_te = dummy_te.to_numpy().tolist()
                return X_tr, list(y_tr['Label']),X_te, list(y_te['Label'])  
        else:
            print("Incorrect params") 

def load_predict_salary(self,format = "pandas" , in_x_y= True, samples= 2, encoding= 'utf-8'):
    import pandas as pd
    import os 
    path = self.download()
    ptrain = os.path.join(path,'Final_Train_Dataset.csv')
    ptest =  os.path.join(path,'Final_Test_Dataset.csv')
    plabel_test =  os.path.join(path,'sample_submission.xlsx')
    
    dftr = pd.read_csv(ptrain, encoding = encoding)
    Xtest = pd.read_csv(ptest, encoding = encoding)
    ytest = pd.read_excel(plabel_test)
    dfte = pd.concat([ Xtest, ytest],axis=1)
    dftr = dftr.set_axis( ['id','experience','job_description','job_desig','job_type','key_skills','location','salary','company_name_encoded'],axis = 1).drop(['id'],axis=1)
    dfall = pd.concat([dftr,dfte],axis=0).reset_index(drop = True)
 
    #experience,job_description,job_desig,job_type,key_skills,location,salary,company_name_encoded
    if in_x_y == False:
        if samples == 1:
            return dfall
        elif samples ==2:
            return dftr,dfte
        else:
            print("Incorrect params") 
    else:
        y_tr = dftr.filter(regex='salary')
        dummy_tr = dftr.drop(['salary'],axis=1)

        y_te = dfte.filter(regex='salary') 
        dummy_te = dfte.drop(['salary'],axis=1) 
        if samples== 1:
            y = dfall.filter(regex='salary')
            dummy_all = dfall.drop(['salary'],axis=1) 
        
            if format == "pandas":
                return dummy_all,y
            else:
                X = dummy_all.to_numpy().tolist()
                return X,list(y['salary']) 
        elif samples ==2:
            if format == "pandas":
                return dummy_tr,y_tr,dummy_te,y_te 
            else:
                #X_tr = list()
                #for i in range(len(dummy_tr.axes[0])):
                    #X_tr.append((dummy_tr.iloc[i,0],dummy_tr.iloc[i,1])) 
                X_tr = dummy_tr.to_numpy().tolist()
                #X_te = list()
                #for i in range(len(dummy_te.axes[0])):
                 #   X_te.append((dummy_te.iloc[i,0],dummy_te.iloc[i,1])) 
                X_te = dummy_te.to_numpy().tolist()
                return X_tr, list(y_tr['salary']),X_te, list(y_te['salary'])  
        else:
            print("Incorrect params")    

def load_price_book(self,format = "pandas" , in_x_y= True, samples= 2, encoding= 'utf-8'):   
   
     
    import pandas as pd 
    import os 
    path = self.download()
    # Load the xlsx file

    ptrain = os.path.join(path,'Data_Train.xlsx')
    ptest = os.path.join(path,'Data_Test.xlsx')
    plabel_test =  os.path.join(path,'Sample_Submission.xlsx')
    # df_te["Class Name"] = df_te["Class Name"].astype("category")
    # print(df_te['Class Name'])
    # df_te = df_te[df_te["Class Name"].notna()]
    # print(df_te.isnull().sum())
    
    train = pd.read_excel(ptrain,engine='openpyxl',)
    test = pd.read_excel(ptest,engine='openpyxl')
    label_test = pd.read_excel(plabel_test,engine='openpyxl')
    
    # Read the values of the file in the dataframe
    dftr = pd.DataFrame(train)
    dftest1 = pd.DataFrame(test)
    dftest2 = pd.DataFrame(label_test)
    dfte = pd.concat([dftest1,dftest2],axis=1)
    dfall = pd.concat([dftr,dfte],axis=0).reset_index(drop = True)
    
    if in_x_y == False:
        if samples == 1:
            return dfall
        elif samples ==2:
            return dftr,dfte
        else:
            print("Incorrect params") 
    else:
        y_tr = dftr.filter(regex='Price')
        dummy_tr = dftr.drop(['Price'],axis=1)

        y_te = dfte.filter(regex='Price') 
        dummy_te = dfte.drop(['Price'],axis=1) 
        if samples== 1:
            y = dfall.filter(regex='Price')
            dummy_all = dfall.drop(['Price'],axis=1) 
        
            if format == "pandas":
                return dummy_all,y
            else:
                X = dummy_all.to_numpy().tolist()
                return X,list(y['Price']) 
        elif samples ==2:
            if format == "pandas":
                return dummy_tr,y_tr,dummy_te,y_te 
            else:
                #X_tr = list()
                #for i in range(len(dummy_tr.axes[0])):
                    #X_tr.append((dummy_tr.iloc[i,0],dummy_tr.iloc[i,1])) 
                X_tr = dummy_tr.to_numpy().tolist()
                #X_te = list()
                #for i in range(len(dummy_te.axes[0])):
                 #   X_te.append((dummy_te.iloc[i,0],dummy_te.iloc[i,1])) 
                X_te = dummy_te.to_numpy().tolist()
                return X_tr, list(y_tr['Price']),X_te, list(y_te['Price'])  
        else:
            print("Incorrect params") 
    
def load_stroke(self,format = "pandas" , in_x_y= True, samples= 2, encoding= 'utf-8',target= 'stroke'):
    import pandas as pd 
    import os 
    path = self.download()
    pall = os.path.join(path,'healthcare-dataset-stroke-data.csv')

    dfall = pd.read_csv(pall,encoding=encoding).drop(['id'],axis=1)
    dtr1 = dfall.iloc[:199]
    dfte = dfall.iloc[199:1221].reset_index(drop=True)
    dtr2 = dfall.iloc[1221:]
    dftr = pd.concat([dtr1,dtr2],axis = 0).reset_index(drop=True)

    if in_x_y == False:
        if samples == 1:
            return dfall
        elif samples ==2:
            return dftr,dfte
        else:
            print("Incorrect params") 
    else:
        y_tr = dftr.filter(regex=target)
        dummy_tr = dftr.drop([target],axis=1)

        y_te = dfte.filter(regex=target) 
        dummy_te = dfte.drop([target],axis=1) 
        if samples== 1:
            y = dfall.filter(regex=target)
            dummy_all = dfall.drop([target],axis=1) 
        
            if format == "pandas":
                return dummy_all,y
            else:
                X = dummy_all.to_numpy().tolist()
                return X,list(y[target]) 
        elif samples ==2:
            if format == "pandas":
                return dummy_tr,y_tr,dummy_te,y_te 
            else:
                #X_tr = list()
                #for i in range(len(dummy_tr.axes[0])):
                    #X_tr.append((dummy_tr.iloc[i,0],dummy_tr.iloc[i,1])) 
                X_tr = dummy_tr.to_numpy().tolist()
                #X_te = list()
                #for i in range(len(dummy_te.axes[0])):
                    #   X_te.append((dummy_te.iloc[i,0],dummy_te.iloc[i,1])) 
                X_te = dummy_te.to_numpy().tolist()
                return X_tr, list(y_tr[target]),X_te, list(y_te[target])  
        else:
            print("Incorrect params") 

def load_wines(self,format = "pandas" , in_x_y= True, samples= 2, encoding= 'utf-8',target = 'price'):
    import pandas as pd 
    import os 
    path = self.download()
    pall = os.path.join(path,'wines_SPA.csv')
    
    dfall = pd.read_csv(pall,encoding=encoding)
    dfall['body'] = dfall['body'].astype('Int64') 
    dfall['acidity'] = dfall['acidity'].astype('Int64')
    dftr = dfall.iloc[:6000]
    dfte = dfall.iloc[6000:].reset_index(drop= True)
   
    if in_x_y == False:
        if samples == 1:
            return dfall
        elif samples ==2:
            return dftr,dfte
        else:
            print("Incorrect params") 
    else:
        y_tr = dftr.filter(regex=target)
        dummy_tr = dftr.drop([target],axis=1)

        y_te = dfte.filter(regex=target) 
        dummy_te = dfte.drop([target],axis=1) 
        if samples== 1:
            y = dfall.filter(regex=target)
            dummy_all = dfall.drop([target],axis=1) 
        
            if format == "pandas":
                return dummy_all,y
            else:
                X = dummy_all.to_numpy().tolist()
                return X,list(y[target]) 
        elif samples ==2:
            if format == "pandas":
                return dummy_tr,y_tr,dummy_te,y_te 
            else:
                #X_tr = list()
                #for i in range(len(dummy_tr.axes[0])):
                    #X_tr.append((dummy_tr.iloc[i,0],dummy_tr.iloc[i,1])) 
                X_tr = dummy_tr.to_numpy().tolist()
                #X_te = list()
                #for i in range(len(dummy_te.axes[0])):
                 #   X_te.append((dummy_te.iloc[i,0],dummy_te.iloc[i,1])) 
                X_te = dummy_te.to_numpy().tolist()
                return X_tr, list(y_tr[target]),X_te, list(y_te[target])  
        else:
            print("Incorrect params") 

def load_women_clothing(self,format = "pandas" , in_x_y= True, samples= 2, encoding= 'utf-8'):
    import pandas as pd 
    import os 
    path = self.download()
    all = os.path.join(path,'womens_clothing.csv')

    dfall = pd.read_csv(all).filter(regex='(Age|Title|Review Text|Rating|Recommended IND|Positive Feedback Count|Division Name|Department Name|Class Name)')
    dfall['Class Name'] = dfall['Class Name'].astype('category')
    dftr = dfall.iloc[:16440]
    dfte = dfall.iloc[16440:].reset_index(drop= True)
    
    if in_x_y == False:
        if samples == 1:
            return dfall
        elif samples ==2:
            return dftr,dfte
        else:
            print("Incorrect params") 
    else:
        y_tr = dftr.filter(regex='Class Name')
        dummy_tr = dftr.drop(['Class Name'],axis=1)

        y_te = dfte.filter(regex='Class Name') 
        dummy_te = dfte.drop(['Class Name'],axis=1) 
        if samples== 1:
            y = dfall.filter(regex='Class Name')
            dummy_all = dfall.drop(['Class Name'],axis=1) 
        
            if format == "pandas":
                return dummy_all,y
            else:
                X = dummy_all.to_numpy().tolist()
                return X,list(y['Class Name']) 
        elif samples ==2:
            if format == "pandas":
                return dummy_tr,y_tr,dummy_te,y_te 
            else:
                #X_tr = list()
                #for i in range(len(dummy_tr.axes[0])):
                    #X_tr.append((dummy_tr.iloc[i,0],dummy_tr.iloc[i,1])) 
                X_tr = dummy_tr.to_numpy().tolist()
                #X_te = list()
                #for i in range(len(dummy_te.axes[0])):
                 #   X_te.append((dummy_te.iloc[i,0],dummy_te.iloc[i,1])) 
                X_te = dummy_te.to_numpy().tolist()
                return X_tr, list(y_tr['Class Name']),X_te, list(y_te['Class Name'])  
        else:
            print("Incorrect params") 
    
    
    
    print(dfte)
   
def load_project_kickstarter(self, format = "pandas" , in_x_y= True, samples= 2, encoding= 'utf-8'):
    import pandas as pd 
    import os 
    path = self.download()
    ptrain = os.path.join(path,'train.csv')
    ptest = os.path.join(path,'test.csv')
    pplabel = os.path.join(path,'samplesubmission.csv')

    
    # Read the values of the file in the datafrae
    dftr = pd.read_csv(ptrain,encoding= 'utf-8')
    dfte1 = pd.read_csv(ptest,encoding= 'utf-8')
    dfte2 = pd.read_csv(pplabel,encoding= 'utf-8')

    dfte = pd.concat([dfte1,dfte2],axis=1).drop(['project_id'],axis=1)
    dftr = dftr.drop(['project_id','backers_count'],axis=1)
    dfall = pd.concat([dftr,dfte],axis=0).reset_index(drop = True)
    
    if in_x_y == False:
        if samples == 1:
            return dfall
        elif samples ==2:
            return dftr,dfte
        else:
            print("Incorrect params") 
    else:
        y_tr = dftr.filter(regex='final_status')
        dummy_tr = dftr.drop(['final_status'],axis=1)

        y_te = dfte.filter(regex='final_status') 
        dummy_te = dfte.drop(['final_status'],axis=1) 
        if samples== 1:
            y = dfall.filter(regex='final_status')
            dummy_all = dfall.drop(['final_status'],axis=1) 
        
            if format == "pandas":
                return dummy_all,y
            else:
                X = dummy_all.to_numpy().tolist()
                return X,list(y['final_status']) 
        elif samples ==2:
            if format == "pandas":
                return dummy_tr,y_tr,dummy_te,y_te 
            else:
                #X_tr = list()
                #for i in range(len(dummy_tr.axes[0])):
                    #X_tr.append((dummy_tr.iloc[i,0],dummy_tr.iloc[i,1])) 
                X_tr = dummy_tr.to_numpy().tolist()
                #X_te = list()
                #for i in range(len(dummy_te.axes[0])):
                 #   X_te.append((dummy_te.iloc[i,0],dummy_te.iloc[i,1])) 
                X_te = dummy_te.to_numpy().tolist()
                return X_tr, list(y_tr['final_status']),X_te, list(y_te['final_status'])  
        else:
            print("Incorrect params") 

def load_jobs(self, format = "pandas" , in_x_y= True, samples= 2, encoding= 'utf-8'):
    import pandas as pd 
    import os 
    import numpy as np
    path = self.download()
    pall = os.path.join(path,'fake_job_postings.csv')
    
    dfall = pd.read_csv(pall,encoding=encoding).drop(['job_id'],axis =1)
        
    dftr = dfall.iloc[:12516]
    dfte = dfall.iloc[12516:].reset_index(drop= True)
   
    if in_x_y == False:
        if samples == 1:
            return dfall
        elif samples ==2:
            return dftr,dfte
        else:
            print("Incorrect params") 
    else:
        y_tr = dftr.filter(regex='fraudulent')
        dummy_tr = dftr.drop(['fraudulent'],axis=1)

        y_te = dfte.filter(regex='fraudulent') 
        dummy_te = dfte.drop(['fraudulent'],axis=1) 
        if samples== 1:
            y = dfall.filter(regex='fraudulent')
            dummy_all = dfall.drop(['fraudulent'],axis=1) 
        
            if format == "pandas":
                return dummy_all,y
            else:
                X = dummy_all.to_numpy().tolist()
                return X,list(y['fraudulent']) 
        elif samples ==2:
            if format == "pandas":
                return dummy_tr,y_tr,dummy_te,y_te 
            else:
                #X_tr = list()
                #for i in range(len(dummy_tr.axes[0])):
                    #X_tr.append((dummy_tr.iloc[i,0],dummy_tr.iloc[i,1])) 
                X_tr = dummy_tr.to_numpy().tolist()
                #X_te = list()
                #for i in range(len(dummy_te.axes[0])):
                 #   X_te.append((dummy_te.iloc[i,0],dummy_te.iloc[i,1])) 
                X_te = dummy_te.to_numpy().tolist()
                return X_tr, list(y_tr['fraudulent']),X_te, list(y_te['fraudulent'])  
        else:
            print("Incorrect params") 
   
###################################### Image  #######################################
def load_fashion(self):
    import pandas as pd 
    import os 
    path = self.download()
    ptrain = os.path.join(path,'train.csv')
    ptest =  os.path.join(path,'dev.csv')
    pdev = os.path.join(path,'test.csv')
    
    df_tr = pd.read_csv(ptrain)
    df_de = pd.read_csv(pdev)
    df_te = pd.read_csv(ptest)
    
    y_tr = df_tr['label'].to_numpy().tolist()
    y_de = df_de['label'].to_numpy().tolist()
    y_te = df_te['label'].to_numpy().tolist()
    
    del df_tr['label']
    del df_de['label']
    del df_te['label']
    return df_tr, y_tr, df_de,y_de ,df_te,y_te 