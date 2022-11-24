import spacy
import re


def main():
    file_name = 'corpus_noticias.txt'
    nlp = spacy.load("es_core_news_sm")
    # nlp.max_length = 1600000

    corpus_news = []
    with open(file_name, 'r', encoding='utf8') as input_file:
        for line in input_file.readlines():
            corpus_news.append(line)
        

        for i in range(len(corpus_news)):
            new = corpus_news[i]
            new =re.sub("\d+&+","",new.replace("\n", "").replace("'", "").replace(",", ""))
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

    with open("./tokenized_corpus.txt", "wt+", encoding='UTF8') as f:
        for i in corpus_news:
            len_new = len(i)
            f.write("[")
            for j, elem in enumerate(i):
                if j+1 == len_new:
                    f.write(f"{elem}")
                else:
                    f.write(f"{elem},")
            f.write("]\n")


if __name__ == '__main__':
    main()