import spacy
from nltk.corpus import stopwords
import re


def tokenizing(file_name):
    nlp = spacy.load("es_core_news_sm")
    # nlp.max_length = 1600000

    corpus_news = []
    with open(file_name, 'r',encoding='utf8') as input_file:
        for line in input_file.readlines():
            corpus_news.append(line)
        

        for i in range(len(corpus_news)):
            new = corpus_news[i]
            new =re.sub("\d+&+","",new.replace("\n", ""))
            new =re.sub("[a-zA-ZÀ-ÿ]+&+","",new)
            new =re.sub("&+","",new)
            new =re.sub("[\d.]+","",new)
            new =re.sub("(,\s,\s)+","",new)
            corpus_news[i] = new
        

        for i in range(len(corpus_news)):
            tokens = nlp(corpus_news[i])
            news = []
            for token in tokens:
                news.append(token.text)
            corpus_news[i] = news
        
        return corpus_news


def rake(news):

    nlp = spacy.load("es_core_news_sm")

    tokens = nlp(news)
    words_candidates = []
    candidates = []
    for i in tokens:
        if not i.is_stop:
            words_candidates.append(i)
        elif i.is_stop and len(words_candidates) > 0:
            candidates.append(words_candidates)
            words_candidates = []

    if len(words_candidates) > 0:
        candidates.append(words_candidates)
        words_candidates = []

    print(candidates)




    

def main():

    file_name = 'test.txt'
    corpus_news_tokenized = tokenizing(file_name)

    corpus_news = []

    with open(file_name, 'r',encoding='utf8') as input_file:
        for line in input_file.readlines():
            corpus_news.append(line)

        for i in range(len(corpus_news)):
            new = corpus_news[i]
            new =re.sub("\d+&+","",new.replace("\n", ""))
            new =re.sub("[a-zA-ZÀ-ÿ]+&+","",new)
            new =re.sub("&+","",new)
            new =re.sub("[\d.]+","",new)
            new =re.sub("(,\s,\s)+","",new)
            corpus_news[i] = new
        
        # for i in corpus_news:
        #     rake(i)
    
        rake(corpus_news[1])



if __name__ == "__main__":
    main()